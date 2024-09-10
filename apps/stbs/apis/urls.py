from django.urls import path
from rest_framework import routers
from apps.stbs.apis import views
from apps.stbs.apis.views import LanguageViewset, STBManufactureViewSet, NatcoViewSet, NatcoLanguageViewSet

app_name = 'stbs'

routers = routers.SimpleRouter()
routers.register(r'language', LanguageViewset)
routers.register(r'stb-manufacture', STBManufactureViewSet)
routers.register(r'natco', NatcoViewSet)
routers.register(r'nacto-language', NatcoLanguageViewSet)

urlpatterns = [
    path('natco-option/', views.NatcoOptionView.as_view()),
    path('language-option/', views.LanguageOptionView.as_view()),
    path('device-option/', views.DeviceOptionView.as_view()),
    path('test-view/', views.ReportFilterView.as_view())
]

urlpatterns += routers.urls