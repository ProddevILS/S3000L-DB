from django.contrib import admin
from .models import *
for model in list(globals().values()):
    if getattr(model, '__module__', '').endswith('.models'):
        try: admin.site.register(model)
        except admin.sites.AlreadyRegistered: pass
