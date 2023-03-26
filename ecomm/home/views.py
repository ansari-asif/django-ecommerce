from django.shortcuts import render
from products.models import Product


def index(request):
    products=Product.objects.all()
    data={
        'products':products
    }
    # print(products)
    return render(request,'home/index.html',data)