from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    api_root,
    DrugViewSet,
    DrugImageViewSet,
    PrescriptionViewSet,
    CompoundViewSet,
)

router = routers.DefaultRouter()

router.register('compounds', CompoundViewSet, basename='compound')
# app_name = 'store'

prescription_urls = [
    path("prescriptions/",
         PrescriptionViewSet.as_view({"get": "list"}), name="prescription-list"),
    path("prescriptions/<str:prescription_slug>/",
         PrescriptionViewSet.as_view({"get": 'retrieve'}), name="prescription-detail"),
    path("prescriptions/<slug:prescription_slug>/medicines/",
         DrugViewSet.as_view({"get": "list"}), name="drug-list"),
    path("prescriptions/<slug:prescription_slug>/medicines/<medicine_slug>/",
         DrugViewSet.as_view({"get": "retrieve"}), name="drug-detail"),
]



urlpatterns = [
    path("", api_root),
    path("", include(prescription_urls)),
    path("", include(router.urls)),

    # path("prescriptions/<slug:prescription_slug>/drugs/<medicine_slug>/images/", DrugViewSet.as_view({"get":"list"}), name="image-list"),
    # path("medicines/images/<int:pk>/",
    #      DrugImageViewSet.as_view({"get": "retrieve"}), name="image-detail"),


]
