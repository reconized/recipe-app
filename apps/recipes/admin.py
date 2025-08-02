from django.contrib import admin
from django.contrib.admin.models import LogEntry
from apps.recipes.models.category import Category
from apps.recipes.models.recipe import Recipe
from apps.recipes.models.ingredient import Ingredient
from apps.recipes.models.instruction import Instruction

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

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Instruction)
