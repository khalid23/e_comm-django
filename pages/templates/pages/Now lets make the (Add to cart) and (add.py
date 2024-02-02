Now lets make the (Add to cart) and (add to wishlist ) to work in the products too.
Here is the current html 

<!-- Products -->
<div class="container g-pb-100">
  <div class="text-center mx-auto g-max-width-600 g-mb-50">
      <h2 class="g-color-black mb-4">Featured Products</h2>
      <p class="lead">We want to create a range of beautiful, practical and modern outerwear that doesn't cost the earth – but lets you still live life in style.</p>
  </div>

  <div id="carouselCus1" class="js-carousel g-pb-100 g-mx-minus-10"
       data-infinite="true"
       data-slides-show="4"
       data-arrows-classes="u-arrow-v1 g-pos-abs g-bottom-0 g-width-45 g-height-45 g-color-gray-dark-v5 g-bg-secondary g-color-white--hover g-bg-primary--hover rounded"
       data-arrow-left-classes="fa fa-angle-left g-left-10"
       data-arrow-right-classes="fa fa-angle-right g-right-10"
       data-pagi-classes="u-carousel-indicators-v1 g-absolute-centered--x g-bottom-20 text-center">

      {% for product in featured_products %}
      <div class="js-slide">
          <div class="g-px-10">

              <!-- Product -->
              {% if product.images.first %}
              <figure class="g-pos-rel g-mb-20">
                  <img class="img-fluid" src="{{ product.images.first.image.url }}" alt="{{ product.name }}">
                  {% if product.discount_percentage %}
                  <span class="u-ribbon-v1 g-width-40 g-height-40 g-color-white g-bg-primary g-font-size-13 text-center text-uppercase g-rounded-50x g-top-10 g-right-minus-10 g-px-2 g-py-10">-{{ product.discount_percentage }}%</span>
                  {% endif %}
                  {% if product.is_new_arrival %}
                      <figcaption class="w-100 g-bg-primary g-bg-black--hover text-center g-pos-abs g-bottom-0 g-transition-0_2 g-py-5">
                          <a class="g-color-white g-font-size-11 text-uppercase g-letter-spacing-1 g-text-underline--none--hover" href="#">New Arrival</a>
                      </figcaption>
                  {% elif product.is_sold_out %}
                      <figcaption class="w-100 g-bg-lightred text-center g-pos-abs g-bottom-0 g-transition-0_2 g-py-5">
                          <span class="g-color-white g-font-size-11 text-uppercase g-letter-spacing-1">Sold Out</span>
                      </figcaption>
                  {% endif %}
              </figure>
              {% endif %}

              <div class="media">
                  <!-- Product Info -->
                  <div class="d-flex flex-column">
                      <h4 class="h6 g-color-black mb-1">
                          <a class="u-link-v5 g-color-black g-color-primary--hover" href="#">
                              {{ product.name }}
                          </a>
                      </h4>
                      <a class="d-inline-block g-color-gray-dark-v5 g-font-size-13" href="{% url 'category_detail' product.category.id %}">{{ product.category.name }}</a>
                      <span class="d-block g-color-black g-font-size-17">${{ product.price }}</span>
                  </div>
                  <!-- End Product Info -->

                  <!-- Products Icons -->
                  <ul class="list-inline media-body text-right">
                      <li class="list-inline-item align-middle mx-0">
                          <a class="u-icon-v1 u-icon-size--sm g-color-gray-dark-v5 g-color-primary--hover g-font-size-15 rounded-circle" href="#"
                              data-toggle="tooltip"
                              data-placement="top"
                              title="Add to Cart">
                              <i class="icon-finance-100 u-line-icon-pro"></i>
                          </a>
                      </li>
                      <li class="list-inline-item align-middle mx-0">
                          <a class="u-icon-v1 u-icon-size--sm g-color-gray-dark-v5 g-color-primary--hover g-font-size-15 rounded-circle" href="#"
                              data-toggle="tooltip"
                              data-placement="top"
                              title="Add to Wishlist">
                              <i class="icon-medical-022 u-line-icon-pro"></i>
                          </a>
                      </li>
                  </ul>
                  <!-- End Products Icons -->
              </div>
              <!-- End Product -->
          </div>
      </div>
      {% endfor %}
  </div>
</div>
<!-- End Products -->


My current models

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Collection(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='collection_images/')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.TextField()
    sizes = models.TextField()
    quantity = models.PositiveIntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    is_featured = models.BooleanField(default=False)
    colors = models.ManyToManyField(Color, related_name='products')
    collections = models.ManyToManyField(Collection, related_name='products')
    is_new_arrival = models.BooleanField(default=False)
    is_sold_out = models.BooleanField(default=False)
    discount_percentage = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')



    my current views 

    from django.shortcuts import render, get_object_or_404
from .models import Product, Collection, Category
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



my current urls 

from django.urls import path
from .views import home, collection_detail, category_detail

urlpatterns = [
    path('', home, name='home'),
    path('collection/<int:collection_id>/', collection_detail, name='collection_detail'),
    path('categories/<int:category_id>/', category_detail, name='category_detail'),
]
