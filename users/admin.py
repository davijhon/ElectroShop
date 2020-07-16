from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import UserProfile


CustomUser = get_user_model()



class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
	add_form = CustomUserCreationForm
	form = CustomUserChangeForm
	model = CustomUser
	list_display = ['email', 'username',]

	inlines = (ProfileInline, )

	def get_inline_instances(self, request, obj=None):
		if not obj:
			return list()
		return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.register(CustomUser, CustomUserAdmin)



# class UserProfileAdmin(admin.ModelAdmin):
# 	list_display = ['user_name', 'shipping_address',#  'billing_address', 'shipping_country', 'shipping_zip']


# admin.site.register(UserProfile, UserProfileAdmin)