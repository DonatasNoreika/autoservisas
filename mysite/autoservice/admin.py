from django.contrib import admin

# Register your models here.
from .models import Paslauga, Automobilio_modelis, Paslaugos_kaina, Automobilis, Uzsakymas, UzsakymoEilute, UzsakymoKomentaras, Profilis


class UzsakymoEilutesInline(admin.TabularInline):
    model = UzsakymoEilute


class UzsakymasAdmin(admin.ModelAdmin):
    list_display = ('automobilis_id', 'klientas_id', 'grazinimo_laikas', 'suma')
    inlines = [UzsakymoEilutesInline]


class AutomobilisAdmin(admin.ModelAdmin):
    list_display = ('savininkas', 'automobilio_modelis_id', 'valstybinis_numeris', 'vin_kodas')
    list_filter = ('savininkas', 'automobilio_modelis_id')
    search_fields = ('valstybinis_numeris', 'vin_kodas')


class PaslaugosKainaAdmin(admin.ModelAdmin):
    list_display = ('paslauga_id', 'automobiliai', 'kaina')

class UzsakymoKomentarasAdmin(admin.ModelAdmin):
    list_display = ('uzsakymas_id', 'klientas_id', 'date_created', 'komentaras')

admin.site.register(Paslauga)
admin.site.register(Automobilio_modelis)
admin.site.register(Paslaugos_kaina, PaslaugosKainaAdmin)
admin.site.register(Automobilis, AutomobilisAdmin)
admin.site.register(Uzsakymas, UzsakymasAdmin)
admin.site.register(UzsakymoEilute)
admin.site.register(UzsakymoKomentaras, UzsakymoKomentarasAdmin)
admin.site.register(Profilis)

