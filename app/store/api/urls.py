
from cgitb import lookup
from django.db import router
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import api_root, DrugViewSet, PrescriptionViewSet

# app_name = 'store'



urlpatterns = format_suffix_patterns(  [
    path("", api_root),
    path("prescriptions/", PrescriptionViewSet.as_view({"get":"list"}), name="prescription-list"),
    path("prescriptions/<str:prescription_slug>/", PrescriptionViewSet.as_view({"get":'retrieve'}), name="prescription-detail"),
    path("prescriptions/<slug:prescription_slug>/drugs/", DrugViewSet.as_view({"get":"list"}), name="drug-list"),
    path("prescriptions/<slug:prescription_slug>/<slug:drug_slug>/", DrugViewSet.as_view({"get":"retrieve"}), name="drug-detail"),
    path("prescriptions/<slug:prescription_slug>/<slug:drug_slug>/images/", DrugViewSet.as_view({"get":"list"}), name="image-list"),
    path("prescriptions/<slug:prescription_slug>/<slug:drug_slug>/<int:pk>", DrugViewSet.as_view({"get":"retrieve"}), name="image-detail"),
    
])

