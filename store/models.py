from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg
from django.db.models import Count


# Create your models here.

class Product(models.Model):
    product_name =models.CharField(max_length=200, unique= True)
    slug =models.SlugField(max_length=200, unique= True)
    description = models.TextField(max_length=1000, blank= True)
    images = models.ImageField(upload_to='photos/products')
    price = models.IntegerField()

    stock = models.IntegerField()
    is_available =models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add = True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name= 'product'
        verbose_name_plural = 'products'

    def __str__(self) -> str:
        return self.product_name

    # Methoque aui renvoi l'url
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])


        # Pour afficher le nombre d'etaoiles sous le titre du produit
    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0 
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg   

        # fonction pour compter le ombre de commentaire sur chaque produit
    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0 
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

# cette classe permet de separer les variatons 
class VariationManager(models.Manager):
    # Cette methode concerne uniquement la variation color
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

 # Cette methode concerne uniquement la variation color
    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)
     


# cette classe permet d'enregistrer les variations de nos produits comme :
    #  La couleur des caussures
    #   La taille des chaussures

variation_category_choice = (
     ('color', 'color'),
     ('size',  'size'),
)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=200, choices=variation_category_choice)
    variation_value = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    # Pour une liaison
    objects =VariationManager()

    def __str__(self):
        return self.variation_value


class ReviewRating(models.Model):#    Table pour les commentaires
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
	subject = models.CharField(max_length=1000, blank=True)#          sujet
	review = models.TextField(max_length=500, blank=True) # commentaire
	rating = models.FloatField()    # notation
	ip = models.CharField(max_length=30, blank=True)
	status = models.BooleanField(default=True)
	created_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.subject


class ProductGallery(models.Model):# table pour la gallery photo (plusieurs images pour le meme produit)
	product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='store/products', max_length=500)

	def __str__(self):
		return self.product.product_name

	class Meta:
		verbose_name = 'productgallery'
		verbose_name_plural = 'product gallery'  


