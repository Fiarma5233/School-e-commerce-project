
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
	def create_user(self, nom, prenom, username, email, password=None):
		if not email:
			raise valueError("L'utilisateur doit avoir une adresse email")

		if not username:
			raise valueError("L'utilisateur doit avoir un nom")

		user = self.model(
			email = self.normalize_email(email),
			username = username,
			nom = nom,
			prenom = prenom,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user 

	def create_superuser(self, nom, prenom, email, username, password):
		user = self.create_user(
			email = self.normalize_email(email),
			username = username,
			password = password,
			nom = nom,
			prenom = prenom,
		)
		user.is_admin = True
		user.is_active = True 
		user.is_staff = True 
		user.is_superadmin = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
	nom = models.CharField(max_length=50)
	prenom = models.CharField(max_length=50)
	username = models.CharField(max_length=50, unique=True)
	email = models.EmailField(max_length=100, unique=True)
	phone_number = models.CharField(max_length=50)

	#requise
	date_joined = models.DateTimeField(auto_now_add=True)
	last_login = models.DateTimeField(auto_now_add=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=False)
	is_superadmin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'nom', 'prenom']

	objects = MyAccountManager()

	def full_name(self):
		return f'{self.nom} {self.prenom}'

	def __str__(self):
		return self.email 

	def has_perm(self, perm, obj=None):
		return self.is_admin 

	def has_module_perms(self, add_label):
		return True

# Table de profile utilisateur
class UserProfile(models.Model):
	user = models.OneToOneField(Account, on_delete=models.CASCADE)
	address_line_1 = models.CharField(blank=True, max_length=100)
	address_line_2 = models.CharField(blank=True, max_length=100)
	profile_picture = models.ImageField(blank=True, upload_to='userprofile')
	city = models.CharField(blank=True, max_length=20)
	state = models.CharField(blank=True, max_length=20)
	country = models.CharField(blank=True, max_length=20)

	def __str__(self):
		return self.user.nom

	def full_address(self):
		return f'{self.address_line_1} {self.address_line_2}'
	
	def get_profile_picture_url(self):
		if self.profile_picture:
			return self.profile_picture.url
		else:
			# Remplacez 'default-avatar.jpg' par le nom de votre avatar par défaut
			#return '/static/images/avatars/avatar1.png'
			return 'media/avatars/default_image_pro.png'

























'''from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, nom, prenom, username, email, password=None):
        if not email:
            raise ValueError("L'utilisateur doit avoir une addresse email")

        if not username:
            raise ValueError("L'utilisateur doit avoir une addresse email")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            nom = nom,
            prenom = prenom
        )

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    ## Creation de superuser

    def create_superuser(self, nom, prenom, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            nom=nom,
            prenom=prenom

        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=50)



    #requise
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


    USERNAME_FIELD = 'email' # ie le email sera le username
    REQUIRED_FIELDS = ['username', 'nom', 'prenom']

    objects = MyAccountManager()

    def __str__(self) -> str:
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True'''

