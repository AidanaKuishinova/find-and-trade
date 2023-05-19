import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password


class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, name: str, surname: str, password=None):
        if not email:
            raise ValueError("email field is mandatory")
        elif not name:
            raise ValueError("Name field is mandatory")
        elif not surname:
            raise ValueError("Surname field is mandatory")

        user = self.model(
            email=email,
            name=name,
            surname=surname
        )
        user.password = make_password(password)

        profile = Profile()
        profile.save()

        user.profile = profile
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, name: str, surname: str, password=None):
        user = self.create_user(
            email=email,
            name=name,
            surname=surname,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def user_profile_directory_path(instance, filename: str) -> str:
    return f'profile_images/{instance.id}/{filename}'

def user_image_directory_path(instance, filename: str) -> str:
    return f'ad_images/{instance.id}/{filename}'

class Role(models.Model):
    OWNER = "Предприниматель"
    SUPPLIER = "Поставщик"
    choices = [
        (OWNER, "Предприниматель"),
        (SUPPLIER, "Поставщик"),
    ]

class Profile(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    city = models.CharField(max_length=15, blank=True, null=True, verbose_name="City")
    date_of_birth = models.DateField(max_length=15, blank=True, null=True, verbose_name='Date of birth')
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Phone number")
    role = models.CharField(max_length=200, choices=Role.choices, verbose_name="Role")
    image_link = models.ImageField(upload_to=user_profile_directory_path, blank=True, null=True,
                                   verbose_name="Profile image")


class CustomUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True, verbose_name="ID")

    email = models.EmailField(unique=True, verbose_name="Email")
    name = models.CharField(max_length=26, verbose_name="Name")
    surname = models.CharField(max_length=26, verbose_name="Surname")

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Profile")

    reset_password_token = models.UUIDField(blank=True, null=True, default=None, verbose_name="Reset password token")

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True, verbose_name="Last login")

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["name", "surname"]

    objects = CustomUserManager()


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

def user_and_order_directory_path(instance, filename: str) -> str:
    return f'order/{instance.order.creator.username}/{instance.order.id}/{filename}'


def generate_upload_path(instance, filename:str) -> str:
    # Generate a unique filename for the uploaded file
    return f'ad/{instance.user.email}/{instance.id}/{filename}'

class Ad(models.Model):
    user= models.ForeignKey(CustomUser, blank=False, null=False, on_delete=models.CASCADE, related_name='creator')
    title= models.CharField(max_length=50, verbose_name="Title")
    company_name= models.CharField(max_length=50, blank=True, null=True, verbose_name="Company_name")
    description= models.TextField(verbose_name="Description")
    image_link = models.ImageField(upload_to=user_image_directory_path, blank=True, null=True,
                                   verbose_name="Ad image")
    cost= models.FloatField(verbose_name="Cost")
    responders= models.ManyToManyField(CustomUser)
    create_date = models.DateField(auto_now_add=True, verbose_name="Creation date")
    edit_date = models.DateField(auto_now=True, verbose_name="Edit date")
    is_active = models.BooleanField(default=True, verbose_name="Active")


    def __str__(self):
        return self.title

class FavoriteAd(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'ad')