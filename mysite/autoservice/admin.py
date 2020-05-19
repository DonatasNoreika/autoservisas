from django.contrib import admin

# Register your models here.
from .models import Paslauga, Automobilio_modelis, Paslaugos_kaina, Automobilis, Uzsakymas, UzsakymoEilute

class UzsakymoEilutesInline(admin.TabularInline):
    model = UzsakymoEilute

class UzsakymasAdmin(admin.ModelAdmin):
    inlines = [UzsakymoEilutesInline]

admin.site.register(Paslauga)
admin.site.register(Automobilio_modelis)
admin.site.register(Paslaugos_kaina)
admin.site.register(Automobilis)
admin.site.register(Uzsakymas, UzsakymasAdmin)
admin.site.register(UzsakymoEilute)