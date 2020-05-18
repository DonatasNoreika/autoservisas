from django.db import models

# Create your models here.
from django.db import models


class Paslauga(models.Model):
    name = models.CharField('Pavadinimas', max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Paslauga'


class Automobilio_modelis(models.Model):
    metai = models.IntegerField('Metai')
    marke = models.CharField('Markė', max_length=200)
    modelis = models.CharField('Modelis', max_length=200)
    variklis = models.CharField('Variklis', max_length=200)

    def __str__(self):
        return f"{self.metai}, {self.marke} {self.modelis}, {self.variklis}"


class Paslaugos_kaina(models.Model):
    paslauga_id = models.ForeignKey('Paslauga', on_delete=models.SET_NULL, null=True)
    automobilis_ids = models.ManyToManyField(Automobilio_modelis, help_text='Išrinkite žanrą(us) šiai knygai')
    kaina = models.FloatField("Kaina")

    def __str__(self):
        return f"{self.paslauga_id}: {self.kaina}"


class Automobilis(models.Model):
    savininkas = models.CharField('Savininkas', max_length=200)
    automobilio_modelis_id = models.ForeignKey('Automobilio_modelis', on_delete=models.SET_NULL, null=True)
    valstybinis_numeris = models.CharField('Valstybinis numeris', max_length=200)
    vin_kodas = models.CharField('VIN kodas', max_length=200)

    def __str__(self):
        return f"{self.savininkas}: {self.automobilio_modelis_id}, {self.valstybinis_numeris}, {self.vin_kodas}"


class Uzsakymas(models.Model):
    automobilis_id = models.ForeignKey('Automobilis', on_delete=models.SET_NULL, null=True)
    suma = models.FloatField("Suma")

    def __str__(self):
        return f"{self.automobilis_id}: {self.suma}"


class UzsakymoEilute(models.Model):
    uzsakymas_id = models.ForeignKey('Uzsakymas', on_delete=models.SET_NULL, null=True)
    paslauga_id = models.ForeignKey('Paslauga', on_delete=models.SET_NULL, null=True)
    kiekis = models.IntegerField("Kiekis")
    kaina = models.FloatField("Kaina")

    def __str__(self):
        return f"{self.paslauga_id} – {self.kiekis}: {self.kaina}"
