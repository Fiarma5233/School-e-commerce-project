from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem

from store.models import Product
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


from .forms import OrderForm # importation du formulaire de la commande
from .models import Order, Payment, OrderProduct
import datetime
import json


# vue pour les paiement
def payments(request):
	body = json.loads(request.body) # on charge le body
	order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

	#enregistrer les informations sur la transaction.
	payment = Payment(
		user = request.user,
		payment_id = body['transID'],
		payment_method = body['payment_method'],
		amount_paid = order.order_total,# montant total
		status = body['status'],
	)
	payment.save()

	order.payment = payment #paiement
	order.is_ordered = True # commande validee
	order.save()# commande enregistree

	cart_items = CartItem.objects.filter(user=request.user)# on filtre et recupere les articles de l'utilisateur connecte
	for item in cart_items: # Pour chaq article parmi les articles du panier
		orderproduct = OrderProduct() # Produit commande
		orderproduct.order_id = order.id #id du produit commande
		orderproduct.payment = payment # produit paye = paiement
		orderproduct.user_id = request.user.id # 
		orderproduct.product_id = item.product_id 
		orderproduct.quantity = item.quantity 
		orderproduct.product_price = item.product.price 
		orderproduct.ordered = True 
		orderproduct.save()

    #Pour gerer les variatios des produits
		cart_item = CartItem.objects.get(id=item.id)
		product_variation = cart_item.variations.all()
		orderproduct = OrderProduct.objects.get(id=orderproduct.id)
		orderproduct.variations.set(product_variation)
		orderproduct.save()

        #
		product = Product.objects.get(id=item.product_id)
		product.stock -= item.quantity
		product.save()

	CartItem.objects.filter(user=request.user).delete()

    # Email de remerciement
	mail_subject = "Merci pour votre commande chez Fiarma Shop"
	message = render_to_string('orders/order_receveid_email.html', {
		'user': request.user,
		'order': order,
	})
	to_email = request.user.email 
	send_email = EmailMessage(mail_subject, message, to=[to_email])
	send_email.send()

    
	data = {
		'order_number': order.order_number,
		'transID': payment.payment_id,
	}
	return JsonResponse(data)

# # Vue pour passer une commande
# def place_order(request, total=0, quantity=0):
# 	current_user = request.user # utilisateur actuel

# 	cart_items = CartItem.objects.filter(user=current_user) # articles de l'utilisateur actuel
# 	cart_count = cart_items.count() # on compte le nombre de produits concernant l'utilisateur
# 	if cart_count <= 0: # si le nombre est <=0, 
# 		return redirect('store') # on le redirige vers  la boutique

#     # initialisation des variables
# 	grand_total = 0 
# 	tax = 0
# 	for cart_item in cart_items: # pour chaque article parmis les articles du panier
# 		total += (cart_item.product.price * cart_item.quantity) # calcul du total
# 		quantity += cart_item.quantity # incrementation de la quantity

# 	tax = (2 * total)/100 # calcul de la taxe
# 	grand_total = total + tax  # prix global

# 	if request.method == 'POST': # si c'est pour soumettre un formulaire
# 		form = OrderForm(request.POST) # Formulaire
# 		if form.is_valid(): # si le formulaire est valide
# 			data = Order() # donnees
# 			data.user = current_user# on recupere l'utilisateur
			
#             # on recupere les informations envoyees par l'utilisateur et on nettoie les champs
# 			data.nom = form.cleaned_data['nom']
# 			data.prenom = form.cleaned_data['prenom']
# 			data.phone = form.cleaned_data['phone']
# 			data.email = form.cleaned_data['email']
# 			data.address_line_1 = form.cleaned_data['address_line_1']
# 			data.address_line_2 = form.cleaned_data['address_line_2']
# 			data.country = form.cleaned_data['country']
# 			data.state = form.cleaned_data['state']
# 			data.city = form.cleaned_data['city']
# 			data.order_note = form.cleaned_data['order_note']
# 			data.order_total = grand_total
# 			data.tax = tax
# 			data.ip = request.META.get('REMOTE_ADDR') # addresse de l'utilisateur
# 			data.save()

#             # generation d'un numero pour chq commande
# 			yr = int(datetime.date.today().strftime('%Y')) # annee
# 			dt = int(datetime.date.today().strftime('%d')) # jour
# 			mt = int(datetime.date.today().strftime('%m')) # mois
# 			d = datetime.date(yr,mt,dt)     # date
# 			current_date = d.strftime('%Y%m%d') # date actuelle 20240215
# 			order_number = current_date + str(data.id) # numero de la commande composee de la date actuelle et du numero id de la commande
# 			data.order_number = order_number
# 			data.save()

# 			order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number) # on recupere la commande
# 			context = {
# 				'order': order,
# 				'cart_items': cart_items,
# 				'total': total,
# 				'tax': tax,
# 				'grand_total': grand_total,
# 			}
# 			return render(request, 'orders/payments.html', context)
# 		else:
# 			print(form.errors)
# 	else:
# 		return redirect('checkout')




def place_order(request, total=0, quantity=0):
    current_user = request.user  # Utilisateur actuel

    # Récupérer les articles du panier de l'utilisateur
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()  # Nombre d'articles dans le panier

    # Si le panier est vide, rediriger vers la boutique
    if cart_count <= 0:
        return redirect('store')

    # Calcul du total, de la taxe et du grand total
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)  # Total des articles
        quantity += cart_item.quantity  # Quantité totale

    tax = (2 * total) / 100  # Calcul de la taxe (2%)
    grand_total = total + tax  # Prix total avec taxe

    if request.method == 'POST':  # Si la méthode est POST (soumission du formulaire)
        form = OrderForm(request.POST)  # Instancier le formulaire avec les données POST
        if form.is_valid():  # Si le formulaire est valide
            # Créer une nouvelle commande
            data = Order()
            data.user = current_user  # Utilisateur actuel

            # Récupérer et nettoyer les données du formulaire
            data.nom = form.cleaned_data['nom']
            data.prenom = form.cleaned_data['prenom']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')  # Adresse IP de l'utilisateur
            data.save()

            # Générer un numéro de commande unique
            yr = int(datetime.date.today().strftime('%Y'))  # Année
            dt = int(datetime.date.today().strftime('%d'))  # Jour
            mt = int(datetime.date.today().strftime('%m'))  # Mois
            d = datetime.date(yr, mt, dt)  # Date actuelle
            current_date = d.strftime('%Y%m%d')  # Format de la date (AAAAMMJJ)
            order_number = current_date + str(data.id)  # Numéro de commande (date + ID)
            data.order_number = order_number
            data.save()

            # Récupérer la commande créée
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

            # Préparer le contexte pour le template
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)
        else:
            # Si le formulaire n'est pas valide, réafficher le formulaire avec les erreurs
            context = {
                'form': form,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)
    else:
        # Si la méthode n'est pas POST, rediriger vers la page de paiement
        return redirect('checkout')

        
###########  Modification ###############
# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from .models import CartItem, Order
# from .forms import OrderForm
# import datetime

# def place_order(request, total=0, quantity=0):
#     current_user = request.user  # Utilisateur actuel

#     # Récupérer les articles du panier de l'utilisateur
#     cart_items = CartItem.objects.filter(user=current_user)
#     cart_count = cart_items.count()  # Nombre d'articles dans le panier

#     # Si le panier est vide, rediriger vers la boutique
#     if cart_count <= 0:
#         return redirect('store')

#     # Calcul du total, de la taxe et du grand total
#     grand_total = 0
#     tax = 0
#     for cart_item in cart_items:
#         total += (cart_item.product.price * cart_item.quantity)  # Total des articles
#         quantity += cart_item.quantity  # Quantité totale

#     tax = (2 * total) / 100  # Calcul de la taxe (2%)
#     grand_total = total + tax  # Prix total avec taxe

#     if request.method == 'POST':  # Si la méthode est POST (soumission du formulaire)
#         form = OrderForm(request.POST)  # Instancier le formulaire avec les données POST
#         if form.is_valid():  # Si le formulaire est valide
#             # Créer une nouvelle commande
#             data = Order()
#             data.user = current_user  # Utilisateur actuel

#             # Récupérer et nettoyer les données du formulaire
#             data.nom = form.cleaned_data['nom']
#             data.prenom = form.cleaned_data['prenom']
#             data.phone = form.cleaned_data['phone']
#             data.email = form.cleaned_data['email']
#             data.address_line_1 = form.cleaned_data['address_line_1']
#             data.address_line_2 = form.cleaned_data['address_line_2']
#             data.country = form.cleaned_data['country']
#             data.state = form.cleaned_data['state']
#             data.city = form.cleaned_data['city']
#             data.order_note = form.cleaned_data['order_note']
#             data.order_total = grand_total
#             data.tax = tax
#             data.ip = request.META.get('REMOTE_ADDR')  # Adresse IP de l'utilisateur
#             data.save()

#             # Générer un numéro de commande unique
#             yr = int(datetime.date.today().strftime('%Y'))  # Année
#             dt = int(datetime.date.today().strftime('%d'))  # Jour
#             mt = int(datetime.date.today().strftime('%m'))  # Mois
#             d = datetime.date(yr, mt, dt)  # Date actuelle
#             current_date = d.strftime('%Y%m%d')  # Format de la date (AAAAMMJJ)
#             order_number = current_date + str(data.id)  # Numéro de commande (date + ID)
#             data.order_number = order_number
#             data.save()

#             # Récupérer la commande créée
#             order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

#             # Préparer le contexte pour le template
#             context = {
#                 'order': order,
#                 'cart_items': cart_items,
#                 'total': total,
#                 'tax': tax,
#                 'grand_total': grand_total,
#             }
#             return render(request, 'orders/payments.html', context)
#         else:
#             # Si le formulaire n'est pas valide, réafficher le formulaire avec les erreurs
#             context = {
#                 'form': form,
#                 'cart_items': cart_items,
#                 'total': total,
#                 'tax': tax,
#                 'grand_total': grand_total,
#             }
#             return render(request, 'orders/payments.html', context)
#     else:
#         # Si la méthode n'est pas POST, rediriger vers la page de paiement
#         return redirect('checkout')


def order_complete(request):
	order_number = request.GET.get('order_number')
	transID = request.GET.get('payment_id')

	try:
		order = Order.objects.get(order_number=order_number, is_ordered=True)
		ordered_products = OrderProduct.objects.filter(order_id=order.id)

		subtotal = 0 
		for i in ordered_products:
			subtotal += i.product_price * i.quantity 

		payment = Payment.objects.get(payment_id=transID)

		context = {
			'order': order,
			'ordered_products': ordered_products,
			'order_number': order.order_number,
			'payment': payment,
			'subtotal': subtotal,
			'transID': transID,
		}
		return render(request, 'orders/order_complete.html', context)
	except (Payment.DoesNotExist, Order.DoesNotExist):
		return redirect('home')


