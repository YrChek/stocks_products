from django.contrib import admin

from logistic.models import Product, Stock, StockProduct


class StockProductInLine(admin.TabularInline):
    model = StockProduct
    extra = 0


@admin.register(Product)
class ProduktAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    inlines = [StockProductInLine]


@admin.register(StockProduct)
class StockProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product']
