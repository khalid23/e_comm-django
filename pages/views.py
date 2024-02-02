from django.shortcuts import render, get_object_or_404
from .models import Product, Collection, Category
from django.http import JsonResponse
from django.db.models import Q


def home(request):
    new_arrivals = Product.objects.filter(is_new_arrival=True)
    sold_out = Product.objects.filter(is_sold_out=True)
    discounted_products = Product.objects.filter(discount_percentage__isnull=False)

    featured_products = Product.objects.filter(is_featured=True)
    promo_product = featured_products.first()
    collections = Collection.objects.all()
    categories = Category.objects.all()

    return render(request, 'pages/home.html', {
        'new_arrivals': new_arrivals,
        'sold_out': sold_out,
        'discounted_products': discounted_products,
        'featured_products': featured_products,
        'promo_product': promo_product,
        'collections': collections,
        'categories': categories,
    })


def collection_detail(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    products = collection.products.all()

    return render(request, 'pages/collection_detail.html', {'collection': collection, 'products': products})


def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(category=category)

    return render(request, 'pages/category_detail.html', {'category': category, 'products': products})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session['cart'] = cart

    response_data = {'message': f'{product.name} added to cart successfully'}
    return JsonResponse(response_data)

def get_cart_details(request):
    cart_html = render_to_string('pages/get_cart_details.html', {'cart': request.session.get('cart', {})})
    return JsonResponse({'html': cart_html})

def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    wishlist = request.session.get('wishlist', {})
    wishlist[product_id] = True
    request.session['wishlist'] = wishlist

    response_data = {'message': f'{product.name} added to wishlist successfully'}
    return JsonResponse(response_data)
