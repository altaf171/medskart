
from cgitb import lookup
from rest_framework import serializers
from store.models import Prescription, Drug, DrugImage


class DrugImageModelSerializer(serializers.ModelSerializer):
    # image_url = serializers.SerializerMethodField()
    image = serializers.ImageField(
        max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = DrugImage
        fields = ['image']


class DrugModelSerializer(serializers.ModelSerializer):
    images = DrugImageModelSerializer(
        source='drugimage_set', many=True, read_only=True)
    # images = serializers.HyperlinkedIdentityField(
    #     source='drugimage_set', many=True,
    #     view_name='image-detail'
    #     )

    # url = serializers.HyperlinkedIdentityField(
    #     view_name="drug-detail",
    #     lookup_field="drug_slug",
    # )

    class Meta:
        model = Drug
        fields = [ 'images', 'drug_slug', 'name']
        extra_kwargs = {'url': {'lookup_field': 'drug_slug'}, }


class PrescriptionModelSerializer(serializers.ModelSerializer):
    medicines = DrugModelSerializer(
        source='drug_set', many=True, read_only=True)

    # medicines = serializers.HyperlinkedRelatedField(
    #     source="drug_set",
    #     view_name="drug-detail",
    #     many=True,
    #     read_only = True,

    # )

    # url = serializers.HyperlinkedIdentityField(
    #     view_name="prescription-detail",
    #     lookup_field="prescription_slug",
    # )

    class Meta:
        model = Prescription
        # fields = ['url', 'id', 'prescription_name', 'slug', 'medicines']
        fields = ['id', 'prescription_name',
                  'prescription_slug', 'medicines']

        # lookup_field="slug"
        # extra_kwargs = {'url': {'lookup_field': 'prescription_slug'}}


# medicines = serializers.HyperlinkedRelatedField(
#         source="drug_set", view_name='prescription-drugs-detail',
#         lookup_field='slug', many=True, read_only=True)
        # lookup_field = 'slug'
        # extra_kwargs = {'url': {'lookup_field': 'slug'}}
