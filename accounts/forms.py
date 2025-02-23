'''from django.forms import forms
from .models import *

# Creationnde notre formulaire
#class RegistrationForm(forms.ModelForms):
class RegistrationForm(forms.ModelForm):


    password = forms.ChardFields(wiget=forms.PasswordInput(attrs={
        'placeholder':"Mot de passe"
    }))

    confirm_password = forms.ChardFields(wiget=forms.PasswordInput(attrs={
        'placeholder':"Confirmer le mot de passe"
    }))
    class Meta:
        model = Account
        fields = ('nom', 'prenom', 'phone_number','email', 'password')



def __init__(self, *args, **kwargs):
    super(RegistrationForm, self).__init__(*args, **kwargs)

    self.fields['nom'].widget.attrs['placeholder'] = 'Entrez votre nom'
    self.fields['prenom'].widget.attrs['placeholder'] = 'Entrez votre prenom'

    self.fields['phone_number'].widget.attrs['placeholder'] = 'Entrez votre numero de telephone'

    self.fields['email'].widget.attrs['placeholder'] = 'Entrez votre addresse email'

    for field in self.fields:
        self.fields[field].widget.attrs['class'] = 'form-control' '''


from typing import Any
from django import forms
from .models import Account, UserProfile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':"Mot de passe"
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':"Confirmer le mot de passe",
        'class':'form-control'
    }))

    # cette fonction permet de nettoyer les champs password apres l'envoi des donnees
    def clean(self) :
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        #verifiction de la conformite des mots de passe
        if password != confirm_password:
            raise forms.ValidationError(
                "Les mots de passe ne correspondent pas"
            )


    class Meta:
        model = Account
        fields = ('nom', 'prenom', 'phone_number', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['nom'].widget.attrs['placeholder'] = 'Entrez votre nom'
        self.fields['prenom'].widget.attrs['placeholder'] = 'Entrez votre prénom'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Entrez votre numéro de téléphone'
        self.fields['email'].widget.attrs['placeholder'] = 'Entrez votre adresse email'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'




# formulaire de l'utilisateur 
class UserForm(forms.ModelForm):
	class Meta:
		model = Account 
		fields = ('nom', 'prenom', 'phone_number')

	def __init__(self, *args, **kwargs):
		super(UserForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'
			
# formulaire du profile utilisateur 
class UserProfileForm(forms.ModelForm):
	profile_picture = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
	class Meta:
		model = UserProfile 
		fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture')

	def __init__(self, *args, **kwargs):
		super(UserProfileForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'