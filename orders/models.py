from django.db import models

# Create your models here.

from django.db import models
from accounts.models import Account
from store.models import Product, Variation

class Payment(models.Model): # Table paiement
	user = models.ForeignKey(Account, on_delete=models.CASCADE) # on associe chque utilisateur au paiement
	payment_id = models.CharField(max_length=100) # id du paiement
	payment_method = models.CharField(max_length=100) # le moyement de paiement
	amount_paid = models.CharField(max_length=100) # la quantite payee
	status = models.CharField(max_length=100) # status du paiement
	created_at = models.DateTimeField(auto_now_add=True) # date de creation 

	def __str__(self):
		return self.payment_id


class Order(models.Model): # table commande
	# status de la commande
	STATUS = (
		('New','New'), # Nouvelle commande
		('Accepted','Accepted'), # Accepter
		('Completed','Completed'), # completer
		('Cancelled','Cancelled'), # Annuler
	)

	user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True) # on associe la commande a un utilisateur
	payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True) # on associe la commande au paiement
	order_number = models.CharField(max_length=30) # ordre de la commande
	nom = models.CharField(max_length=50)   
	prenom = models.CharField(max_length=50)
	phone = models.CharField(max_length=20)
	email = models.EmailField(max_length=50)
	address_line_1 = models.CharField(max_length=50)
	address_line_2 = models.CharField(max_length=50, blank=True)
	country = models.CharField(max_length=50)
	state = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	order_note = models.CharField(max_length=100, blank=True) # note de commande
	order_total = models.FloatField()   # Commande totale
	tax = models.FloatField()   # taxe
	status = models.CharField(max_length=10, choices=STATUS, default='New') # status
	ip = models.CharField(blank=True, max_length=20)
	is_ordered = models.BooleanField(default=False) # si c'est une commande
	created_at = models.DateTimeField(auto_now_add=True) # date de creation
	updated_at = models.DateTimeField(auto_now=True) # date de mise a jour

	def full_name(self):
		return f'{self.nom} {self.prenom}'

	def full_address(self):
		return f'{self.address_line_1} {self.address_line_2}'


	def __str__(self):
		return self.nom


class OrderProduct(models.Model): # Table commande du produit
	order = models.ForeignKey(Order, on_delete=models.CASCADE) # on associe un prouit commande a une commande
	payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True) # on associe un prouit commande a un paiement
	user = models.ForeignKey(Account, on_delete=models.CASCADE) # on associe un prouit commande a un utilisateur
	product = models.ForeignKey(Product, on_delete=models.CASCADE) # on associe un prouit commande a un produit
	variations = models.ManyToManyField(Variation, blank=True) # pour les variations
	quantity = models.IntegerField()
	product_price = models.FloatField()
	ordered = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True) # dat de creation
	updated_at = models.DateTimeField(auto_now=True) # date de mise a jour

	def __str__(self):
		return self.product.product_name