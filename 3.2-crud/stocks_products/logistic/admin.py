from django.contrib import admin
from .models import Product, Stock, StockProduct


class StockProductInline(admin.TabularInline):
    model = StockProduct
    extra = 1


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    inlines = [StockProductInline]


admin.site.register(Product)