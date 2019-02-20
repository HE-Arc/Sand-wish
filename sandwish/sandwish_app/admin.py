from django.contrib import admin
from .models import User, Wishlist, Gift, Contribution

admin.site.register(User)
admin.site.register(Wishlist)
admin.site.register(Gift)
admin.site.register(Contribution)
