from django.contrib import admin
from rango.models import Category , Page ,ProfilUser

class PageAdmin(admin.ModelAdmin):
	 list_display = ('title', 'category', 'url')   
	 fieldsets = [
              (None,               {'fields': ['category']}),
              ('other informations', {'fields': ['title','url','views'], 'classes': ['collapse']}),
    	      ]

admin.site.register(Category)
admin.site.register(Page,PageAdmin)

admin.site.register(ProfilUser)
