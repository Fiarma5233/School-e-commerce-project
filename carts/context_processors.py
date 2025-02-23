
from .models import *
from .views import _cart_id

# cette vue est pour afficher le nombre d'articles du panier au nivau de la nav-bar
def counter(request):
    cart_count = 0 # initialisation  de la varible 
    if 'admin' in request.path:
        return {}
    
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated: # si l'utilisateur est authentifie
                cart_items = CartItem.objects.all().filter(user=request.user) # on filtre les articles de l'utilisateur connecte
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])

            for cart_item in cart_items:
                cart_count +=cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
        return dict(cart_count=cart_count)
