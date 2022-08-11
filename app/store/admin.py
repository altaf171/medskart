from django.contrib import admin

from store.models import (
    Drug,
    NavigationLink,
    Prescription,
    Stock
)

admin.site.register(Drug)
admin.site.register(Prescription)
admin.site.register(Stock)
admin.site.register(NavigationLink)
