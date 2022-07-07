
from rest_framework import serializers
from .utils import serializer_utils
from store.models import (
    Compound,
    Prescription,
    Drug,
    DrugImage,
    ProductDetails,
    Stock,
)


class ProductDetailsModelSeializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetails
        fields = '__all__'

class StockModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock




class DrugImageModelSerializer(serializers.ModelSerializer):
    """
    Serializes DrugImage model gives image's url

    """
    image = serializers.ImageField(
        max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = DrugImage
        fields = ["image", ]


class DrugModelSerializer(serializers.ModelSerializer):
    """
    
    Serializes Drug model and give all info about medicine

    """

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

    details  =ProductDetailsModelSeializer(source='productdetails')

    in_stock = serializers.SerializerMethodField(method_name="get_stock")

    class Meta:
        model = Drug
        fields = ['url', 'images', 'name', 'compounds', 'details', 'in_stock']
    
    def get_stock(self, obj):
        """
        calculate that is item in stock or not

        """
        items=0
        if obj.stock_set.all():
            for stock in obj.stock_set.all():
                items += stock.items
        
        if items:
            return True
        return False

        # return {"items": items}



class DrugInlineModelSerializer(serializers.ModelSerializer):
    """
    This Serializer is used inside PrescriptionModelSerializer
    to display limited info of drug

    """
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
        fields = ['url', 'images', 'name', 'compounds']



class PrescriptionModelSerializer(serializers.ModelSerializer):
    medicines = DrugInlineModelSerializer(
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
