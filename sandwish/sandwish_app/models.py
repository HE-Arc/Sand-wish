from django.db import models
from django.contrib.auth.models import User

# - WISHLIST MODEL -------------------------------------------------------------

class Wishlist(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()

    fk_user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.title

# - GIFT MODEL -----------------------------------------------------------------

class Gift(models.Model):
    name = models.CharField(max_length=128)
    image = models.CharField(max_length=128, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    link = models.CharField(max_length=256, blank=True)
    validated = models.BooleanField(default=False)

    fk_wishlist = models.ForeignKey('Wishlist', on_delete = models.CASCADE)

    def __str__(self):
        return self.name

# - CONTRIBUTION MODEL ---------------------------------------------------------

class Contribution(models.Model):
    value = models.DecimalField(max_digits=8, decimal_places=2)

    fk_gift = models.ForeignKey('Gift', on_delete = models.CASCADE)
    fk_user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.value)
