from django.shortcuts import render, redirect

from products.models import Product
from .models import Cart
from orders.models import Order

# Create your views here.

# def cart_home(request):
#     cart_id = request.session.get('cart_id', None)
#     qs = Cart.objects.filter(id=cart_id)
#     if qs.count() == 1:
#         cart_obj = qs.first()
#         # If an user log in and the current session cart has no user, then assign it:
#         if request.user.is_authenticated() and cart_obj.user is None:
#             cart_obj.user = request.user
#             cart_obj.save()
#     else:
#         cart_obj = Cart.objects.new_cart(user=request.user)
#         request.session['cart_id'] = cart_obj.id
#     # print(request.session)
#     # request.session.set_expiry(300) # 5 min
#     return render(request, 'carts/home.html', {})


# Now moving all the creation cart logic to the CartManager (this way will be available for other apps):
def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get_cart(request)
    # Now all this is done by the signals
    # products = cart_obj.products.all()
    # total = 0
    # for prod in products:
    #     total += prod.price
    # print(total)
    # cart_obj.total = total
    # cart_obj.save()
    return render(request, 'carts/home.html', {'cart': cart_obj})

def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Show message to user, product is gone?")
            return redirect('cart:home')
        cart_obj, new_obj = Cart.objects.new_or_get_cart(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj) # cart_obj.products.add(product_id)
        request.session['cart_items'] = cart_obj.products.count()
    # return redirect(product_obj.get_absolute_url())
    return redirect('cart:home')

def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get_cart(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect('cart:home')
    else:
        order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
    return render(request, 'carts/checkout.html', {'object': order_obj})
