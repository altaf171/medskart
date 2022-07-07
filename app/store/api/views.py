

from django.shortcuts import get_object_or_404
from rest_framework.reverse import reverse as drf_reverse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Prescription, Drug, DrugImage, Compound
from .serializers import (
    PrescriptionModelSerializer, 
    DrugModelSerializer, 
    DrugImageModelSerializer,
    CompoundModelSerializer,
    )


@api_view(['GET'])
def api_root(request, format=None):
    """
    API ROOT 
    (❁´◡`❁) 
    Shows available API endpoints

    """
    prescription = Prescription.objects.first()
    prescription_url= "prescription data is not awailable"
    if prescription:
        prescription_url  = drf_reverse("prescription-detail", request=request, args=[prescription.slug, ], format=format)

    drug = Drug.objects.all()
    drug_list_url = " medicine data is not available"
    drug_url = " medicine data is not available"
    if drug:
        drug = drug.filter(prescription__slug=prescription.slug).first()
        drug_list_url = drf_reverse("drug-list", request=request, args=[prescription.slug], format=format)
        drug_url = drf_reverse("drug-detail", request=request, args=[prescription.slug, drug.slug], format=format)
        

    return Response({
        'Prescriptions': drf_reverse("prescription-list", request=request, format=format),
        # "(👉ﾟヮﾟ)👉  example link of nested": " first medicine of first prescription *_*(((o(*ﾟ▽ﾟ*)o)))",
        'Prescription Detail': prescription_url,
        'Medicines': drug_list_url,
        'Medicine Detail': drug_url,
    })


class PrescriptionViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Prescription.objects.all()
        serializer = PrescriptionModelSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, prescription_slug=None):
        queryset = Prescription.objects.all()
        prescription = get_object_or_404(
            queryset, slug=prescription_slug)
        serializer = PrescriptionModelSerializer(
            prescription, context={'request': request})
        return Response(serializer.data)


class DrugViewSet(viewsets.ViewSet):
    def list(self, request, prescription_slug=None):
        queryset = Drug.objects.filter(
            prescription__slug=prescription_slug)
        serializer = DrugModelSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, medicine_slug=None, prescription_slug=None):

        queryset = Drug.objects.filter(
            prescription__slug=prescription_slug)
        drug = get_object_or_404(queryset, slug=medicine_slug)
        serializer = DrugModelSerializer(drug, context={'request': request})
        return Response(serializer.data)


class DrugImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DrugImage.objects.all()
    serializer_class = DrugImageModelSerializer


class CompoundViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Compound.objects.all()
    serializer_class = CompoundModelSerializer
   





# class isAdminUserOrReadOnly(permissions.IsAdminUser):
#     """
#     custom permission only admin can add or edit drug data

#     """
#     def has_permission(self, request, view):

#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return super().has_permission(request, view)
