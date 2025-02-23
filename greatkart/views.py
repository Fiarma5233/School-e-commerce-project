# from django.shortcuts import render
# from store.models import Product, ReviewRating, Reviews

# def home(request):
# 	products = Product.objects.all().filter(is_available=True)

# 	for product in products:
# 		reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

# 	context = {
# 		'products':products,
# 		'reviews':reviews,
# 	}
# 	return render(request, 'home.html', context)


# from django.shortcuts import render
# from store.models import Product, ReviewRating

# def home(request):
#     products = Product.objects.all().filter(is_available=True)
#     reviews = []  # Initialiser reviews comme une liste vide

#     for product in products:
#         product_reviews = ReviewRating.objects.filter(product_id=product.id, status=True)
#         reviews.extend(product_reviews)  # Ajouter les avis à la liste

#     context = {
#         'products': products,
#         'reviews': reviews,  # Utiliser la liste complète des avis
#     }
#     return render(request, 'home.html', context)


from django.shortcuts import render
from django.db.models import Prefetch
from store.models import Product, ReviewRating

def home(request):
    products = Product.objects.all().filter(is_available=True).prefetch_related()
    Prefetch('reviewrating_set', queryset=ReviewRating.objects.filter(status=True))
    context = {
        'products': products,
    }
    return render(request, 'home.html', context)