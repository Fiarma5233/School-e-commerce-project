from django.db import models
# importation du model Product depuis l'app store
from store.models import *
from accounts.models import *

# Create your models here.


#Cette classe contient l'id du panier et la date d'ajout au panier
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.cart_id
    


# Cette classe est pour chaque produit du panier
class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)# Pour lier chq panier  a un compte utilisateur
    product= models.ForeignKey(Product, on_delete=models.CASCADE) # cle secondaire faisant reference au produit 
    # cle secondaire faisant reference au panier car chaque produit appartient (est mis dans un panier bien specifique)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True) 
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True) # pour dire si le produit est pris ou pas

    # cette fonction permet de calculer le prix total de chaque article
    def sub_total(self):
        return self.product.price * self.quantity
    
    def __unicode__(self):
        return self.product