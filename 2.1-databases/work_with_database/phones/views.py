from django.shortcuts import render, redirect
from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):

    sort_type = request.GET.get("sort")
    if sort_type =="name":
        phones = Phone.objects.all().order_by('name')
    elif sort_type =="min_price":
        phones = Phone.objects.all().order_by('price')
    elif sort_type =="max_price":
        phones = Phone.objects.all().order_by('-price')
    else:
        phones = Phone.objects.all().order_by('name')

    template = 'catalog.html'
    context = {'phones': phones}
    return render(request, template, context)


def show_product(request, slug):
    phone = Phone.objects.get(slug=slug)
    template = 'product.html'
    context = {'phone': phone}
    return render(request, template, context)
