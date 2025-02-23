from django.urls import path
from . import views

urlpatterns = [
	path('place_order/', views.place_order, name='place_order'), # url pour passer une commande
	path('payments/', views.payments, name='payments'), # url pour paiement
	path('order_complete/', views.order_complete, name="order_complete"), # url vers la page de paiement reusie
]