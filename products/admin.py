import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import Brand, Category, Product

"""
    Registrando os models no Django Admin.
    Isso permite gerenciar "Brand", "Category" e "Product" pela interface administrativa
"""

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display  = ('name', 'is_active', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter   = ('is_active',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'is_active', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter   = ('is_active',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ('title', 'brand', 'category', 'price', 'is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'brand__name', 'category__name') # "__" para acessar campos das tabelas relacionadas.
    list_filter   = ('is_active', 'brand', 'category')
    actions       = ['export_to_csv']

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products.csv"'

        writer = csv.writer(response)
        writer.writerow(['titulo', 'marca', 'categoria', 'preço', 'ativo', 'descrição', 'criado em', 'atualizado em'])

        for product in queryset:
            writer.writerow([
                product.title,
                product.brand.name,
                product.category.name,
                product.price,
                product.is_active,
                product.description,
                product.created_at,
                product.updated_at
            ])

        return response

    export_to_csv.short_description = 'Exportar para CSV' # type: ignore
