from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from main.models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

# Register your models here.

@admin.register(HomePage)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image')


admin.site.register(Property)

@admin.register(Navbar)
class DisposalAdmin(DraggableMPTTAdmin):

    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 20
    list_display = ('tree_actions', 'indented_title', 'parent','name')
    list_display_links = ('name',)


admin.site.register(Blog)

admin.site.register(News)



class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'phone', 'is_staff','image')
    ordering = ('date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password','image','username')}),
        (_('Personal info'), {'fields': ('phone',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'username', 'phone')


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
