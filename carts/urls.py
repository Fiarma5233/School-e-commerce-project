from django.urls import path
from . import views

urlpatterns = [
    # url pour aller  panier
    path('', views.cart, name='cart'),
    # url pour ajouter un unarticle au panier
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    # url pour decrementer la quantite ou supprimer un article du  panier
   # path('remove_cart/<int:product_id>/', views.remove_cart, name='remove_cart'),
   	path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),

    # url pour  supprimer un article du  panier
    #path('remove_cart_item/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),

    # url pour voir les producits
	path('checkout/', views.checkout, name='checkout'),

]