from django.contrib import admin
from .models import FinancialProduct, AdditionalProduct, WishList, Option, AdditionalOption

# Register your models here.
class FinancialProductAdmin(admin.ModelAdmin):
    pass

class WishListAdmin(admin.ModelAdmin):
    pass

class OptionAdmin(admin.ModelAdmin):
    pass


admin.site.register(FinancialProduct, FinancialProductAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(WishList, WishListAdmin)