from . import views

from rest_framework import routers

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register('register', views.RegisterViewSet)
router.register('login', views.LoginViewSet, basename='login')
router.register('production', views.ProductionViewSet)
router.register('machine', views.MachineViewSet)
router.register('part', views.PartViewSet)
router.register('hourly', views.HourlyProductionViewSet)
router.register('changelog', views.ChangeLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/', include(router.urls)),
    path('api/api-auth/', include('rest_framework.urls', namespace='pro_api')),
] 