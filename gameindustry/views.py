from pickle import GET
from django.shortcuts import render
from .models import Offer
from .models import *
from .filters import OfferFilter


def homepage(request):
    """
    Provides the view for the /gameindustry/home/ page
    """
    latest_timestamp = Offer.objects.all().order_by('-time_scraped')[0].time_scraped
    latest_offers = Offer.objects.filter(time_scraped=latest_timestamp)

    offerFilter = OfferFilter(request.GET, queryset=latest_offers)
    latest_offers = offerFilter.qs
    context = {
        'offers': latest_offers,
        'offerFilter': offerFilter
    }
    return render(request, 'homepage.html', context)
