from functools import lru_cache
import csv
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.conf import settings


WANTED = ("Name", "Street", "District")
PAGE_SIZE = 10


@lru_cache(maxsize=1)
def load_bus_stations():
    with open(settings.BUS_STATION_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return tuple({k: row[k] for k in WANTED} for row in reader)


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    data = load_bus_stations()
    paginator = Paginator(data, PAGE_SIZE)
    page = paginator.get_page(request.GET.get("page"))
    context = {
         'bus_stations': page.object_list,
         'page': page,
    }
    return render(request, 'stations/index.html', context)
