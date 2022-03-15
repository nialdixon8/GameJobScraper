from pickle import GET
from django.shortcuts import render
from .models import Offer
from .models import *
from .filters import OfferFilter


def homepage(request):
    """
    Provides the view for the /gameindustry/ page
    """
    all_offers = Offer.objects.all()
    offerFilter = OfferFilter(request.GET, queryset=all_offers)
    all_offers = offerFilter.qs
    langs = [0,0,0,0,0,0]
    for offer in all_offers:
        if "Python" in offer.requirements.split():
            langs[0] +=1
        if "C++" in offer.requirements.split():
            langs[1] +=1
        if "C#" in offer.requirements.split():
            langs[2] +=1
        if "Java" in offer.requirements.split():
            langs[3] +=1
        if "SQL" in offer.requirements.split():
            langs[4] +=1
        if "Unity" in offer.requirements.split():
            langs[5] +=1
    context = {
        'offers': all_offers,
        'offerFilter': offerFilter,
        'langs': langs

    }
    return render(request, 'homepage.html', context)
