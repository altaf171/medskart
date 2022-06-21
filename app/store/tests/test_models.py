from django.test import TestCase
from store.models import Drug, Compound, Stock


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
            compound_name="paracetamol",
            compound_power="500"

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
        ensure that adding stock detail (no of strip or bottle or boxes and
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
            stock=20,
            batch_no="ap00476",
            drug=drug
        )
        stock.save()

        self.assertEqual(drug.stock_set.all()[0].stock, 20)