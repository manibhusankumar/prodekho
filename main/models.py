from ckeditor.fields import RichTextField
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from django_extensions.db.fields import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.utils import timezone

from main import enums


# Create your models here.


class UserAccountManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)

    def create_staff_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('Username'), max_length=100, blank=True)
    email = models.EmailField(_('Email address'), unique=True)
    image = models.ImageField(_('Image'),upload_to='pics', null=True, blank=True)
    phone = models.CharField(_('Phone'),max_length=20, null=False, blank=False, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'), )
    is_active = models.BooleanField(_('active'), default=False, help_text=_(
        'Designates whether this user should be treated as active.'), )
    date_joined = models.DateTimeField(_('Date joined'), default=timezone.now)
    is_user = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


    objects = UserAccountManager()
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('User')
        ordering = ['-pk']

    def __str__(self):
        return self.email or self.username

class AddressAbstract(models.Model):
    address = models.TextField(_('Address'), null=True, blank=True)
    street = models.TextField(_('Colony / Street / Locality'), null=True, blank=True)
    city = models.CharField(_('City'), max_length=255, null=True, blank=True)
    district = models.CharField(_('District'), max_length=255, null=True, blank=True)
    state = models.CharField(_('State'), max_length=255, null=True, blank=True)
    country = models.CharField(_('Country'), max_length=255, null=True, blank=True)
    zip_code = models.CharField(_('Zip code'), max_length=10, null=True, blank=True)

    class Meta:
        abstract = True

class UserProfile(AddressAbstract, models.Model):
    first_name = models.CharField(_('First name'), max_length=30, blank=True)
    last_name = models.CharField(_('Last name'), max_length=30, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    gender = models.CharField(_('Gender'), max_length=255, choices=enums.GENDER, null=True, blank=True)
    dob = models.DateField(_('DOB'), null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    about = models.TextField(_('About'),  null=True,blank=True)

    class Meta:
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfile'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = "{} {}".format(self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return self.first_name + " " + self.last_name



def HomePage_dir(instance, filename):
    return 'homepage/{0}/{1}'.format(instance.title, filename)


def Property_dir(instance, filename):
    return 'property_image/{0}/{1}'.format(instance.title, filename)



class HomePage(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'))
    image = models.ImageField(_(' Image'), null=True, blank=True, upload_to=HomePage_dir)

    class Meta:
        verbose_name = _('HomePage')
        verbose_name_plural = _('HomePage')

    def __str__(self):
        return self.title


class Property(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(_(' Image'), null=True, blank=True, upload_to=Property_dir)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.TextField(_('location'), null=True, blank=True)
    li_title = RichTextField()
    author_image = models.ImageField(_('Author Image'), null=True, blank=True, upload_to='uploads/')
    author_name = models.CharField(_('Author Name'), max_length=233, null=True, blank=True)
    rating = models.IntegerField(_('Rating'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    slug = AutoSlugField(populate_from=['title'], null=True, blank=True)

    def __str__(self):
        return self.title


class Navbar(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    urls = models.CharField(max_length=500, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Navbar'
        verbose_name_plural = 'Navbars'

    def __str__(self):
        return self.name

    def get_urls_list(self):
        return self.urls.split(',')


class Blog(TimeStampedModel):
    title = models.CharField(max_length=200)
    image = models.ImageField(_(' Image'), null=True, blank=True, upload_to=Property_dir)
    description = RichTextField()
    author_image = models.ImageField(_('Author Image'), null=True, blank=True, upload_to='uploads/')
    author_name = models.CharField(_('Author Name'), max_length=233, null=True, blank=True)
    slug = AutoSlugField(populate_from=['title'], null=True, blank=True)
    tags = RichTextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

    def __str__(self):
        return self.title

class News(TimeStampedModel):
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'))
    image = models.ImageField(_(' Image'), null=True, blank=True, upload_to='uploads/')

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'

    def __str__(self):
        return self.title


class SocialMedia(models.Model):
    profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='socialmedia')
    facebook = models.URLField(max_length = 200,null=True,blank=True)
    instagram = models.URLField(max_length =200, null=True,blank=True)
    twitter = models.URLField(max_length=200, null=True,blank=True)
    linkedin = models.URLField(max_length=200, null=True,blank=True)

    class Meta:
        verbose_name = 'Social Media'
        verbose_name_plural = 'Social Media'






