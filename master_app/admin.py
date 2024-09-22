from django.contrib import admin

# Register your models here.


from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db import models

# from cked.widgets import CKEditorWidget
from ckeditor.widgets import CKEditorWidget


class FlatPageCustom(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageCustom)


from .models import *



class DocumentLogs(admin.TabularInline):
    model = DocumentLogs
    # fields = ['timestamp','public_ip_address', 'user_agent' ]
    readonly_fields = ['timestamp', 'public_ip_address', 'user_agent']
    # extra = 0
    can_delete = False
    extra = 0
    max_num=0


class DocumentAdmin(admin.ModelAdmin):
    inlines = [
        DocumentLogs,
    ]
    list_display = [
        "name",
        "ip_address",
        "uploaded_at",
        "expires_at",
        "short_url",
        "user_agent",
    ]


class UserLogsAdmin(admin.ModelAdmin):
    list_display = [
        "timestamp",
        "public_ip_address",
        "user_agent"
    ]

class AdminLogsAdmin(admin.ModelAdmin):
    list_display = [
        "timestamp",
        "public_ip_address",
        "user_agent"
    ]


class ReportsAdmin(admin.ModelAdmin):
    list_display = [
        "url",
        "email"
    ]

admin.site.register(Document, DocumentAdmin)
admin.site.register(UserLogs, UserLogsAdmin)
admin.site.register(AdminLogs, AdminLogsAdmin)
admin.site.register(Reports, ReportsAdmin)


