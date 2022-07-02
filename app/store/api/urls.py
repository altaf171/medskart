
from django.urls import path, include
from rest_framework import routers
from .views import PrescriptionViewSet, DrugRetrieveViewSet, DrugListViewSet, api_root

# app_name = 'store'

# router = routers.DefaultRouter()
# router.register('', DrugViewSet, basename='drug')

urlpatterns = [
    path("",api_root),
    # path('drugs/', DrugViewSet.as_view(), name='drug-list'),
    path("prescriptions/", PrescriptionViewSet.as_view({"get":"list"}), name="prescription-list"),
    path("prescriptions/<slug:slug>/", PrescriptionViewSet.as_view({"get":'retrieve'}), name="prescription-detail"),
    path("prescriptions/medicines/", DrugListViewSet.as_view({"get":"list"}), name='drug-list'),
    path('prescriptions/medicines/<slug:slug>/',DrugRetrieveViewSet.as_view({'get':'retrieve'}), name='drug-detail'),

]
