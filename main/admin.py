from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from main.models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

# Register your models here.

@admin.register(HomePage)
class HomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image')



@admin.register(Navbar)
class DisposalAdmin(DraggableMPTTAdmin):

    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 20
    list_display = ('tree_actions', 'indented_title', 'parent','name')
    list_display_links = ('name',)


admin.site.register(Blog)

admin.site.register(News)
@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('id','title')


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'phone', 'is_staff','image')
    ordering = ('date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password','image','username')}),
        (_('Personal info'), {'fields': ('phone',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions' ,'user_type')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'phone'),
        }),
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'username', 'phone')


admin.site.register(User, CustomUserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name','last_name', 'about','city')

@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ('id','facebook','instagram')


@admin.register(City)
class CityAdmin(DraggableMPTTAdmin):

    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 20
    list_display = ('tree_actions', 'indented_title', 'parent','name')
    list_display_links = ('name',)

@admin.register(Type)
class CategoryAdmin(DraggableMPTTAdmin):

    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 20
    list_display = ('tree_actions', 'indented_title', 'parent','name')
    list_display_links = ('name',)

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):

    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 20
    list_display = ('tree_actions', 'indented_title', 'parent','name')
    list_display_links = ('name',)




admin.site.register(Slider)
admin.site.register(CompanyStory)
admin.site.register(AboutUs)
admin.site.register(CompanySupport)
admin.site.register(Team)
admin.site.register(Booking)