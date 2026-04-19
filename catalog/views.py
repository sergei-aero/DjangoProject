from django.shortcuts import render
from .models import Product

def home(request):
    products = Product.objects.all()
    return render(request, 'catalog/home.html', {'products': products})

def contacts(request):
    return render(request, 'catalog/contacts.html')

def product_detail(request, pk):
    from django.shortcuts import get_object_or_404
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})