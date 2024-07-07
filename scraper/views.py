from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponseRedirect
from .models import Link


# Create your views here.
def scrape(request):
    if request.method == "POST":
        site = request.POST.get('site', '')

        page = requests.get(site)
        soup = BeautifulSoup(page.text, 'html.parser')

        for link in soup.find_all('a'):  # Go through all <a> tag links on a site
            link_address = link.get('href')  # Get the link addresses
            link_text = link.string
            Link.objects.create(address=link_address, name=link_text)  # Create an object of the Link model
        return HttpResponseRedirect('/')  # Return to current homepage
    else:
        data = Link.objects.all()

    return render(request, 'scraper/result.html', {'data': data})


def clear(request):
    Link.objects.all().delete()  # Delete all Link objects
    return render(request, 'scraper/result.html')
