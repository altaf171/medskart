from django.contrib import admin

from store.models import (
    Drug,
    Prescription,
    Stock
)

from .ui_models import(
    NavigationLink,
    Banner,
)
admin.site.register(Drug)
admin.site.register(Prescription)
admin.site.register(Stock)
#----ui-------
admin.site.register(NavigationLink)
admin.site.register(Banner)

