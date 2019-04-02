from django.test import TestCase
from django.utils import timezone
from django.core.files import File
from sandwish_app.models import User, Wishlist, Gift, Contribution

class TestModels(TestCase):
    """
    Tests project models.
    """

# - INITIALIZATION METHODS ----------------------------------------------------------------

    def create_user(self, username, password="satestnd", email="user@sandwish.com", first_name="sandwish", last_name="appweb"):
        return User.objects.create(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

    def create_wishlist(self, title="some title", description="some description"):
        user = self.create_user("user1")
        return Wishlist.objects.create(title=title, description=description, fk_user=user)

    def create_gift(self, name="some name", image=None, price=10.0, link="", validated=False):
        wishlist = self.create_wishlist()
        return Gift.objects.create(name=name, image=image, price=price, link=link, validated=validated, fk_wishlist=wishlist)

    def create_contribution(self, value=10.0):
        user = self.create_user("user2")
        gift = self.create_gift()
        return Contribution.objects.create(value=value, fk_user=user, fk_gift=gift)

# - TEST METHODS ----------------------------------------------------------------

    def test_user_creation(self):
        user = self.create_user("user3")
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.__str__(), user.username)

    def test_wishlist_creation(self):
        wishlist = self.create_wishlist()
        self.assertTrue(isinstance(wishlist, Wishlist))
        self.assertEqual(wishlist.__str__(), wishlist.title)

    def test_gift_creation(self):
        gift = self.create_gift()
        self.assertTrue(isinstance(gift, Gift))
        self.assertEqual(gift.__str__(), gift.name)

    def test_contribution_creation(self):
        contribution = self.create_contribution()
        self.assertTrue(isinstance(contribution, Contribution))
        self.assertEqual(contribution.__str__(), str(contribution.value))