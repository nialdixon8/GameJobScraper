from django.shortcuts import render
from .models import Offer


def homepage(request):
    """
    Provides the view for the /gameindustry/home/ page
    """
    all_offers = Offer.objects.all()
    context = {
        'offers': all_offers
    }
    return render(request, 'homepage.html', context)
