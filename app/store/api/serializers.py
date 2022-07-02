from asyncore import read
from cgitb import lookup
from importlib.metadata import files
from pyexpat import model
from rest_framework import serializers
from store.models import Prescription, Drug, DrugImage


class DrugImageModelSerializer(serializers.ModelSerializer):
    # image_url = serializers.SerializerMethodField()
    image = serializers.ImageField(
        max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = DrugImage
        fields = ['image']


class DrugModelSerializer(serializers.HyperlinkedModelSerializer):
    images = DrugImageModelSerializer(
        source='drugimage_set', many=True, read_only=True)

    # images = serializers.HyperlinkedRelatedField(
    #     source="drugimage_set",
    #     many=True,
    #     view_name=
    # )

    class Meta:
        model = Drug
        fields = ['url', 'images', 'name']
        # fields = '__all__'
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class PrescriptionModelSerializer(serializers.HyperlinkedModelSerializer):
    # medicines =  DrugModelSerializer(source="drug_set", many=True, read_only=True)
    medicines = serializers.HyperlinkedRelatedField(source="drug_set",
                                                    view_name='drug-detail',
                                                    lookup_field='slug',
                                                    many=True,
                                                    read_only=True
                                                    )

    class Meta:
        model = Prescription
        fields = ['url', 'prescription_name', 'medicines']
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}
