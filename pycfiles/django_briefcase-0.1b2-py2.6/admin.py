# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\briefcase\admin.py
# Compiled at: 2010-10-14 13:12:52
from django.contrib import admin
from briefcase.models import DocumentStatus, DocumentType, Document

class DocumentStatusAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


class DocumentTypeAdmin(admin.ModelAdmin):
    pass


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'type', 'status', 'added_by', 'added_at', 'updated_at')
    list_display_links = ('__unicode__', )
    list_filter = ('type', 'status')

    def queryset(self, request):
        """
        Forces a JOIN to DocumentType and User models.
        
        Cannot be achieved by setting list_select_related=True, because
        the foreign key fields have null=True. We have an OUTER JOIN here.
        """
        qs = super(DocumentAdmin, self).queryset(request)
        return qs.select_related('type', 'added_by')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.added_by = request.user
        super(DocumentAdmin, self).save_model(request, obj, form, change)


admin.site.register(DocumentStatus, DocumentStatusAdmin)
admin.site.register(DocumentType, DocumentTypeAdmin)
admin.site.register(Document, DocumentAdmin)