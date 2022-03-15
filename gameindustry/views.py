from pickle import GET
from django.shortcuts import render
from .models import Offer
from .models import *
from .filters import OfferFilter


def homepage(request):
    """
    Provides the view for the /gameindustry/ page
    """

    latest_timestamp = Offer.objects.all().order_by('-time_scraped')[0].time_scraped
    latest_offers = Offer.objects.filter(time_scraped=latest_timestamp)

    offerFilter = OfferFilter(request.GET, queryset=latest_offers)
    latest_offers = offerFilter.qs
    langs = [0,0,0,0,0,0]
    for offer in latest_offers:
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
        'offers': latest_offers,
        'offerFilter': offerFilter,
        'langs': langs
    }
    return render(request, 'homepage.html', context)
