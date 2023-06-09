from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from .models import Profile
from products.models import Product,SizeVariant,Coupon
from accounts.models import Cart,CartItems
from django.http import HttpResponseRedirect


def login_page(request):
    if(request.method=='POST'):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj=User.objects.filter(username=email)
       
        if not user_obj.exists():
            messages.warning(request, 'Account not found')
            return HttpResponseRedirect(request.path_info)
    
        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)
        
        user_obj=authenticate(username=email,password=password)
        
        if(user_obj):
            login(request,user_obj)
            return redirect('/')
        
        messages.warning(request,'an invalid credentials')
        return HttpResponseRedirect(request.path_info)
    return render(request,'accounts/login.html')


def register_page(request):

    if(request.method=='POST'):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj=User.objects.filter(username=email)

        if user_obj.exists():
            messages.error(request, 'Email already exists')
            return HttpResponseRedirect(request.path_info)
        user_obj=User.objects.create(
            first_name=first_name, last_name=last_name, email=email, username=email
        )
        user_obj.set_password(password)
        user_obj.save()
        messages.success(request,'An email has been sent on your mail')
        return HttpResponseRedirect(request.path_info)
    return render(request,'accounts/register.html')   

def activate_email(request,email_token):
    try:
        user=Profile.objects.get(email_token=email_token)
        user.is_email_verified=True
        user.save()
        return redirect('/')
    except Exception as e:
        print(e)
        return HttpResponse('invalid Email Token')
import inspect
from pprint import pprint
def cart(request):
    cart_obj=Cart.objects.get(is_paid=False,user=request.user)
    data={
        'cart':cart_obj
    }

    if request.method =='POST':
        coupon=request.POST.get('coupon')
        coupon_obj=Coupon.objects.filter(coupon_code=coupon)
        print('********************************')
        print(vars(coupon_obj))
        print('********************************')
        if not coupon_obj.exists():
            messages.warning(request, 'Invalid Coupon Code')   
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if cart_obj.coupon:
            messages.warning(request, 'Coupon already exists')   
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))        
        
        if cart_obj.get_cart_total() < coupon_obj[0].minimum_amount:
            messages.success(request, f'Amount should be greater than {coupon_obj[0].minimum_amount}')   
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if coupon_obj[0].is_expired:
            messages.warning(request, 'Coupon expired')   
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
        cart_obj.coupon = coupon_obj[0]
        cart_obj.save()
        messages.success(request, 'Coupon applied successfully')   
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request,'accounts/cart.html',data)   

def remove_coupon(request,cart_uid):
    try:
        cart=Cart.objects.get(uid=cart_uid)
        cart.coupon=None
        cart.save()
        messages.success(request, 'Coupon removed')  
    except Exception as e:
        print(e) 
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def add_to_cart(request,uid):
    variant=request.GET.get('variant')
    
    product=Product.objects.get(uid=uid)
    user=request.user
    cart,_=Cart.objects.get_or_create(user=user,is_paid=False)
    cart_item=CartItems.objects.create(cart=cart,product=product)

    if variant:
        variant=request.GET.get('variant')
        size_variant=SizeVariant.objects.get(size_name=variant)
        cart_item.size_variant=size_variant
        cart_item.save()


    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_cart(request, cartItem_uid):
    try:
        cart_item =CartItems.objects.get(uid=cartItem_uid)
        cart_item.delete()
    except exception as e:
        print(e)
                
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

