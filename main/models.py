from ckeditor.fields import RichTextField
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    image = models.ImageField(_('Image'), upload_to='pics', null=True, blank=True)
    phone = models.CharField(_('Phone'), max_length=20, null=False, blank=False, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'), )
    is_active = models.BooleanField(_('active'), default=False, help_text=_(
        'Designates whether this user should be treated as active.'), )
    date_joined = models.DateTimeField(_('Date joined'), default=timezone.now)
    user_type = models.CharField(choices=enums.USER_TYPE, max_length=50)
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
    about = models.TextField(_('About'), null=True, blank=True)

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

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)


def HomePage_dir(instance, filename):
    return 'homepage/{0}/{1}'.format(instance.title, filename)

def AboutUs_dir(instance, filename):
    return 'aboutus/{0}/{1}'.format(instance.title, filename)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='socialmedia')
    facebook = models.URLField(max_length=200, null=True, blank=True)
    instagram = models.URLField(max_length=200, null=True, blank=True)
    twitter = models.URLField(max_length=200, null=True, blank=True)
    linkedin = models.URLField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = 'Social Media'
        verbose_name_plural = 'Social Media'


class Type(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Category(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class City(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Listing(TimeStampedModel):
    title = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User,related_name="listing_user", on_delete=models.CASCADE,  null=True, blank=True)
    # type = models.CharField(max_length=255, choices=[('Rent', 'Rent'), ('Sale', 'Sale')])
    type = models.ForeignKey(Type, related_name='listing_type', on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # category = models.CharField(max_length=255, choices=[('House', 'House'), ('Apartment', 'Apartment'), ('Hotel', 'Hotel'), ('Villa', 'Villa'), ('Office', 'Office')])
    category = models.ForeignKey(Category, related_name='all_category', on_delete=models.CASCADE, null=True, blank=True)
    keywords = models.CharField(max_length=255)
    # locations
    address = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    city = models.ForeignKey(City, related_name='listing_city', on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(_('Email address'), unique=True)
    phone = models.CharField(_('Phone'), max_length=20, null=False, blank=False, unique=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    # Listing Details
    area = models.CharField(max_length=255)
    accommodation = models.CharField(max_length=255)
    yard_size = models.CharField(max_length=255)
    bedrooms = models.CharField(max_length=255)
    bathrooms = models.CharField(max_length=255)
    garage = models.CharField(max_length=255)
    details_text = models.TextField(_('Details'), null=True, blank=True)
    wi_fi = models.BooleanField(default=False)
    pool = models.BooleanField(default=False)
    security = models.BooleanField(default=False)
    laundry_room = models.BooleanField(default=False)
    equipped_kitchen = models.BooleanField(default=False)
    air_conditioning = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    # Rooms
    room_title = models.CharField(max_length=255)
    additional_room = models.CharField(max_length=255)
    room_details = models.TextField()
    room_image = models.ImageField(null=True, blank=True, upload_to='room_image/')
    # Amenities
    air_conditioner = models.BooleanField(default=False)
    tv_inside = models.BooleanField(default=False)
    ceramic_bath = models.BooleanField(default=False)
    microwave = models.BooleanField(default=False)
    # Content Widgets
    video_presentation = models.BooleanField(default=False)
    video_youtube = models.URLField(max_length=200, null=True, blank=True)
    video_vimeo = models.URLField(max_length=200, null=True, blank=True)
    document = models.FileField(null=True, blank=True, upload_to='Document/')
    google_mapp = models.BooleanField(default=False)
    contact_form = models.BooleanField(default=False)
    mortage_calulator = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from=['title'], null=True, blank=True)

    class Meta:
        verbose_name = 'Listing'
        verbose_name_plural = 'Listing'

    def __str__(self):
        return self.title



class Slider(TimeStampedModel):
    title = models.CharField(_('Title'), max_length=255)
    sub_title = models.CharField(_('Sub Title'), max_length=255, null=True, blank=True)
    description = models.TextField(_('Description'))
    image = models.ImageField(_(' Image'), null=True, blank=True, upload_to=HomePage_dir)
    heading = models.CharField(_('Heading'), max_length=255, null=True, blank=True)
    sub_description = models.TextField(_('Sub Description'))
    location = models.TextField(_('location'), null=True, blank=True)
    slider_image = models.ImageField(_(' Slider Image'), null=True, blank=True, upload_to=HomePage_dir)
    rating = models.IntegerField(_('Rating'), null=True, blank=True)
    price = models.FloatField(_('Price'), null=True, blank=True)
    slug = AutoSlugField(populate_from=['title'], null=True, blank=True)

    class Meta:
        verbose_name = _('Slider')
        verbose_name_plural = _('Sliders')

    def __str__(self):
        return self.title


class AboutUs(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    sub_title = models.CharField(_('Sub Title'), max_length=255, null=True, blank=True)
    description = models.TextField(_('Description'))
    image = models.ImageField(_(' Image'), null=True, blank=True, upload_to=AboutUs_dir)

    class Meta:
        verbose_name = _('AboutUs')
        verbose_name_plural = _('AboutUs')

    def __str__(self):
        return self.title

class CompanyStory(models.Model):
    title = models.CharField(_('  Title'), max_length=255, null=True,blank=True)
    heading = models.CharField(_(' Heading'), max_length=255,null=True,blank=True)
    description = RichTextField(null=True, blank=True)
    image = models.ImageField(_('Company image'), upload_to='uploads/', null=True,blank=True)
    about = models.TextField(_('About'),null=True,blank=True)


    class Meta:
        verbose_name = 'CompanyStory'
        verbose_name_plural = 'CompanyStory'

    def __str__(self):
        return self.title

class CompanySupport(TimeStampedModel):
    title = models.CharField(_('  Title'), max_length=255, null=True,blank=True)
    description = RichTextField(null=True, blank=True)


    class Meta:
        verbose_name = 'CompanySupport'
        verbose_name_plural = 'CompanySupport'

    def __str__(self):
        return self.title


class Team(models.Model):
    fullname = models.CharField(_("Team Fullname"), max_length=255)
    image = models.ImageField(_('image'), upload_to='uploads/', null=True,blank=True)
    degination = models.CharField(_('Destination'), max_length=255)
    aboutus = models.TextField()
    facebook = models.URLField(max_length=200, null=True, blank=True)
    instagram = models.URLField(max_length=200, null=True, blank=True)
    twitter = models.URLField(max_length=200, null=True, blank=True)
    linkedin = models.URLField(max_length=200, null=True, blank=True)


    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Team'

    def __str__(self):
        return self.fullname

class Booking(TimeStampedModel):
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='booking')
    name = models.CharField(_('Name'),max_length=255,null=True, blank=True)
    phone = models.CharField(_('Phone'),max_length=255,null=True, blank=True)
    email = models.EmailField(_('Email'),max_length=50, unique=True,null=True, blank=True)
    is_booked = models.BooleanField(_('Booking'), default=False )
    slug = AutoSlugField(populate_from=['id'], null=True, blank=True)


    def __str__(self):
        return self.listing.title


    class Meta:
        verbose_name = _('Booking')
        verbose_name_plural = _('Bookings')
        ordering = ('-id',)

