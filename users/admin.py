from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Поле для отображения в списке пользователей
    list_display = ('email', 'is_staff', 'is_active',)

    # Поля, по которым можно искать
    search_fields = ('email',)

    # Фильтры в боковой панели
    list_filter = ('is_staff', 'is_active',)

    # Настройка формы редактирования пользователя
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'avatar', 'phone', 'country')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Настройка формы добавления нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    # Поля, которые будут автоматически заполняться и недоступны для редактирования
    readonly_fields = ('date_joined', 'last_login')

    ordering = ('email',)



from django.contrib import admin

# Register your models here.
