from django.contrib import admin
from django.utils.html import format_html
from .models import Product, NetworkNode


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'release_date')
    list_filter = ('release_date',)
    search_fields = ('name', 'model')


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'node_type', 'city', 'debt', 'supplier_link', 'created_at')
    list_filter = ('city', 'country', 'node_type')
    search_fields = ('name', 'email', 'city')
    actions = ['clear_debt']

    def supplier_link(self, obj):
        if obj.supplier:
            url = f'/admin/electronics/networknode/{obj.supplier.id}/change/'
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return "-"

    supplier_link.short_description = 'Поставщик'

    def clear_debt(self, request, queryset):
        updated = queryset.update(debt=0)
        self.message_user(request, f'Задолженность очищена у {updated} объектов')

    clear_debt.short_description = 'Очистить задолженность перед поставщиком'
