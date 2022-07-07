
from pyexpat import model
from rest_framework import serializers
from .utils import serializer_utils
from store.models import (
    Compound,
    Prescription,
    Drug,
    DrugImage,
)


class DrugImageModelSerializer(serializers.ModelSerializer):
    # image_url = serializers.SerializerMethodField()
    image = serializers.ImageField(
        max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = DrugImage
        fields = ["image", ]


class DrugModelSerializer(serializers.ModelSerializer):
    url = serializer_utils.ParameterisedHyperlinkedIdentityField(
        view_name="drug-detail",
        lookup_fields=(('prescription.slug', 'prescription_slug'),
                       ('slug', 'medicine_slug')),

    )

    images = DrugImageModelSerializer(
        source='drugimage_set',
        many=True,
        read_only=True,
    )

    compounds = serializers.StringRelatedField(many=True)

    class Meta:
        model = Drug
        fields = ['url', 'images', 'name', 'compounds' ]


class PrescriptionModelSerializer(serializers.ModelSerializer):
    medicines = DrugModelSerializer(
        source='drug_set', many=True, read_only=True)

    url = serializer_utils.ParameterisedHyperlinkedIdentityField(
        view_name="prescription-detail",
        lookup_fields=(('slug', 'prescription_slug'),)

    )

    class Meta:
        model = Prescription
        fields = ['url', 'name', 'medicines']


class CompoundModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compound
        fields = ['name']
