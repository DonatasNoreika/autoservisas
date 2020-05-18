from django.contrib import admin

# Register your models here.
from .models import Paslauga, Automobilio_modelis, Paslaugos_kaina, Automobilis, Uzsakymas, UzsakymoEilute

admin.site.register(Paslauga)
admin.site.register(Automobilio_modelis)
admin.site.register(Paslaugos_kaina)
admin.site.register(Automobilis)
admin.site.register(Uzsakymas)
admin.site.register(UzsakymoEilute)