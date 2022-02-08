from multiprocessing import context
from django.shortcuts import render

listings = [
    {
        'listingID': 451324,
        'title': 'Game Developer',
        'lang' : 'C++',
        'company': 'Unreal Engine',
        'region': 'West Midlands',
        'datePosted': 'February 5, 2022'
    }
]

# Create your views here.
def homepage(request):
    context = {
        'listings': listings
    }
    return render(request, 'homepage.html', context)