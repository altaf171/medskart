
from django.urls import reverse
from django.db import models
from django.utils.translation import gettext as _

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

# ----------  banner silde ----------

class Banner(models.Model):
    """
    banner image for slide and their link

    """
    image = models.ImageField(_("Banner Image"), upload_to="banner-images/", height_field=None, width_field=None, max_length=None)
    link = models.CharField(_("Banner link"), max_length=80)
    class Meta:
        verbose_name = _("Banner")
        verbose_name_plural = _("Banners")

    def __str__(self):
        return self.link

    def get_absolute_url(self):
        return reverse("Banner_detail", kwargs={"pk": self.pk})
