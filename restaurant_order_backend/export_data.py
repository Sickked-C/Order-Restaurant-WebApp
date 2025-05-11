import os
import django
import sys
import io
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurant_order_backend.settings")
django.setup()

# Đảm bảo output là UTF-8
with io.open("data.json", "w", encoding="utf-8") as f:
    call_command("dumpdata", exclude=["contenttypes", "auth.Permission"], stdout=f)
