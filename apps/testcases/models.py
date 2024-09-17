import re
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from apps.stbs.models import Language, Natco, STBManufacture, STBNodeConfig, NatcoRelease
from django.contrib.auth import get_user_model
from simple_history.models import HistoricalRecords
from django.db.models import Max
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from autoslug import AutoSlugField
# Create your models here.

User = get_user_model()

# ------------------------ Choices Enum ------------------------


class PriorityChoice(models.TextChoices):
    CLASSONE = 'class_1', _('Class 1')
    CLASSTWO = 'class_2', _('Class 2')
    CLASSTHREE = 'class_3', _('Class 3')


class StatusChoices(models.TextChoices):
    TODO = 'todo', _('Todo')
    ONGOING = 'ongoing', _('Ongoing')
    COMPLETED = 'completed', _('Completed')


class AutomationChoices(models.TextChoices):
    AUTOMATABLE = 'automatable', _('Automatable')
    NOT_AUTOMATABLE = 'not-automatable', _('Not-Automatable')
    IN_DEVELOPMENT = 'in-development', _('In-Development')
    REVIEW = 'review', _('Review')
    READY = 'ready', _('Ready')
    COMPLETE = StatusChoices.COMPLETED


class TestCaseChoices(models.TextChoices):

    PERFORMANCE = 'performance', _('Perfomance')
    SOAK = 'soak', _('Soak')
    SMOKE = 'smoke', _('Smoke')

# ----------------------------------------------------


class TestCaseScript(models.Model):

    testcase = models.ForeignKey('TestCaseModel', on_delete=models.SET_NULL, blank=True, null=True,
                                 related_name='testcase_script')
    script_name = models.CharField(max_length=200, default='')
    script_location = models.URLField()
    script_type = models.CharField(choices=TestCaseChoices.choices, max_length=20)
    developed_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True,
                                     related_name='script_developed')
    reviewed_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True,
                                    related_name='script_reviewed')
    modified_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True,
                                    related_name='script_modified')
    description = models.TextField(default='')

    class Meta:
        verbose_name = 'TestCase Script'
        verbose_name_plural = 'TestCase Script'


class TestCaseModel(TimeStampedModel):

    jira_id = models.IntegerField(_("Jira Id"), unique=True, help_text=("Jira Id"), blank=True, null=True)
    test_name = models.CharField(_("Test Report Name"), max_length=255, help_text=("Please Enter the TestCase Name"))
    priority = models.CharField(max_length=20, choices=PriorityChoice.choices, default=PriorityChoice.CLASSTHREE)
    summary = models.TextField(_("Jira Summary"), default='')
    description = models.TextField(_('TestCase Description'), default='')
    testcase_type = models.CharField(max_length=20, choices=TestCaseChoices.choices,  default=TestCaseChoices.SMOKE)
    script = models.ForeignKey(TestCaseScript, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.TODO)
    automation_status = models.CharField(max_length=20, choices=AutomationChoices.choices,
                                         default=AutomationChoices.NOT_AUTOMATABLE)
    comments = GenericRelation("Comment", related_name='testcases')
    slug = AutoSlugField(populate_from='test_name', unique=True, always_update=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'TestCase'
        verbose_name_plural = 'TestCases'
        ordering = ['-id',]

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __str__(self) -> str:
        return '%s' % self.test_name

    def get_jira_id(self) -> str:
        return 'TTVTM-%s' % self.jira_id
    
    def get_status(self) -> str:
        return '%s' % self.status

    def get_short_descript(self) -> str:
        return self.description

    def get_slug(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.id:
            get_current_id = TestCaseModel.objects.aggregate(max_id=Max('id'))['max_id']
            if get_current_id is None:
                self.id = 13000
            else:
                self.id = get_current_id + 1
        super().save(*args, **kwargs)


class NatcoSupport(TimeStampedModel):
    class NatcoStatusChoice(models.TextChoices):
        AUTOMATABLE = AutomationChoices.AUTOMATABLE
        NOT_AUTOMATABLE = AutomationChoices.NOT_AUTOMATABLE
        IN_DEVELOPMENT = AutomationChoices.IN_DEVELOPMENT
        REVIEW = AutomationChoices.REVIEW
        READY = AutomationChoices.READY
        MANUAL = 'manual', _('Manual')

    testcase = models.ForeignKey(TestCaseModel, on_delete=models.CASCADE, related_name='natco_support')
    natcos = models.ManyToManyField(Natco, blank=True, related_name='supported_natcos')
    language = models.ManyToManyField(Language, blank=True, related_name='supported_languages')
    devices = models.ManyToManyField(STBManufacture, blank=True, related_name='supported_devices')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_natco', blank=True, null=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='natco_reviewer', blank=True,
                                    null=True)
    modified = models.ForeignKey(User, on_delete=models.CASCADE, related_name='natoc_modified', blank=True, null=True)
    applicable = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.testcase


class NatcoStatus(TimeStampedModel):

    class NatcoStatusChoice(models.TextChoices):
        AUTOMATABLE = AutomationChoices.AUTOMATABLE
        NOT_AUTOMATABLE = AutomationChoices.NOT_AUTOMATABLE
        IN_DEVELOPMENT = AutomationChoices.IN_DEVELOPMENT
        REVIEW = AutomationChoices.REVIEW
        READY = AutomationChoices.READY
        MANUAL = 'manual', _('Manual')

    natco = models.ForeignKey(Natco, on_delete=models.CASCADE, related_name='natco_status')
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    device = models.ForeignKey(STBManufacture, on_delete=models.CASCADE)
    test_case = models.ForeignKey(TestCaseModel, on_delete=models.CASCADE, related_name='natco_status')
    status = models.CharField(max_length=20, choices=NatcoStatusChoice.choices, default=NatcoStatusChoice.MANUAL)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_natco', blank=True, null=True)
    # reviewed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='natco_reviewer', blank=True,
    #                                 null=True)
    # modified = models.ForeignKey(User, on_delete=models.CASCADE, related_name='natoc_modified', blank=True, null=True)
    applicable = models.BooleanField(default=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Natco Status'
        verbose_name_plural = 'Natco Status'

    def __str__(self):
        return '%s' % self.test_case

    def save(self, **kwargs):
        status = self.status
        test_case = TestCaseModel.objects.get(jira_id=self.test_case.jira_id)
        if status == 'in_development':
            test_case.automation_status = 'in-development'
        elif status == 'review':
            test_case.automation_status = 'review'
        elif status == 'ready':
            test_case.automation_status = 'ready'
        test_case.save()
        super(NatcoStatus, self).save(**kwargs)


class TestCaseStep(TimeStampedModel):

    testcase = models.ForeignKey(TestCaseModel, on_delete=models.CASCADE, related_name='test_steps', blank=True,
                                 null=True)
    step_number = models.IntegerField(_("step number"), blank=True, null=True)
    step_data = models.TextField(_('Testing Parameters'), blank=True, null=True)
    step_action = models.TextField(blank=True, null=True)
    expected_result = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.TODO)
    history = HistoricalRecords()


class TestReport(TimeStampedModel):

    job_id = models.CharField(max_length=255)
    run_type = models.CharField(max_length=200, default='')
    date = models.DateField(max_length=200, default='')
    iteration_number = models.IntegerField()
    testcase = models.ForeignKey(TestCaseModel, on_delete=models.CASCADE, max_length=255, default='')
    node = models.ForeignKey(NatcoRelease, on_delete=models.SET_NULL, null=True, blank=True)
    loadtime = models.DecimalField(max_digits=10, decimal_places=5)
    cpu_hundred_percentile = models.CharField(max_length=200, default='')
    ram_hundred_percentile = models.CharField(max_length=200, default='')
    start_time = models.CharField(max_length=200, default='')
    end_time = models.CharField(max_length=200, default='')
    loadtime_percentile = models.CharField(max_length=200, default='')
    cpu_usage_percentile = models.CharField(max_length=200, default='')
    ram_usage_percentile = models.CharField(max_length=200, default='')
    result = models.CharField(max_length=200, default='', null=True, blank=True)
    failure_reason = models.TextField(default='', null=True, blank=True)
    comment = models.TextField(default='', null=True, blank=True)

    def __str__(self):
        return self.job_id


class TestcaseExcelResult(TimeStampedModel):

    run_type = models.CharField(max_length=200, default='')
    date = models.CharField(max_length=200, default='')
    iteration_number = models.CharField(max_length=200, default='')
    testcase = models.CharField(max_length=255, default='')
    cpu = models.CharField(max_length=200, default='')
    ram = models.CharField(max_length=200, default='')
    start_time = models.CharField(max_length=200, default='')
    end_time = models.CharField(max_length=200, default='')
    job_uid = models.CharField(max_length=255, default='')
    node_id = models.CharField(max_length=255, default='')
    failure_reason = models.TextField()
    result = models.CharField(max_length=200, default='pass')
    natco = models.CharField(max_length=200, default='')
    load_time = models.DecimalField(max_digits=10, decimal_places=5)
    cpu_usage = models.DecimalField(max_digits=10, decimal_places=5)
    ram_usage = models.DecimalField(max_digits=10, decimal_places=5)
    country_code = models.CharField(max_length=200, default='')
    stb_release = models.CharField(max_length=200, default='')
    stb_firmware = models.CharField(max_length=200, default='')
    stb_android = models.CharField(max_length=200, default='')
    stb_build = models.CharField(max_length=255, default='')
    natco_node = models.CharField(max_length=200, default='')
    comment = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.testcase

    @property
    def get_start_time(self):
        start_time = re.findall(r'\b\d{2}:\d{2}:\d{2}\b', self.start_time)
        return start_time[0]

    @property
    def get_end_time(self):
        end_time = re.findall(r'\b\d{2}:\d{2}:\d{2}\b', self.end_time)
        return end_time[0]

    @classmethod
    def get_unique_node(cls):  
        natco_node = cls.objects.values_list('natoc_node', flat=True).distinct()
        return natco_node

    @classmethod
    def get_unique_natco_type(cls):
        natco_type = cls.objects.values_list('natco', flat=True).distinct()
        return natco_type
    
    @classmethod
    def get_unique_stb_release(cls):  
        stb_release = cls.objects.values_list('stb_release', flat=True).distinct()
        return stb_release

    @classmethod
    def get_unique_stb_android(cls):
        stb_android = cls.objects.values_list('stb_android', flat=True).distinct()
        return stb_android
    
    @classmethod
    def get_unique_stb_firmware(cls):  
        stb_firmware = cls.objects.values_list('stb_firmware', flat=True).distinct()
        return stb_firmware
    
    @classmethod
    def get_unique_filters(cls):
        _filter = {
            'natco_node': cls.objects.values_list('natco_node', flat=True).distinct(),
            'natco_type': cls.objects.values_list('natco', flat=True).distinct(),
            'stb_release': cls.objects.values_list('stb_release', flat=True).distinct(),
            'stb_android': cls.objects.values_list('stb_android', flat=True).distinct(),
            'stb_firmware': cls.objects.values_list('stb_firmware', flat=True).distinct()
        }
        return _filter


class ScriptIssue(TimeStampedModel):

    class Status(models.TextChoices):
        RESOLVED = 'resolved', _('Resolved')
        INCOMPLETE = 'incomplete', _('Incomplete')

    testcase = models.ForeignKey(TestCaseModel, on_delete=models.CASCADE, max_length=255, related_name='issues')
    summary = models.TextField(default='')
    description = models.TextField(default='')
    result = models.CharField(max_length=255, default='')
    status = models.CharField(choices=Status.choices, default=Status.INCOMPLETE, max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name='created_issues')
    assinged_to = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                                        related_name='assinged_issues')
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                                    related_name='resolved_issues')
    comment = GenericRelation("Comment", related_name='issues')

    def __str__(self):
        return self.summary


class Comment(TimeStampedModel):

    comments = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name='created_comments')

    def __str__(self):
        return f"{self.comments[:20]}..."
