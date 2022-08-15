from django.contrib import admin

from store.models import (
    Banner,
    Drug,
    NavigationLink,
    Prescription,
    Stock
)

admin.site.register(Drug)
admin.site.register(Prescription)
admin.site.register(Stock)
#----ui-------
admin.site.register(NavigationLink)
admin.site.register(Banner)

