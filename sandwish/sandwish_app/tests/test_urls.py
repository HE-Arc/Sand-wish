from django.test import SimpleTestCase
from django.urls import reverse, resolve
from sandwish_app.views import index, search, ProfileView, WishlistView, WishlistDeleteView, GiftCreateView, GiftDeleteView, GiftValidateView, contribute

class TestUrls(SimpleTestCase):
    """
    Tests project urls.
    """

    def test_index_url_resolves(self):
        url = reverse("index")
        self.assertEquals(resolve(url).func, index)
    
    def test_search_url_resolves(self):
        url = reverse(search)
        self.assertEquals(resolve(url).func, search)
    
    def test_index_search_url_resolves(self):
        url = reverse("index_search", args=["some_username"])
        self.assertEquals(resolve(url).func, index)
    
    def test_profile_url_resolves(self):
        url = reverse("profile", args=["some_username"])
        self.assertEquals(resolve(url).func.view_class, ProfileView)
    
    def test_wishlist_url_resolves(self):
        url = reverse("wishlist", args=["some_username", 0])
        self.assertEquals(resolve(url).func.view_class, WishlistView)
    
    def test_wishlist_delete_url_resolves(self):
        url = reverse("wishlist-delete", args=["some_username", 0])
        self.assertEquals(resolve(url).func.view_class, WishlistDeleteView)
    
    def test_gift_create_url_resolves(self):
        url = reverse("gift-create", args=["some_username", 0])
        self.assertEquals(resolve(url).func.view_class, GiftCreateView)
    
    def test_gift_delete_url_resolves(self):
        url = reverse("gift-delete", args=["some_username", 0, 0])
        self.assertEquals(resolve(url).func.view_class, GiftDeleteView)
    
    def test_gift_validate_url_resolves(self):
        url = reverse("gift-validate", args=["some_username", 0, 0])
        self.assertEquals(resolve(url).func.view_class, GiftValidateView)
    
    def test_contribution_create_url_resolves(self):
        url = reverse("create-contribution")
        self.assertEquals(resolve(url).func, contribute)