from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from .models import Paslauga, Uzsakymas, Automobilis
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q

def index(request):
    paslaugu_kiekis = Paslauga.objects.count()
    atliktu_uzsakymu_kiekis = Uzsakymas.objects.filter(status__exact='a').count()
    automobiliu_kiekis = Automobilis.objects.count()

    # perduodame informaciją į šabloną žodyno pavidale:
    context = {
        'paslaugu_kiekis': paslaugu_kiekis,
        'atliktu_uzsakymu_kiekis': atliktu_uzsakymu_kiekis,
        'automobiliu_kiekis': automobiliu_kiekis,
    }

    # renderiname base.html, su duomenimis kintamąjame context
    return render(request, 'index.html', context=context)

def automobiliai(request):
    paginator = Paginator(Automobilis.objects.all(), 5)
    page_number = request.GET.get('page')
    paged_automobiliai = paginator.get_page(page_number)
    context = {
        'automobiliai': paged_automobiliai
    }
    return render(request, 'automobiliai.html', context=context)

def automobilis(request, automobilis_id):
    automobilis = get_object_or_404(Automobilis, pk=automobilis_id)
    return render(request, 'automobilis.html', context={'automobilis': automobilis})


def search(request):
    """
    paprasta paieška. query ima informaciją iš paieškos laukelio,
    search_results prafiltruoja pagal įvestą tekstą knygų pavadinimus ir aprašymus.
    Icontains nuo contains skiriasi tuo, kad icontains ignoruoja ar raidės
    didžiosios/mažosios.
    """
    query = request.GET.get('query')
    search_results = Automobilis.objects.filter(Q(savininkas__icontains=query) | Q(valstybinis_numeris__icontains=query) | Q(vin_kodas__icontains=query) | Q(automobilio_modelis_id__marke__icontains=query) | Q(automobilio_modelis_id__modelis__icontains=query))
    return render(request, 'search.html', {'automobiliai': search_results, 'query': query})


class UzsakymaiListView(generic.ListView):
    model = Uzsakymas
    context_object_name = 'uzsakymai'
    paginate_by = 5
    template_name = 'uzsakymai.html'

class UzsakymasDetailView(generic.DetailView):
    model = Uzsakymas
    template_name = 'uzsakymas.html'