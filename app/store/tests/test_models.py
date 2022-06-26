from email.mime import image
import io
from django.test import TestCase
from store.models import Drug, Compound, DrugImage, Stock, ProductDetails

from PIL import Image
import requests

class DrugModelTest(TestCase):
    def test_drug_create(self):
        """
        test that new drug creation is successfull 

        """
        drug = Drug(
            name="dolo 500",
            varient_type="pill 10 strip",
            mrp=20.0,
            final_price=18.00

        )

        drug.save()
        self.assertEqual(drug.name, "dolo 500")

    def test_creating_new_compound(self):
        """
        test that creating new compound is successfull

        """
        compound = Compound(
            name="paracetamol",
            power_content="500"

        )
        compound.save()
        # comp_from_db = Compound.objects.all()
        # print(comp_from_db[0])
        self.assertEqual(compound.compound_name, "paracetamol")

    def test_compound_and_drug(self):
        """
        test creating drug with compound name

        """
        compound = Compound(
            compound_name="paracetamol",
            compound_power="500"

        )
        compound.save()

        drug = Drug(
            name="dolo 500",
            varient_type="pill 10 strip",
            mrp=20.0,
            final_price=18.00,
        )

        drug.save()
        drug.compounds.add(compound)
        # print(drug.compounds.all()[0].compound_name)
        self.assertEqual(drug.name, "dolo 500")
        self.assertEqual(drug.compounds.all()[0].compound_name, "paracetamol")

    def test_stock_drug(self):
        """
        Ensure that adding stock detail (no of strip or bottle or boxes and
        batch no ) to drug works

        """
        drug = Drug(
            name="dolo 500",
            varient_type="pill 10 strip",
            mrp=20.0,
            final_price=18.00,
        )
        drug.save()

        stock = Stock(
            items=20,
            batch_no="ap00476",
            drug=drug
        )
        stock.save()

        self.assertEqual(drug.stock_set.all()[0].items, 20)

    def test_product_details(self):
        """
        Ensure that creation of product details is successfull
        for drug

        """
        drug = Drug(
            name="Jilazo 100mg Injection 5ml",
            varient_type="",
            mrp=3045.00,
            final_price=2436.00,
        )
        drug.save()

        product_details = ProductDetails(
            drug=drug,
            net_qty=1,
            item_weight=40,
            ingredient="IRON ISOMALTOSIDE 100MG",
            customer_care_email="dsrm@lupin.com",
            manufacturer_marketer="Lupin Ltd",
            manufacturer="Pharmacosmos A/S",
            importer="Lupin Ltd",
            direction_of_use="This medicine will be administered by a doctor or nurse."

        )

        product_details.save()

        self.assertTrue(hasattr(drug, "productdetails"))
    
    def test_drug_image(self):
        drug = Drug(
            name="Jilazo 100mg Injection 5ml",
            varient_type="",
            mrp=3045.00,
            final_price=2436.00,
        )
        drug.save()
       
        url = "https://www.netmeds.com/images/product-v1/600x600/838583/jilazo_100mg_injection_5ml_0_0.jpg"

        #im = Image.open(requests.get(url, stream=True).raw)
        im = requests.get(url, stream=True)
        drug_image = DrugImage(
            image = Image.open(io.BytesIO(im.content)),
            drug = drug
        )
        drug_image.save()
        self.assertTrue(hasattr(drug,"drugimage"))
