from django.shortcuts import render, get_object_or_404, redirect
from category.models import Category
from .models import Product
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator # Pour la pagination
from django.http import HttpResponse

from category.models import Category
from carts.views import _cart_id
from carts.models import *
from django.db.models import Q  # qui servira pour la recherche

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import ReviewForm 
from .models import ReviewRating
from django.contrib import messages
from .models import ProductGallery
from orders.models import OrderProduct


# Create your views here.

# Vue pour les produits par category

'''def store(request, category_slug=None):
    # Initialisation des variables
    categories = None
    products = None

    if category_slug != None: # sid  le slud de la cateory !=None
        categories = get_object_or_404(Category, slug=category_slug) # On obtient la category oou on renvoie une erreur de type 404
        products = Product.objects.all().filter(category=categories,  is_available=True)# Onaffiffche les fichiers disponibles
        product_count = products.count()
    else:
        products = Product.objects.all().filter(category=categories,  is_available=True)# Onaffiffche les fichiers disponibles
        product_count = products.count()

    context = {
        'products':products,
        'product_count':product_count
    }
    return render(request, 'store/store.html', context)'''



def store(request, category_slug=None):
     # Initialisation des variables

    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug) # On obtient la category oou on renvoie une erreur de type 404
        products = Product.objects.filter(category=categories ,is_available=True) #Onaffiffche les fichiers disponibles
        paginator = Paginator(products, 6) #  Affichage de 3 produits par page
        page = request.GET.get('page') # on obtien la page
        paged_products = paginator.get_page(page) # methode pour recuperer la page
        product_count = products.count() # on compte le nombre de produits
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products':paged_products,
        'product_count':product_count,
    }

    return render(request, 'store/store.html', context)


# Vue pour rechercher des produits
def search(request):
	if 'keyword' in request.GET: # si le mot qu'on cherche existe
		keyword = request.GET['keyword'] # On le recupere
		if keyword: 
               # Cela filtre les mots dans la descripton et les noms des produits puis les affiche selon le plus recent au plus anc1
			products = Product.objects.order_by('-modified_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            # Compte le nombre de produits retrouves
			product_count = products.count()
	context = {
		'products':products,
		'product_count':product_count,
	}
	return render(request, 'store/store.html', context)

"""
    Cette vue permet d'afficher les details de chaque produit.
    Etant donnee que chaque produit a son id et chaque produit appartient a une categorie ,
    alors, il va falloir d'abord avoir l'id de la categorie puis celui du produit,
    ce qui fait que dans la fonction product_detail, nous avons en parametres :
            -   category_slug ---> id de la categorie
            -   product_slug  ---> id du produit
"""



def product_detail(request, category_slug, product_slug):
	try:
		single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
		in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
	except Exception as e:
		raise e 

	if request.user.is_authenticated:
		try:
			orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
		except OrderProduct.DoesNotExist:
			orderproduct = None
	else:
		orderproduct = None

	reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

	product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

	context = {
		'single_product':single_product,
		'in_cart':in_cart,
		'orderproduct':orderproduct,
		'reviews':reviews,
		'product_gallery':product_gallery,
	}
	return render(request, 'store/product_detail.html', context)

# vue pour le commentaire
def submit_reviews(request, product_id):
	url = request.META.get('HTTP_REFERER') # url
	if request.method == 'POST':
		try:
			reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)# commetaire
			form = ReviewForm(request.POST, instance=reviews)
			form.save()
			messages.success(request, 'Merci ! Votre commentaire est bien mis a jours')
			return redirect(url)
		except ReviewRating.DoesNotExist:
			form = ReviewForm(request.POST)
			if form.is_valid():
				data = ReviewRating()
				data.subject = form.cleaned_data['subject']
				data.rating = form.cleaned_data['rating']
				data.review = form.cleaned_data['review']
				data.ip = request.META.get('REMOTE_ADDR')
				data.product_id = product_id 
				data.user_id = request.user.id 
				data.save()
				messages.success(request, 'Merci ! Votre commentaire est soumis')
				return redirect(url)