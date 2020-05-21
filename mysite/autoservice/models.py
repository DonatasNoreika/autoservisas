from django.db import models

# Create your models here.
from django.db import models


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
    savininkas = models.CharField('Savininkas', max_length=200)
    automobilio_modelis_id = models.ForeignKey('Automobilio_modelis', on_delete=models.SET_NULL, null=True)
    valstybinis_numeris = models.CharField('Valstybinis numeris', max_length=200)
    vin_kodas = models.CharField('VIN kodas', max_length=200)

    def __str__(self):
        return f"{self.savininkas}: {self.automobilio_modelis_id}, {self.valstybinis_numeris}, {self.vin_kodas}"

    class Meta:
        verbose_name = 'Automobilis'
        verbose_name_plural = 'Automobiliai'

class Uzsakymas(models.Model):
    automobilis_id = models.ForeignKey('Automobilis', on_delete=models.SET_NULL, null=True)
    suma = models.FloatField("Suma")

    def __str__(self):
        return f"{self.automobilis_id}: {self.suma}"

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
    uzsakymas_id = models.ForeignKey('Uzsakymas', on_delete=models.SET_NULL, null=True)
    paslauga_id = models.ForeignKey('Paslauga', on_delete=models.SET_NULL, null=True)
    kiekis = models.IntegerField("Kiekis")
    kaina = models.FloatField("Kaina")

    def __str__(self):
        return f"{self.paslauga_id} – {self.kiekis}: {self.kaina}"

    class Meta:
        verbose_name = 'Užsakymo eilutė'
        verbose_name_plural = 'Užsakymo eilutės'
