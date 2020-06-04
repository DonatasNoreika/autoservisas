from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import pytz
from tinymce.models import HTMLField
from PIL import Image
# import computed_property
from django.utils.translation import gettext_lazy as _

utc = pytz.UTC


class Paslauga(models.Model):
    name = models.CharField('Pavadinimas', max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Paslauga'
        verbose_name_plural = 'Paslaugos'


class Automobilio_modelis(models.Model):
    metai = models.IntegerField('Metai')
    marke = models.CharField('Markė', max_length=200)
    modelis = models.CharField('Modelis', max_length=200)
    variklis = models.CharField('Variklis', max_length=200)

    def __str__(self):
        return f"{self.metai}, {self.marke} {self.modelis}, {self.variklis}"

    class Meta:
        verbose_name = 'Automobilio modelis'
        verbose_name_plural = 'Automobilio modeliai'


class Paslaugos_kaina(models.Model):
    paslauga_id = models.ForeignKey('Paslauga', on_delete=models.SET_NULL, null=True)
    automobilis_ids = models.ManyToManyField(Automobilio_modelis)
    kaina = models.FloatField("Kaina")

    def __str__(self):
        return f"{self.paslauga_id}: {self.kaina}"

    def automobiliai(self):
        return ', '.join(f"{auto.marke} {auto.modelis}" for auto in self.automobilis_ids.all())

    automobiliai.short_description = 'Automobiliai'

    class Meta:
        verbose_name = 'Paslaugo kaina'
        verbose_name_plural = 'Paslaugų kainos'


class Automobilis(models.Model):
    savininkas = models.CharField(_('Owner'), max_length=200)
    automobilio_modelis_id = models.ForeignKey('Automobilio_modelis', verbose_name=_("Vehicle"), on_delete=models.SET_NULL, null=True)
    valstybinis_numeris = models.CharField(_('Licence plate'), max_length=200)
    vin_kodas = models.CharField(_('VIN code'), max_length=200)
    photo = models.ImageField(_('Photo'), upload_to='autos', null=True)
    aprasymas = HTMLField(_("Summary"), null=True)

    def __str__(self):
        return f"{self.savininkas}: {self.automobilio_modelis_id}, {self.valstybinis_numeris}, {self.vin_kodas}"

    class Meta:
        verbose_name = _('Vehicle')
        verbose_name_plural = _('Vehicles')


class Uzsakymas(models.Model):
    automobilis_id = models.ForeignKey('Automobilis', on_delete=models.SET_NULL, null=True)
    klientas_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    grazinimo_laikas = models.DateTimeField('Gražinimo terminas', null=True, blank=True)

    @property
    def suma(self):
        uzsakymo_eilutes = UzsakymoEilute.objects.filter(uzsakymas_id=self.id)
        suma = 0
        for eilute in uzsakymo_eilutes:
            suma += eilute.kiekis * eilute.kaina
        return suma

    def __str__(self):
        return f"{self.automobilis_id}: {self.suma}"

    # @property
    # def praejes_terminas(self):
    #     if self.grazinimo_laikas:
    #         start_time = self.grazinimo_laikas.replace(tzinfo=utc)
    #         end_time = datetime.today().replace(tzinfo=utc)
    #         print("Datos:", start_time, end_time)
    #     return self.grazinimo_laikas and end_time > start_time

    @property
    def praejes_terminas(self):
        if self.grazinimo_laikas and datetime.today().replace(tzinfo=utc) > self.grazinimo_laikas.replace(tzinfo=utc):
            return True
        return False

    class Meta:
        verbose_name = 'Užsakymas'
        verbose_name_plural = 'Užsakymai'

    STATUS = (
        ('p', 'Patvirtinta'),
        ('v', 'Vykdoma'),
        ('a', 'Atlikta'),
        ('t', 'Atšaukta'),
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS,
        blank=True,
        default='p',
        help_text='Statusas',
    )


class UzsakymoEilute(models.Model):
    uzsakymas_id = models.ForeignKey('Uzsakymas', related_name='eilutes', on_delete=models.SET_NULL, null=True)
    paslauga_id = models.ForeignKey('Paslauga', on_delete=models.SET_NULL, null=True)
    kiekis = models.IntegerField("Kiekis")
    kaina = models.FloatField("Kaina")
    # suma = computed_property.ComputedFloatField(compute_from='suma_calculation', null=True)

    @property
    def suma(self):
        return self.kiekis * self.kaina

    def __str__(self):
        return f"{self.paslauga_id} – {self.kiekis}: {self.kaina} {self.suma}"

    class Meta:
        verbose_name = 'Užsakymo eilutė'
        verbose_name_plural = 'Užsakymo eilutės'


class UzsakymoKomentaras(models.Model):
    uzsakymas_id = models.ForeignKey('Uzsakymas', on_delete=models.SET_NULL, null=True)
    klientas_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    komentaras = models.TextField('Komentaras', max_length=2000)

    class Meta:
        verbose_name = 'Komentaras'
        verbose_name_plural = 'Komentarai'


class Profilis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nuotrauka = models.ImageField(default="default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profilis"


    class Meta:
        verbose_name = 'Profilis'
        verbose_name_plural = 'Profiliai'

    def save(self):
        super().save()
        img = Image.open(self.nuotrauka.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.nuotrauka.path)

