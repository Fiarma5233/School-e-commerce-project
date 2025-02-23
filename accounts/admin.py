from django.contrib import admin
from .models import  Account, UserProfile
from  django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

# Register your models here.


class AccountAdmin(UserAdmin):
    # Champs qu'on souhaite afficher
    list_display = (
        'email',
        "nom",
        "prenom",
        "username",
        "last_login",
        "date_joined",
        "is_active"

    )

    # Ajouter un lien sur les champs qu'on veut
    list_display_links =('email', 'nom', 'prenom')

    # Lire seulement un champ
    readonly_fields = ('last_login', 'date_joined')

    # Ordre d'affichage(du plus recent au plus ancien)
    ordering =('-date_joined',)

    # Affichage horirontal des champs
    filter_horizontal = ()
    list_filter = ()
    fieldsets =()



class UserProfileAdmin(admin.ModelAdmin):
	def thumbnail(self, object):
		return format_html('<img src="{}" width="30" style="border-radius:50%;" >'.format(object.profile_picture.url))
	thumbnail.short_description = 'Profile Picture'
	list_display = ('thumbnail','user', 'city', 'state', 'country')

admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)