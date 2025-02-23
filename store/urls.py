from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    # url pour les produits par category
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),

    # url pour afficher les details de chque produit
    path('category/<slug:category_slug>/<slug:product_slug>', views.product_detail, name='product_detail'),
    # url pour rechercher les produits
    path('search/', views.search, name='search'),

    # url pour soumettre un commentaire
    path('submit_reviews/<int:product_id>/', views.submit_reviews, name='submit_reviews'),


]