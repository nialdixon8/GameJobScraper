import time
from datetime import datetime as dt

from django.shortcuts import render, redirect
from django import template

from .models import *
from .filters import OfferFilter
from lib.scraping import *

register = template.Library()


@register.filter(name='idx')
def return_item(l, i):
    try:
        return l[i]
    except:
        return None


def homepage(request):
    """
    Provides the view for the /gameindustry/ page
    """

    latest_timestamp = Offer.objects.all().order_by('-time_scraped')[0].time_scraped
    latest_offers = Offer.objects.filter(time_scraped=latest_timestamp)
    offerFilter = OfferFilter(request.GET, queryset=latest_offers)
    latest_offers = offerFilter.qs

    langs = [0, 0, 0, 0, 0, 0]
    for offer in latest_offers:
        for idx, tech in enumerate(TECHNOLOGIES):
            tech = tech.replace('\\', '')
            if tech in offer.requirements.split():
                langs[idx] += 1

    trends = [list(), list(), list(), list(), list(), list()]
    timestamps = Offer.objects.values('time_scraped').order_by('time_scraped').distinct()
    for timestamp in timestamps:
        for idx, tech in enumerate(TECHNOLOGIES):
            tech = tech.replace('\\', '')
            timed_offers = Offer.objects.filter(time_scraped=timestamp['time_scraped']).filter(requirements__contains=tech).count()
            trends[idx].append(timed_offers)
    string_timestamps = [date['time_scraped'].strftime("%d-%b-%Y") for date in timestamps]
    print('string_timestamps: {}'.format(string_timestamps))

    context = {
        'offers': latest_offers,
        'offerFilter': offerFilter,
        'langs': langs,
        'trends': trends,
        'timestamps': string_timestamps
    }
    return render(request, 'homepage.html', context)


def scrape(request):
    """
    Provides the view for the /gameindustry/ page
    """

    timestamp = dt.now()
    start_all = time.time()
    for scraper_class in (GamesJobDirectScraper, GameindustryBizScraper, AmiqusScraper):
        start = time.time()
        scraper_class(timestamp).main()
        end = time.time()
        print('{} done in {:.2f}s'.format(scraper_class.__name__, end - start))
    end_all = time.time()
    print('Total scraping time: {:.2f}s'.format(end_all - start_all))
    return redirect('/gameindustry/')

