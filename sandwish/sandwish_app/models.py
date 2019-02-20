from django.db import models

# - USER MODEL -----------------------------------------------------------------

class User(models.Model):
    username = models.CharField(max_length=32)
    firstname = models.CharField(max_length=32)
    lastname = models.CharField(max_length=32)
    email = models.CharField(max_length=128)

    def __str__(self):
        return self.firstname + self.lastname

# - WISHLIST MODEL -------------------------------------------------------------

class Wishlist(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()

    user_id = models.ForeignKey('User', on_delete = models.CASCADE)

    def __str__(self):
        return self.title

# - GIFT MODEL -----------------------------------------------------------------

class Gift(models.Model):
    name = models.CharField(max_length=128)
    image = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    link = models.CharField(max_length=256)
    validated = models.BooleanField(default=False)

    user = models.ForeignKey('Wishlist', on_delete = models.CASCADE)

    def __str__(self):
        return self.name

# - CONTRIBUTION MODEL ---------------------------------------------------------

class Contribution(models.Model):
    value = models.DecimalField(max_digits=8, decimal_places=2)

    gift = models.ForeignKey('Gift', on_delete = models.CASCADE)
    user = models.ForeignKey('User', on_delete = models.CASCADE)

    def __str__(self):
        return self.value
