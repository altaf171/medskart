

from django.shortcuts import get_object_or_404
from rest_framework.reverse import reverse as drf_reverse
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import action
from yaml import serialize
from store.models import Prescription, Drug, DrugImage
from .serializers import PrescriptionModelSerializer, DrugModelSerializer, DrugImageModelSerializer


@api_view(['GET'])
def api_root(request, format=None):
    prescription = Prescription.objects.first()
    pres_slug = prescription.prescription_slug
    drug = Drug.objects.filter(prescription__prescription_slug=pres_slug).first()
    drug_slug = drug.drug_slug
    return Response({
        'Prescriptions': drf_reverse("prescription-list", request=request, format=format),
        # "(👉ﾟヮﾟ)👉  example link of nested": " first medicine of first prescription *_*(((o(*ﾟ▽ﾟ*)o)))",
        'Prescription Detail': drf_reverse("prescription-detail", request=request, args=[pres_slug, ], format=format),
        'Drugs': drf_reverse("drug-list", request=request, args=[pres_slug], format=format),
        'Drug Detail': drf_reverse("drug-detail", request=request, args=[pres_slug, drug_slug], format=format),
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
            queryset, prescription_slug=prescription_slug)
        serializer = PrescriptionModelSerializer(
            prescription, context={'request': request})
        return Response(serializer.data)


class DrugViewSet(viewsets.ViewSet):
    def list(self, request, prescription_slug=None):
        queryset = Drug.objects.filter(
            prescription__prescription_slug=prescription_slug)
        serializer = DrugModelSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, drug_slug=None, prescription_slug=None):

        queryset = Drug.objects.filter(
            prescription__prescription_slug=prescription_slug)
        drug = get_object_or_404(queryset, drug_slug=drug_slug)
        serializer = DrugModelSerializer(drug)
        return Response(serializer.data)


class DrugImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DrugImage.objects.all()
    serializer_class = DrugImageModelSerializer


# class isAdminUserOrReadOnly(permissions.IsAdminUser):
#     """
#     custom permission only admin can add or edit drug data

#     """
#     def has_permission(self, request, view):

#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return super().has_permission(request, view)
