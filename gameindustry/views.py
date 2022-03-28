import time
from datetime import datetime as dt

from django.shortcuts import render, redirect
from django import template
from django.views.decorators.csrf import csrf_exempt

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

    if Offer.objects.all().count() == 0:
        return render(request, 'homepage.html')
    latest_timestamp = Offer.objects.all().order_by('-time_scraped')[0].time_scraped
    latest_offers = Offer.objects.filter(time_scraped=latest_timestamp)
    offerFilter = OfferFilter(request.GET, queryset=latest_offers)
    latest_offers = offerFilter.qs

    technologies_tech = [t.name.replace('\\', '') for t in Technology.objects.filter(type='TECH').all()]
    technologies_art = [t.name.replace('\\', '') for t in Technology.objects.filter(type='ART').all()]
    stats_tech = [0 for _ in technologies_tech]
    stats_art = [0 for _ in technologies_art]

    for offer in latest_offers:
        for idx, tech in enumerate(technologies_tech):
            if tech in offer.requirements.split('|'):
                stats_tech[idx] += 1

    for offer in latest_offers:
        for idx, tech in enumerate(technologies_art):
            if tech in offer.requirements.split('|'):
                stats_art[idx] += 1

    trends_tech = [(t, list()) for t in technologies_tech]
    timestamps = Offer.objects.values('time_scraped').order_by('time_scraped').distinct()
    for timestamp in timestamps:
        for idx, tech in enumerate(technologies_tech):
            timed_offers = Offer.objects.filter(time_scraped=timestamp['time_scraped']).filter(requirements__contains=tech).count()
            trends_tech[idx][1].append(timed_offers)

    trends_art = [(t, list()) for t in technologies_art]
    timestamps = Offer.objects.values('time_scraped').order_by('time_scraped').distinct()
    for timestamp in timestamps:
        for idx, art in enumerate(technologies_art):
            timed_offers = Offer.objects.filter(time_scraped=timestamp['time_scraped']).filter(requirements__contains=art).count()
            trends_art[idx][1].append(timed_offers)

    string_timestamps = [date['time_scraped'].strftime("%d-%b-%Y") for date in timestamps]

    context = {
        'offers': latest_offers,
        'offerFilter': offerFilter,
        'stats_tech': stats_tech,
        'stats_art': stats_art,
        'trends_tech': trends_tech,
        'trends_art': trends_art,
        'timestamps': string_timestamps,
        'technologies_tech': technologies_tech,
        'technologies_art': technologies_art
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


@csrf_exempt
def create_filter(request):
    """
    Provides the view for the /gameindustry/ page
    """
    new_tech_name = request.POST.get('new_tech')
    new_tech_type = request.POST.get('new_tech_type')
    if not new_tech_name:
        return redirect('/gameindustry/')
    new_tech = Technology(name=new_tech_name, type=new_tech_type)
    new_tech.save()
    return redirect('/gameindustry/')
