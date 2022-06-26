from fileinput import filename
import json
import asyncio
import random
import re
from locale import atof, setlocale, LC_NUMERIC
import string
from unittest.mock import call
from urllib import request
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import requests
from django.utils.text import slugify
import urllib
from store.models import Drug, DrugImage, Prescription, Compound, Stock, ProductDetails
from django.core.management.base import BaseCommand, CommandError

def populating(data):

    setlocale(LC_NUMERIC, 'en_IN')

    prescription = Prescription(prescription_name=data["prescription"])
    prescription.save()

    # drug object
    rx = True
    if not data["require rx"]:
        rx = False
    try:
        mrp = atof(data["mrp"])
    except ValueError:
        mrp = 0.00

    try:
        final_price = atof(data["final price"])
    except ValueError:
        final_price = 0.00

    varient = data.pop("drug varient", None)
    if not varient:
        varient=""
    drug = Drug(
        name=data["drug name"],
        varient_type = varient,
        prescription=prescription,
        require_rx=rx,
        mrp=mrp,
        final_price=final_price,

    )

    drug.save()

    # adding compound
    # compound details
    if data["compounds"]:
        compounds_data = data["compounds"].split("+")
        for c in compounds_data:
            # extracting power or concentration info
            compound_power = re.search("[0-9][\s\S]*$", c)
            if compound_power:
                compound_power = compound_power.group()
                compound_name = c.replace(
                    compound_power, "")  # only name to store
            compound_name = c
            compound_power = ''

            compound = Compound(
                name=compound_name,
                power_concent=compound_power
            )

            compound.save()
            drug.compounds.add(compound)

    # adding random number of stock and random data
    for _ in range(0, random.randint(1, 4)):
        """ random number of stock"""

        stock = Stock(
            items=random.choice(range(1, 50)),
            batch_no=' '.join(random.choice(string.ascii_lowercase)
                              for _ in range(10)),
            drug=drug

        )

        stock.save()

    # adding extra product details

    pd = data.pop("product details", None)
    if pd:
        item_weight = pd.pop("Item Weight", '1.0')
        item_weight = re.search("[0-9]+", item_weight)
        if item_weight:
            item_weight = float(item_weight.group())
        else:
            item_weight = 1.00

        net_qty=pd.pop("Net Qty", "1")
        if net_qty.strip():
            net_qty = int(net_qty)
        else:
            net_qty = 1
        
        product_details = ProductDetails(
            drug=drug,
            net_qty=int(pd.pop("Net Qty", "1")),
            item_weight=item_weight,
            ingredient=pd.pop("Ingredient", ""),
            customer_care_email=pd.pop("Customer care email id", ""),
            manufacturer_marketer=pd.pop("Name of Manufacturer/Marketer", ""),
            manufacturer=pd.pop("Name of Manufacturer", ""),
            importer=pd.pop("Name of Importer", ""),
            direction_of_use=pd.pop("Directions to use", "")
        )

        product_details.save()

    # drug image object
    d_images_links = data.pop("drug images", None)

    if d_images_links:
        for image_link in d_images_links:
            url_image = image_link["image link"]
            file_name = url_image.split('/')[-1]
            response = requests.get(url_image, stream=True)
            if response.status_code == 200:
                # img = io.BytesIO(response.content)

                drug_image = DrugImage(

                    image=SimpleUploadedFile(file_name, content=response.content, content_type="image/jpeg"),

                    drug=drug
                )
                # drug_image.image.save(filename, img)
                drug_image.save()


    
class Command(BaseCommand):
    help = 'Populate the database'

    def handle(self, *args, **options):
        with open("./data_json/drug_data.json", "r") as read_file:
            drugs = json.load(read_file)
            i=1
            for drug in drugs:
                self.stdout.write(f"adding drug : {i}")
                populating(drug)
                i+=1
        self.stdout.write(self.style.SUCCESS('Database is populated '))
