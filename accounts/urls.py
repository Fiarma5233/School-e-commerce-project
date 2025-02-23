from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"), # Chemin permettant d'aller vers le site administrateur
    path("login/", views.login, name="login"), # Chemin permettant d'aller vers le site administrateur
    path("logout/", views.logout, name="logout"), # Chemin permettant d'aller vers le site administrateur
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('', views.dashboard, name='dashboard'),

    path('dashboard/', views.dashboard, name='dashboard'), # url pour le dashboard
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),# Vue pour mot de passe oublie

    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),# Vue pour confirmer la renitiaisation du password
    path('resetPassword/', views.resetPassword, name='resetPassword'),# Vue pour renisialiser le password
    path('my_orders/', views.my_orders, name='my_orders'),# pour mes commandes au niveau du dashboard
    path('edit_profile/', views.edit_profile, name='edit_profile'), # pour modifier le profile utilisateur
    path('change_password/', views.change_password, name='change_password'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
 


]