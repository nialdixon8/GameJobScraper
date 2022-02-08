from multiprocessing import context
from django.shortcuts import render
#removed import of HttpRequest as it is no longer needed.
#and response is not a single short string. Therefore used render.
#context is imported for outputing information stored in dictionary form.


#created a dictionary called 'listings'
# in which all the job listings and relevant information will be stored. 
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

#context is a dictionary with variable names as key and their values
#as the value. Placeholders in the template fetch information from
#context as it stores values inside the 'listing' dictionary.
    context = {
        'listings': listings
    }
    return render(request, 'homepage.html', context)