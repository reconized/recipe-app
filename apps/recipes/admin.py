from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin.models import LogEntry
from apps.recipes.models.category import Category
from apps.recipes.models.recipe import Recipe
from apps.recipes.models.ingredient import Ingredient
from apps.recipes.models.instruction import Instruction
from apps.recipes.models.user_profile import Profile

# Register your models here.
@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj = None):
        return False
    
    def has_delete_permission(self, request, obj = None):
        return False
        
    def has_add_permission(self, request):
        return None
    
class CategoryCustomAdmin(admin.ModelAdmin):
    search_fields = ['name']
    show_full_result_count = True
    list_filter = ['name']
    list_display = ['name']

admin.site.register(Category, CategoryCustomAdmin)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Instruction)
