from django.contrib import admin
from .models import CallbackRequest

@admin.register(CallbackRequest)
class CallbackRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'preferred_time', 'created_at', 'processed')
    list_filter = ('created_at', 'preferred_time', 'processed')
    search_fields = ('name', 'phone', 'message')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'phone', 'preferred_time', 'message')
        }),
        ('Статус', {
            'fields': ('processed', 'created_at')
        }),
    )
    
    actions = ['mark_as_processed']
    
    def mark_as_processed(self, request, queryset):
        queryset.update(processed=True)
    mark_as_processed.short_description = "Отметить выбранные заявки как обработанные"