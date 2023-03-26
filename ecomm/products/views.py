from django.shortcuts import render,redirect
from products.models import Product,SizeVariant
from accounts.models import Cart,CartItems
from django.http import HttpResponseRedirect

def get_products(request,slug):
    
    try:
        product=Product.objects.get(slug=slug)
        data={
            'product':product
        }
        if request.GET.get('size'):
            size=request.GET.get('size')
            price=product.get_product_price_by_size(size)
            data['selected_size']=size
            data['updated_price']=price        

        return render(request,'product/product.html',data)
    except Exception as e:
        print(e)

