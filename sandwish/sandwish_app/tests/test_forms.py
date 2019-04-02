from django.test import TestCase
from sandwish_app.forms import SignUpForm, SearchForm, WishlistCreationForm, GiftCreationForm
from django.contrib.auth.models import User
from sandwish_app.models import Wishlist, Gift, Contribution

class TestForms(TestCase):
    """
    Tests project forms.
    """

    def test_invalid_form_signup(self):
        u = User.objects.create(username="sandwish", password="appweb", email="user||%", first_name="sandwish", last_name="appweb")
        data = {"username": u.username, "password": u.password, "email": u.email, "first_name": u.first_name, "last_name": u.last_name}
        form = SignUpForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_form_wishlist(self):
        u = User.objects.create(username="sandwish", password="satestnd", email="user@sandwish.com", first_name="sandwish", last_name="appweb")
        w = Wishlist.objects.create(fk_user=u, title="sandwish", description="sandwish")
        data = {"title":w.title, "description":w.description}
        form = WishlistCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_wishlist(self):
        u = User.objects.create(username="sandwish", password="satestnd", email="user@sandwish.com", first_name="sandwish", last_name="appweb")
        w = Wishlist.objects.create(fk_user=u, title="", description="")
        data = {"title":w.title, "description":w.description}
        form = WishlistCreationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_form_gift(self):
        u = User.objects.create(username="sandwish", password="satestnd", email="user@sandwish.com" , first_name="sandwish" , last_name="appweb")
        w = Wishlist.objects.create(fk_user=u, title="sandwish", description="sandwish")
        g = Gift.objects.create(fk_wishlist=w, name="sandwish", price="199")
        data = {"name":g.name, "price":g.price}
        form = GiftCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_gift(self):
        u = User.objects.create(username="sandwish", password="satestnd", email="user@sandwish.com" , first_name="sandwish" , last_name="appweb")
        w = Wishlist.objects.create(fk_user=u, title="sandwish", description="sandwish")
        g = Gift.objects.create(fk_wishlist=w, name="", price="-100")
        data = {"name":g.name, "price":g.price}
        form = GiftCreationForm(data=data)
        self.assertFalse(form.is_valid())
