from rest_framework.permissions import AllowAny, IsAuthenticated, DjangoModelPermissions, \
    DjangoObjectPermissions, BasePermission


class TestCaseViewPermission(DjangoModelPermissions):

    perms_map = {
        'GET': ['testcases.view_testcase']
    }


class TestCasePermission(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm('testcases.view_testcase'))
