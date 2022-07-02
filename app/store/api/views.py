

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets, permissions, mixins
from rest_framework.decorators import api_view
from store.models import Prescription, Drug
from .serializers import PrescriptionModelSerializer, DrugModelSerializer, DrugImageModelSerializer



@api_view(['GET'])
def api_root(request):
    """return list of api end-point """
    return Response({
        'user-profile': reverse('user:me', request=request),
        'priscriptions': reverse('prescription-list', request=request),
        'medicines': reverse('drug-list', request=request)
    })


class PrescriptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionModelSerializer
    permission_classes = []
    lookup_field = 'slug'


# hyperlinkedmodelserializer would not work with generics 
# so i am using mixins with generic viewset
class DrugListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Get the list of drugs

    """
    queryset = Drug.objects.all()
    serializer_class = DrugModelSerializer
    lookup_field = 'slug'


class DrugRetrieveViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    retrieve drug details

    """
    queryset = Drug.objects.all()
    serializer_class = DrugModelSerializer
    lookup_field = 'slug'




# class isAdminUserOrReadOnly(permissions.IsAdminUser):
#     """
#     custom permission only admin can add or edit drug data

#     """
#     def has_permission(self, request, view):

#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return super().has_permission(request, view)
