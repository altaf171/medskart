from typing import final
from djmoney.models.fields import MoneyField
from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse

# Create your models here.

class Prescription(models.Model):
    """ for what drug is prescribed """
    prescription_name = models.CharField(_("Prescription name"), max_length=50)

    class Meta:
        verbose_name = _("Prescription")
        verbose_name_plural = _("Prescriptions")

    def __str__(self):
        return self.prescription_name

class Compound(models.Model):
    """ model to store info about medicine chemical compound  """

    compound_name = models.CharField(_("Compund Name"), max_length=50)
    compound_power = models.CharField(_("varient power"), max_length=50)

    class Meta:
        verbose_name = _("Compound")
        verbose_name_plural = _("Compounds")

    def __str__(self):
        return self.compound_name



class Drug(models.Model):
    """ model class for medicine  """
    name = models.CharField(_("medicine name"), max_length=50)

    # varient type determines that drug is pill, capsule or syrup type
    varient_type = models.CharField(_("varient type"), max_length=50)

    compounds = models.ManyToManyField(
        "store.Compound", verbose_name=_("compounds"))
        
    prescription = models.ForeignKey(Prescription, verbose_name=_(
        "prescription"), on_delete=models.CASCADE, null=True, blank=True)

    require_Rx = models.BooleanField(_("is Rx required"), default=False)

    mrp = MoneyField(_("mrp"), max_digits=19,
                     decimal_places=4, default_currency='INR')
    final_price = MoneyField(
        _("final price"), max_digits=19, decimal_places=4, default_currency='INR')

    class Meta:
        verbose_name = _("drug")
        verbose_name_plural = _("drugs")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("drug_detail", kwargs={"pk": self.pk})


class DrugImage(models.Model):
    """ model to store medicine's images """
    image = models.ImageField(_("image"), upload_to="drug/images")
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Drug Image")
        verbose_name_plural = _("Drug Images")




class Stock(models.Model):
    """
    stores no of drugs with batch no
    a drug might have diffrent batch no in diffrent quantity 

    """
    stock = models.IntegerField(_("stock"), default=0)
    batch_no = models.CharField(_("batch no"), max_length=30)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("stock")
        verbose_name_plural = _("stocks")

    def __str__(self):
        return str(self.stock) + " " + self.batch_no

    def get_absolute_url(self):
        return reverse("stock_detail", kwargs={"pk": self.pk})
