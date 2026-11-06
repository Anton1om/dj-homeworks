from django.contrib import admin

from .models import Sensor, Measurement


class MeasurementInline(admin.TabularInline):
    model = Measurement
    extra = 0
    fields = ('temperature', 'image', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    can_delete = True
    show_change_link = True


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name', 'description')
    ordering = ('id',)

    inlines = [MeasurementInline]
