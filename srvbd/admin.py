from django.contrib import admin
from .models import *
from django.contrib.auth.models import User


admin.site.register(Person)
admin.site.register(SparPart)
admin.site.register(Incoming)
admin.site.register(DetailInIncomList)
admin.site.register(Detail)
admin.site.register(MaterialSaleObject)
# admin.site.register(User)
admin.site.register(TypeSparPart)
admin.site.register(TypeAppliances)
admin.site.register(Manufacturer)
admin.site.register(Shipper)
admin.site.register(DeviceUnderRepair)
admin.site.register(Device)
admin.site.register(SalesPersonInvoice)
admin.site.register(ExchangeRates)
admin.site.register(Markup)
