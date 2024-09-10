from django.contrib import admin
from apps.stbs.models import Language, STBManufacture, Natco,  NactoManufactureLanguage, STBNode, STBNodeConfig,  \
    NatcoRelease
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin.widgets import ManyToManyRawIdWidget
# Register your models here.


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
     search_fields = ['language']


@admin.register(STBManufacture)
class STBManufactureAdmin(admin.ModelAdmin):
    search_fields = ['manufacture']


@admin.register(NactoManufactureLanguage)
class NatcoManufactureAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ['natco', 'device_name', 'language_name']
    list_editable = ['device_name', 'language_name']


@admin.register(Natco)
class NatcoAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):

    list_display = ['natco', 'country']
    search_fields = ['language', 'manufacture']
    autocomplete_fields = ['language', 'manufacture']


@admin.register(NatcoRelease)
class NatcoReleaseAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ['id', 'natcos', 'version', 'android_version']


admin.site.register(STBNode, ImportExportModelAdmin)
admin.site.register(STBNodeConfig, ImportExportModelAdmin)
