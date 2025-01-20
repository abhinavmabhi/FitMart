from django.contrib import admin
from store.models import Brand,Flavour,tags,Suppliment_Category,Equipment_category,Suppliment,Equipments,CustomUser

admin.site.register(CustomUser)
admin.site.register(Brand)
admin.site.register(Flavour)
admin.site.register(tags)
admin.site.register(Suppliment_Category)
admin.site.register(Equipment_category)
admin.site.register(Suppliment)
admin.site.register(Equipments)
