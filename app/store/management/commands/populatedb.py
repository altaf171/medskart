import io
import concurrent.futures
import asyncio
import aiohttp
import json
import random
import re
from locale import atof, setlocale, LC_NUMERIC
import string
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand
from store.models import Drug, DrugImage, Prescription, Compound, Stock, ProductDetails


medicine_saved = 1


def get_image_tasks(urls, session):
    tasks = []

    for url in urls:
        file_name = url.split('/')[-1]
        tasks.append(asyncio.create_task(session.get(url, ssl=False)))

    return tasks

    # file_name = url.split('/')[-1]
    # response = requests.get(url, stream=True) #//

    # if response.status_code == 200:
    #     image = DrugImage(
    #         image=SimpleUploadedFile(
    #             file_name, content=response.content, content_type="image/jpeg"),
    #         drug=drug
    #     )

    #     image.save()


async def images(data, drug):
    image_objects = []
    images_details = data.pop("drug images", None)
    if images_details:
        urls = [url["image link"] for url in images_details]
        async with aiohttp.ClientSession() as session:
            # tasks = get_image_tasks(urls, session)
            responses = await asyncio.gather(*get_image_tasks(urls, session))
            # print(responses)
            if responses:
                for response in responses:
                    url = str(response.url)
                    file_name = url.split('/')[-1]
                    buffer = io.BytesIO(await response.read())
                    content = buffer.read()
                    image = DrugImage(
                        image=SimpleUploadedFile(
                            file_name, content=content, content_type="image/jpeg"),
                        drug=drug)
                    image_objects.append(image)

    return image_objects

    # image.save()

    # get_image = partial(imagesave, drug=drug)
    # with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executer:
    #     executer.map(get_image, url_list)


def populating(data):

    setlocale(LC_NUMERIC, 'en_IN')

    prescription = Prescription.objects.get_or_create(
        name=data["prescription"])
    # get_or_ create retuns tuple of query_object and True (if created)
    # next line is used to extract object
    if type(prescription) is tuple:
        prescription = prescription[0]

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
        varient = ""
    drug = Drug.objects.get_or_create(
        name=data["drug name"],
        varient_type=varient,
        prescription=prescription,
        require_rx=rx,
        mrp=mrp,
        final_price=final_price,)[0]

    # drug.save()

    # adding compound
    # compound details
    if data["compounds"]:
        compounds_data = data["compounds"].split("+")
        for compound_name in compounds_data:
            compound = Compound.objects.get_or_create(name=compound_name)
            if isinstance(compound, tuple):
                compound = compound[0]
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

        net_qty = pd.pop("Net Qty", "1")
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
        # images(data=data, drug=drug)
        image_objects = asyncio.run(images(data=data, drug=drug))
        for image in image_objects:
            image.save()
        # print(image_objects)

        # for image_detail in images_details:
        #     imagesave(image_detail,drug)

        global medicine_saved
        print(f'medicine saved: {medicine_saved}')
        medicine_saved += 1


class Command(BaseCommand):
    help = 'Populate the database'

    def add_arguments(self, parser) -> None:
        parser.add_argument('--items',
                            type=int,
                            help="Number medicine you want to add"
                            )

    def handle(self, *args, **options):
        with open("./data_json/drug_data.json", "r") as read_file:
            drugs = json.load(read_file)
            self.stdout.write(f"total medicine : {len(drugs)}")
            num = options["items"]
            if num and num < len(drugs) and num > 0:
                drugs = drugs[0:num]

            self.stdout.write(f"you selected : {len(drugs)}")
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executer:
                executer.map(populating, drugs)

            # for drug in drugs:
            #     populating(drug)

        self.stdout.write(self.style.SUCCESS('Database is populated '))
