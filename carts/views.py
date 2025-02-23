from django.shortcuts import render,redirect, get_list_or_404,get_object_or_404
from django.http import HttpResponse
from .models import *
from store.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


# Create your views here.

# Cette fonction permet de recuperer l'id de la session de l'utilisateur
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart





# cette fonction permet d'ajouter un produit au panier prenant en paramettres, l'id du produit
'''def add_cart(request, product_id):
    # On recupere le produit correspodant a l'id
    ''product = Product.objects.get(id=product_id)
    product_variation = [] # declaration du tableau

    if request.method == 'POST':
        # on recupere les informations envoyees depuis le formulaire dans le fichichier product_detail
        for item in request.POST:# Pour tout element qu'on envoi depuis le formulaire'
            key = item # La cle == element (item). Par exemple la cle = color
            value = request.POST[key] # la valeur de l'element . Par exemple la valeur de la color =rouge
            #color = request.GET['color'] # Pour la couleur qui sera choisie 
            #size = request.GET['size'] # Pour la taille
            try:
                variation = Variation.objects.get(variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
                print(variation)
            except:
                pass''
    current_user = request.user # utilisateur actuel
    product = Product.objects.get(id=product_id)    # On recupere le produit correspodant a l'id


    if current_user.is_authenticated: # si l'utilisateur actuel est authentifier
        product_variation = [] # product_vation est vide
        if request.method == 'POST': # s'il veut  soumettre des infos
                
            # on recupere les informations envoyees depuis le formulaire dans le fichichier product_detail
            for item in request.POST:
                key = item # La cle == element (item). Par exemple la cle = color
                value = request.POST[key]    # la valeur de l'element . Par exemple la valeur de la color =rouge
                
                try:
                    # on verifie que:       
                            #- le produit est correspond au produit choisi
                            #  la categorie de la variation est exacte :par example Pour la couleur qui sera choisie 
                            # la valeur de la categorie est exacte : par exemple : rouge
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                            # On ajoute 
                    product_variation.append(variation)
                except: # sinon 
                    pass # on passe

    
    is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, user=current_user)
        ex_var_list = []
        id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)

        print(ex_var_list)

        if product_variation in ex_var_list:
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1 
            item.save()

        else:
            item = CartItem.objects.create(product=product, quantity=1, user=current_user)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()
    else:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            user = current_user,
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
            cart_item.save()
            return redirect('cart')
    
    
    
  
    return redirect('cart')'''


def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) #pour prendre le produit

    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass


        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            print(ex_var_list)

            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1 
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            print(ex_var_list)

            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1 
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')



# Vue pour decrementer  un article du panier et si la quantite est <=0 , on le supprimer
'''def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))# on recupere le panier de la sessionid
    product = get_list_or_404(Product, id=product_id) # on recupere le produit correspond a l'id ou on envoie un messaged'erreu

    try:
        if request.user.is_authenticated:

            # on recupere l'article correspondant au produit et appartenant au panier de l'utilisateur
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # sinon le panier correspond a l'utilisateur de la sessionid(de l'utilisateur actuel non authentifie)
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id) # panier d'articles

        if cart_item.quantity >=1 : # si la quantite vaut au moins 1
            cart_item.quantity -=1 # on le decrement a chaque foi qu'on clique sur le -
            cart_item.save() # on enregistre la nouvelle quantite

        else: # sinon qte <0
            cart_item.delete() # il est automatiquement supprime
    except:
        pass
    return redirect('cart') # redirection vers le panier

# cette vue c'est pour supprimer un article du panier sans passer par la decrementation
def remove_cart_item(request, product_id, cart_item_id):
    product = get_list_or_404(Product, id=product_id) # on recupere le produit correspond a l'id ou on envoie un messaged'erreu
    if request.user.is_authenticated: # si l'utilisateur est authentifie
        # on recupere l'article correspondant au produit et appartenant au panier
        cart_item =CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))	# on recupere le panier de la sessionid
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id) # on recupere l'article

    cart_item.delete() # il est automatiquement supprime
    return redirect('cart') # redirection vers le panier'''



def remove_cart(request, product_id, cart_item_id):

	product = get_object_or_404(Product, id=product_id)
	try:
		if request.user.is_authenticated:
			cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
		else:
			cart = Cart.objects.get(cart_id=_cart_id(request))
			cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
		if cart_item.quantity > 1:
			cart_item.quantity -= 1
			cart_item.save()
		else:
			cart_item.delete()
	except:
		pass 
	return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
	product = get_object_or_404(Product, id=product_id)
	if request.user.is_authenticated:
			cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
	else:
		cart = Cart.objects.get(cart_id=_cart_id(request))	
		cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
	cart_item.delete()
	return redirect('cart')






# Vue pour le panier
'''def cart(request, total=0, quantity=0, cart_items=None):

    try:
        tax = 0
        grand_total = 0

        if request.user.is_authenticated: # si lutilisateur est authentifie
            # on recupere le panier de la sessionid(qui appart1 a un seul user)
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
            #on filtre les articles
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items: #Pour  chq article parmis les articles di panier
            total +=  (cart_item.product.price * cart_item.quantity)
            quantity +=cart_item.quantity
        # tax, on peut prendre ca comme frais de livraison
        tax = (2 * total) / 100
        grand_total = total + tax

    except :
        pass

    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'grand_total':grand_total
    }

    return render(request, 'store/cart.html', context   )'''

def cart(request, total=0, quantity=0, cart_items=None):
	try:
		tax = 0
		grand_total = 0
		if request.user.is_authenticated:
			cart_items = CartItem.objects.filter(user=request.user, is_active=True)
		else:
			cart = Cart.objects.get(cart_id=_cart_id(request))
			cart_items = CartItem.objects.filter(cart=cart, is_active=True)
			
		for cart_item in cart_items:
			total += (cart_item.product.price * cart_item.quantity)
			quantity += cart_item.quantity
		tax = (2 * total)/100
		grand_total = total + tax
	except ObjectDoesNotExist:
		pass

	context = {
		'total': total,
		'quantity': quantity,
		'cart_items': cart_items,
		'tax':tax,
		'grand_total':grand_total,
	}

	return render(request, 'store/cart.html', context)



@login_required(login_url='login') # il faut etre connecter pour voir le detail
#ici ,on veut voir le total, la quatite, les articles
def checkout(request, total=0, quantity=0, cart_items=None):
	try:
          #initialisation des variables
		tax = 0
		grand_total = 0 
		if request.user.is_authenticated:# on veriifie si lutilisateur est authentifie
			cart_items = CartItem.objects.filter(user=request.user, is_active=True) # on filtre les articles
		else:
			cart = Cart.objects.get(cart_id=_cart_id(request))
			cart_items = CartItem.objects.filter(cart=cart, is_active=True)
		for cart_item in cart_items:
			total += (cart_item.product.price * cart_item.quantity)
			quantity += cart_item.quantity
		tax = (2 * total)/100
		grand_total = total + tax
	except ObjectDoesNotExist:
		pass

	context = {
		'tax': tax,
		'quantity': quantity,
		'total': total,
		'cart_items': cart_items,
		'grand_total':grand_total,
	}

	return render(request, 'store/checkout.html', context)