from unicodedata import name
from django.utils.text import slugify
from djmoney.models.fields import MoneyField
from django.db import models
from django.utils.translation import gettext as _
# from django.urls import reverse
from rest_framework.reverse import reverse


class Prescription(models.Model):
    """ for what drug is prescribed """
    name = models.CharField(_("Prescription name"), max_length=50, unique=True)
    slug = models.SlugField(_("Prescription slug"))

    class Meta:
        verbose_name = _("Prescription")
        verbose_name_plural = _("Prescriptions")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("prescription-detail", kwargs={"prescription_slug": self.slug})


class Compound(models.Model):
    """ 
    model to store info about medicine chemical compound name, power and concentration  

    """

    name = models.CharField(_("Compund Name"), max_length=50, unique=True)
    slug = models.SlugField(_("Compound Slug"), blank=True)

    class Meta:
        verbose_name = _("Compound")
        verbose_name_plural = _("Compounds")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Drug(models.Model):
    """ model class for medicine  """
    name = models.CharField(_("medicine name"), max_length=50)

    # varient type determines that drug is pill, capsule or syrup type
    varient_type = models.CharField(_("varient type"), max_length=50)

    compounds = models.ManyToManyField(
        "store.Compound", verbose_name=_("compounds"))

    prescription = models.ForeignKey(Prescription, verbose_name=_(
        "prescription"), on_delete=models.CASCADE, null=True, blank=True)

    require_rx = models.BooleanField(_("is Rx required"), default=False)

    mrp = MoneyField(_("mrp"), max_digits=19,
                     decimal_places=4, default_currency='INR')
    final_price = MoneyField(
        _("final price"), max_digits=19, decimal_places=4, default_currency='INR')

    slug = models.SlugField(_("drug slug"))

    class Meta:
        unique_together = (('name', 'varient_type'),)
        verbose_name = _("drug")
        verbose_name_plural = _("drugs")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("drug-detail", kwargs={"prescription_slug": self.prescription.slug, "drug_slug": self.slug})


class DrugImage(models.Model):
    """ model to store medicine's images """
    image = models.ImageField(_("image"), upload_to="drug/images")
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Drug Image")
        verbose_name_plural = _("Drug Images")

    def __str__(self):
        return self.image.url

    def get_absolute_url(self):
        return reverse("image-detail", kwargs={"pk": self.pk})


class Stock(models.Model):
    """
    stores no of drugs with batch no
    a drug might have diffrent batch no in diffrent quantity 

    """
    items = models.IntegerField(_("items"), default=0)
    batch_no = models.CharField(_("batch no"), max_length=30)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("stock")
        verbose_name_plural = _("stocks")

    def __str__(self):
        return str(self.items) + " " + self.batch_no


class ProductDetails(models.Model):
    """
    (。・ω・。) Optional (。・ω・。)

    some extra detail about drug 

    """
    drug = models.OneToOneField(
        Drug, on_delete=models.CASCADE, primary_key=True)

    net_qty = models.IntegerField(_("net quantity"), default=1)
    item_weight = models.FloatField(
        _("Item Weight"), max_length=10)

    ingredient = models.CharField(_("Ingredient"), max_length=50)

    customer_care_email = models.EmailField(
        _("customer care email"), max_length=254, default='')
    manufacturer_marketer = models.CharField(
        _("manufacturer / marketer"), max_length=50)
    manufacturer = models.CharField(
        _("manufacturer"), max_length=50, default='')
    importer = models.CharField(
        _("drug importer"), max_length=50, default='')

    direction_of_use = models.TextField(
        _("Direction of use"), default='')

    class Meta:
        verbose_name = _("Product_details")
        verbose_name_plural = _("Product_details")

    def __str__(self):
        return str(self.net_qty) + " " + str(self.item_weight) + " " + self.ingredient


# models for ui elements

class NavigationLink(models.Model):
    """
    store links for second navigation

    """
    text = models.CharField(_("link text "), max_length=20)
    link = models.CharField(_("link"), max_length=100)
    
    class Meta:
        verbose_name = _("NavigationLink")
        verbose_name_plural = _("NavigationLinks")

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("NavigationLink_detail", kwargs={"pk": self.pk})
