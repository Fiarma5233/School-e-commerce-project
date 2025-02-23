'''
    Le context processor et une fonction qui prend une requete comme un argument 
    et renvoie le dictionnaire de donnees comme contexte

'''

from .models import Category


def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)