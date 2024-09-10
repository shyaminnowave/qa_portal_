from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.testcases.models import TestCaseModel, TestCaseStep, NatcoStatus
from apps.stbs.models import NactoManufactureLanguage
from django.db import transaction
from django.shortcuts import get_object_or_404


@receiver(post_save, sender=TestCaseModel)
def save_natco_status(sender, instance, created, **kwargs):
    _data = []
    natco = NactoManufactureLanguage.objects.all()
    if created == True:
        for data in natco:
            _data.append(NatcoStatus(natco=data.natco, language=data.language_name, device=data.device_name,
                                         test_case=instance))
        try:
            with transaction.atomic():
                NatcoStatus.objects.bulk_create(_data)
        except Exception as e:
            print(e)
    else:
        pass


