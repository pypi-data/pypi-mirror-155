from django.contrib import admin
from activity.models import Process
from activity.models import Activity


@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    list_display = ['id', 'process_key', 'process_type_slug', 'internal_key', 'status']

    search_fields = [
        'process_key',
        'internal_key',
    ]


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['activity_id', 'process', 'from_template_activity_slug']
    raw_id_fields = ['process']

    search_fields = [
        'activity_id',
        'process__process_key',
        'process__internal_key',
        'from_template_activity_slug',
    ]
