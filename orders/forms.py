from django import forms
from .models import Order 

class OrderForm(forms.ModelForm): # Formulaire de la commande
	class Meta:
		model = Order
		fields = ['nom', 'prenom', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'order_note']