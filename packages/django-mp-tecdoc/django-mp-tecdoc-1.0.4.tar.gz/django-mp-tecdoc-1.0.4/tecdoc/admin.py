
from django.contrib import admin

from tecdoc.models import Supplier


admin.site.register(
    Supplier,
    list_display=['description', 'matchcode'],
    search_fields=['description', 'matchcode']
)
