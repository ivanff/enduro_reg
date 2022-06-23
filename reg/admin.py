from django.contrib import admin

from reg.models import Reg


@admin.register(Reg)
class RegAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'competition', 'number', 'fio', 'klass', 'city', 'team', 'bike', 'paid', 'created'
    )
    search_fields = (
        'number',
        'fio',
    )
    list_filter = (
        'competition',
        'klass',
    )