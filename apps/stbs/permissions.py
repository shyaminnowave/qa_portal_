from rest_framework.permissions import AllowAny, IsAuthenticated, DjangoModelPermissions, \
    DjangoObjectPermissions, BasePermission


class LangaugeOptionPermission(DjangoModelPermissions):

    perms_map = {
        'GET': ['stbs.view_language_option']
    }


class NatcoOptionPermission(DjangoModelPermissions):

    perms_map = {
        'GET': ['stbs.view_natco_option']
    }


class DeviceOptionPermission(DjangoModelPermissions):

    perms_map = {
        'GET': ['stbs.view_stb_option']
    }


class AdminPermission(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name='Admin'))


class LanguagePermission(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm('stbs.view_language'))

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'PUT', 'DELETE']:
            if request.method == 'GET':
                return bool(request.user and request.user.has_perm('stbs.view_langugae'))
            if request.method == 'PUT':
                return bool(request.user and request.user.has_perm('stbs.change_language'))
            if request.method == 'DELETE':
                return bool(request.user and request.user.has_perm('stbs.delete_language'))
        return False


class DevicePermission(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm('stbs.view_stbs_manufacture'))

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'PUT', 'DELETE']:
            if request.method == 'GET':
                return bool(request.user and request.user.has_perm('stbs.view_stbs_manufacture'))
            if request.method == 'PUT':
                return bool(request.user and request.user.has_perm('stbs.change_stbs_manufacture'))
            if request.method == 'DELETE':
                return bool(request.user and request.user.has_perm('stbs.delete_stbs_manufacture'))
        return False


class NatcoPermission(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm('stbs.view_natco'))

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'PUT', 'DELETE']:
            if request.method == 'GET':
                return bool(request.user and request.user.has_perm('stbs.view_natco'))
            if request.method == 'PUT':
                return bool(request.user and request.user.has_perm('stbs.change_natco'))
            if request.method == 'DELETE':
                return bool(request.user and request.user.has_perm('stbs.delete_natco'))
        return False
