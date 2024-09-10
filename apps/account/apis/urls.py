from django.urls import path
from apps.account.apis import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView


app_name = 'accounts'

urlpatterns = [
    path('create-account/', views.AccountCreateView.as_view(), name='create-user'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/<slug:username>/', views.UserProfileView.as_view()),
    path('user-list/', views.UserListView.as_view()),
    path('user-update/<str:username>/', views.UserUpdateGroup.as_view()),
    path('permissions/', views.PermissionListView.as_view()),
    path('group/', views.GroupView.as_view()),
    path('create-group/', views.GroupCreateView.as_view()),
    path('group-detail/<int:pk>/', views.GroupDetailView.as_view())

]
