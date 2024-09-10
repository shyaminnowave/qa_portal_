from django.db import models
from django_extensions.db.models import TimeStampedModel
from simple_history.models import HistoricalRecords
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Language(TimeStampedModel):
    language_name = models.CharField(max_length=100)
    history = HistoricalRecords()

    def __str__(self) -> str:
        return '%s' % self.language_name

    class Meta:
        permissions = [
            ("view_language_option", "Can View Language Option List")
        ]


class STBManufacture(TimeStampedModel):
    name = models.CharField(max_length=200)
    history = HistoricalRecords()

    def __str__(self) -> str:
        return '%s' % self.name

    class Meta:
        permissions = [
            ("view_stb_option", "Can View stb Option List")
        ]
        verbose_name = 'STB Manufactures'
        verbose_name_plural = 'STB Manufactures'


class Natco(TimeStampedModel):

    country = models.CharField(max_length=200)
    natco = models.CharField(max_length=10)
    manufacture = models.ManyToManyField(STBManufacture, blank=True)
    language = models.ManyToManyField(Language)
    history = HistoricalRecords()

    def __str__(self) -> str:
        return '%s' % self.natco

    class Meta:
        permissions = [
            ("view_natco_option", "Can View natco Option List")
        ]


class NactoManufactureLanguage(TimeStampedModel):
    natco = models.ForeignKey(Natco, on_delete=models.CASCADE, related_name='natco_info')
    device_name = models.ForeignKey(STBManufacture, on_delete=models.CASCADE, related_name='natco_manufacture')
    language_name = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='natco_language')
    history = HistoricalRecords()

    def __str__(self) -> str:
        return '%s - %s' % (self.natco.natco, self.language_name.language_name)

    class Meta:
        permissions = [
            ("view_natco_manufacture_option", "Can View Natco Manufacture Language Option List")
        ]
        verbose_name = 'Natco Manufactures Languages'
        verbose_name_plural = 'Natco Manufactures Languages'


class STBNode(TimeStampedModel):
    node_id = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.node_id

    class Meta:
        verbose_name = 'STB Nodes'
        verbose_name_plural = 'STB Nodes'


class NatcoRelease(TimeStampedModel):

    class ReleaseType(models.TextChoices):
        MAJOR = 'MR', _('MR')

    natcos = models.ForeignKey(Natco, on_delete=models.CASCADE, related_name='release')
    release_type = models.CharField(choices=ReleaseType.choices, max_length=20, help_text="MR - Major Release")
    build_type = models.CharField(max_length=200, default='', blank=True, null=True)
    version = models.CharField(max_length=20, default='', blank=True, null=True)
    android_version = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.natcos.natco} {self.release_type} - {self.version}"

    def natco(self):
        return f"{self.natcos.natco} {self.release_type} - {self.version}"

    class Meta:
        verbose_name = 'Natco Releases'
        verbose_name_plural = 'Natco Releases'


class STBNodeConfig(TimeStampedModel):

    stb_node = models.ForeignKey(STBNode, on_delete=models.CASCADE)
    natco = models.ForeignKey(NatcoRelease, on_delete=models.CASCADE, max_length=255, default='')
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.natco.natcos.natco} {self.natco.release_type} {self.natco.version} A{self.natco.android_version} -" \
               f" {self.stb_node.node_id}"

    class Meta:
        verbose_name = 'STB Node Configs'
        verbose_name_plural = 'STB Node Configs'


class PercentileReport(TimeStampedModel):
    release = models.ForeignKey(STBNodeConfig, on_delete=models.CASCADE)
    script = models.ForeignKey('testcases.TestCaseModel', on_delete=models.CASCADE)
    load_time = models.CharField(max_length=200)
    cpu_usage = models.CharField(max_length=200)
    ram_usage = models.CharField(max_length=200)


# class TestIteration(TimeStampedModel):

#     release = models.ForeignKey(STBSRelease, on_delete=models.CASCADE)
#     script = models.ForeignKey('testcases.TestCaseModel', on_delete=models.CASCADE)
#     iteration_numbers = models.IntegerField()
#     load_times = models.CharField(max_length=200)
#     cpu_usage = models.CharField(max_length=200)
#     ram_usage = models.CharField(max_length=200)

