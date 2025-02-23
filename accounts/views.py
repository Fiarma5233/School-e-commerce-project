from .forms import *



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from .models import Account, UserProfile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


## Import concernant l'action de compte
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


from carts.views import _cart_id
from carts.models import Cart, CartItem

from orders.models import Order, OrderProduct

import requests # bibilotheque installee pour modifier les redirections avec la commande pip install requests


# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .forms import RegistrationForm
from .models import Account, UserProfile

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Récupérer les données du formulaire
            nom = form.cleaned_data['nom']
            prenom = form.cleaned_data['prenom']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]  # username = email sans @gmail.com

            # Créer l'utilisateur
            user = Account.objects.create_user(
                nom=nom,
                prenom=prenom,
                email=email,
                username=username,
                password=password
            )
            user.phone_number = phone_number
            user.save()

            # Créer un profil utilisateur
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'avatars/default_image_pro.png'
            profile.save()

            # Activation de l'utilisateur
            current_site = get_current_site(request)  # Pour récupérer le site
            mail_subject = "S'il vous plait, activez votre compte !!!"  # Sujet du mail
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,  # Utilisateur
                'domain': current_site,  # Adresse du site
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),  # UID
                'token': default_token_generator.make_token(user),  # Token généré
            })
            to_email = email  # Email du destinataire
            send_email = EmailMessage(mail_subject, message, to=[to_email])  # Mail à envoyer
            send_email.send()  # Envoi du mail

            # Redirection après succès
            return redirect('/accounts/login/?command=verification&email=' + email)

    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


# Vue pour la connexion
def login(request):
	if request.method == 'POST': # si c'est pour soumettre des infos
		email = request.POST['email'] # on recuper l'email
		password = request.POST['password'] # on recupere le password

		user = auth.authenticate(email=email, password=password) # on authentifie l'utilisateur

		if user is not None: # si l'utilisateur existe
			try:
				cart = Cart.objects.get(cart_id=_cart_id(request)) # on lie le panier  a la session id (correspond a l'utilisateur connecte en ce momment)
				is_cart_item_exists = CartItem.objects.filter(cart=cart).exists() # existences d'articles dans lepanier
				if is_cart_item_exists: # s'il ya d'articles dans le panier
					cart_item = CartItem.objects.filter(cart=cart) # on  filtre chq article du panier

	
					product_variation = [] # iniatilsation de la variale a une liste vide
					for item in cart_item: # pour chq elemeent de ldes articles du panier
						variation = item.variations.all() # variation = varions de l'ement
						product_variation.append(list(variation)) # on regroupe les variation

					
					cart_item = CartItem.objects.filter(user=user) # panier d'articles de l'utilisateur
					ex_var_list = [] # initialisation 
					id = [] # initialisation des id
					for item in cart_item: # pour chq article dans le panier d'article
						existing_variation = item.variations.all() # variation_existante = toutes variations de l'articl
						ex_var_list.append(list(existing_variation)) # on ajoute 
						id.append(item.id) # on ajoude l'id

					for pr in product_variation: # pour chq produit dans les produits varies
						if pr in ex_var_list: # si le produit appart1 
							index = ex_var_list.index(pr) # on troute l'index du produit
							item_id = id[index] # l'id du produit(article) = id de l'index
							item = CartItem.objects.get(id=item_id) # on recupere les articles
							item.quantity += 1 # on increment la quantite
							item.user = user # on associe l'utilisateur a u produit
							item.save() # puis on enregistre le preoduit(article)
						else:
							cart_item = CartItem.objects.filter(cart=cart)
							for item in cart_item:
								item.user = user
								item.save()
			except:
				pass
			auth.login(request, user)
			messages.success(request, 'Vous à présent connecté.')
			url = request.META.get('HTTP_REFERER') # pour modifier la redirection
			try:
				query = requests.utils.urlparse(url).query	# Pourl'url

				params = dict(x.split('=') for x in query.split('&')) # pour parametres
				if 'next' in params: # si next dans params
					nextPage = params['next'] # page suivante 
					return redirect(nextPage) # redirection vers la page suivante
			except: #sinon
				return redirect('dashboard') # redirection vers le tableau de bord
		else:
			messages.error(request, 'Identifiant de connexion invalide')
			return redirect('login')

	return render(request, 'accounts/login.html')


# Vue pour la deconnexion
@login_required(login_url='login') # il faut d'abord est connecte pour pouvoir se deconnecter
def logout(request):
	auth.logout(request)
	messages.success(request, 'Vous êtes déconnecté')
	return redirect('login')

# cette fonction est utilise dans le fichier account_verification_email.html pour activer le compte
def activate(request, uidb64, token):
	try:
		uid = urlsafe_base64_decode(uidb64).decode() # on recuper le uid
		user = Account._default_manager.get(pk=uid) # on verifie qu'il s'git bien du vrai utilisateur
	#except(TypeError, ValueError, OverFlowError, Account.DoesNotExist): # on prevoit les divers cas d'exception
	except (TypeError, ValueError, OverflowError, Account.DoesNotExist):

		user = None # l'utilisateur ici est none
    

    # on verifie le user et le token et si les deux  sont verifie
	if user is not None and default_token_generator.check_token(user, token):
		user.is_active = True # on active l'utilisateur
		user.save() # on l'enregistre dans la db
		messages.success(request, 'Félicitation, votre compte est activé.') # on lui envoie un message d'encouragement
		return redirect('login') # Puis on le redirige vers la connexion
	else: # sinon
		messages.error(request, "Lien d'action invalide") # on lui envoi un message d;erreur
		return redirect('register')
	

@login_required(login_url='login')
def dashboard(request):
	# On recupere toutes les commandes de l'utilisateur connecte et on les filtre selon la plus recente a la plus ancienne
	orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True) # 
	# on compte le nombre de commande
	orders_count = orders.count()

	user = request.user
	userprofile, created = UserProfile.objects.get_or_create(user=user)  # Crée un profil si absent

	#userprofile = UserProfile.objects.get(user_id=request.user.id)
	context = {
		'orders_count':orders_count,
		'userprofile':userprofile,
	}
	return render(request, 'accounts/dashboard.html', context)

# vue pour les mots de passe oublies
def forgotPassword(request):
	if request.method == 'POST': # si c'est pour soumettre les infos(email)
		email = request.POST['email'] # On recupere le email soumis
		if Account.objects.filter(email=email).exists(): # On verifie voir si l'email existe
			user = Account.objects.get(email__exact=email) # on trouve l'utilsateur ayant cet email

			# REIINITIALISATION DU MOT DE PASSE

			current_site = get_current_site(request)
			mail_subject = "Rénitialiser votre mot de passe."
			message = render_to_string('accounts/reset_password_email.html', {
				'user': user,
				'domain': current_site,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': default_token_generator.make_token(user),
			})
			to_email = email
			send_email = EmailMessage(mail_subject, message, to=[to_email])
			send_email.send()

            # msg pour signaler a l'utilisateur que nous lui avons envoye un mail
			messages.success(request, " Nous vous avons envoyé un mail pour Rénitialiser votre mot de passe. ")
			return redirect('login')
		else: # sinon si l'addresse email que l'ulisisateur a envoye n'existe pas dans la db
			messages.error(request, "Votre compte n'existe pas.") # on lui signale ceci
			return redirect('forgotPassword') # on le rdirige vers ca
	return render(request, 'accounts/forgotPassword.html')

# vue pour valiter la renisialisation du mt de passe
def resetpassword_validate(request, uidb64, token):
	try:
		uid = urlsafe_base64_decode(uidb64).decode()
		user = Account._default_manager.get(pk=uid)
	except(TypeError, ValueError, OverFlowError, Account.DoesNotExist):
		user = None

	if user is not None and default_token_generator.check_token(user, token):
		request.session['uid'] = uid
		messages.success(request, "S'il vous plait réinitialiser le mot de passe.")
		return redirect('resetPassword')
	else:
		messages.error(request, "Le lien est expirer! ")
		return redirect('login')

# Vue pour renitialiser le password
def resetPassword(request):
	if request.method == 'POST': # si s'est pour soumettre des infos
		password = request.POST['password'] # on recupere le mot de passe
		confirm_password = request.POST['confirm_password'] # egalemeent la confirmation du password

		if password == confirm_password: # on verifie la conformite des deux password
			uid = request.session.get('uid') # uid correspond a l'uid de la session utilisation
			user = Account.objects.get(pk=uid) # on a l'utilisateur associe a cet uid
			user.set_password(password) # on change le password du user
			user.save() # on l'enregistre
			messages.success(request, "Reinitialisation du mot de passe Réussir") # on lui envoie un message de succes
			return redirect('login')
		else:
			messages.error(request, 'Les mots de passe ne se corresponde pas.')
			return redirect('resetPassword')
	else:
		return render(request, 'accounts/resetPassword.html')

# vue pour mes commandes
def my_orders(request):
	# on recupere les commandes de l'utilisateur connecte
	orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
	context = {
		'orders':orders,
	}
	return render(request, 'accounts/my_orders.html', context)

# vue pour modifier le profile utilisateur
@login_required(login_url='login')
def edit_profile(request):
	userprofile = get_object_or_404(UserProfile, user=request.user)# on recupere le profile utilisareuer sinon on lui renvoie une erreur
	if request.method == 'POST': # si c'est pour soumettre les donnees du formulaire
		user_form = UserForm(request.POST, instance=request.user) #formulaire de l'instance utiliseur
		profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)# formulaire du profile

		if user_form.is_valid() and profile_form.is_valid(): # si les 2 formulaires snt valides
			user_form.save() # enregistre 
			profile_form.save()#  sauvegarde
			messages.success(request, 'Votre profile est bien mis à jours.')# msg de success
			#return redirect('edit_profile')
			return redirect('dashboard')

	else:
		user_form = UserForm(instance=request.user)
		profile_form = UserProfileForm(instance=userprofile)

	context = {
		'user_form':user_form,
		'profile_form':profile_form,
		'userprofile':userprofile,
	}

	return render(request, 'accounts/edit_profile.html', context)

# Vue pour changer le mot de passe
@login_required(login_url='login')
def change_password(request):
	if request.method == 'POST':
		current_password = request.POST['current_password']
		new_password = request.POST['new_password']
		confirm_password = request.POST['confirm_password']

		user = Account.objects.get(username__exact=request.user.username)

		if new_password == confirm_password:
			success = user.check_password(current_password)
			if success:
				user.set_password(new_password)
				user.save()

				messages.success(request, 'Mise à jour du mot de passe réussie.')
				return redirect('change_password')
			else:
				messages.error(request, 'Veuillez entrer le mot de passe actuel valide')
				return redirect('change_password')
		else:
			messages.error(request, 'Le mot de passe ne correspond pas !')
			return redirect('change_password')
	return render(request, 'accounts/change_password.html')


# Vue pour voir les details de la commande
@login_required(login_url='login')
def order_detail(request, order_id):
	order_detail = OrderProduct.objects.filter(order__order_number=order_id)
	order = Order.objects.get(order_number=order_id)

	subtotal = 0
	for i in order_detail:
		subtotal += i.product_price * i.quantity

	context = {
		'order_detail': order_detail,
		'order': order,
		'subtotal': subtotal
	}
	return render(request, 'accounts/order_detail.html', context)