from pickle import GET
from django.shortcuts import render
from .models import Offer
from .models import *
from .filters import OfferFilter


def homepage(request):
    """
    Provides the view for the /gameindustry/home/ page
    """
    all_offers = Offer.objects.all()
    offerFilter = OfferFilter(request.GET, queryset=all_offers)
    all_offers = offerFilter.qs
    context = {
        'offers': all_offers,
        'offerFilter': offerFilter
    }
    return render(request, 'homepage.html', context)
