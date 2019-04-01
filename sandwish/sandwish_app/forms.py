from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Wishlist, Gift
from django.forms import RegexField, URLField, ImageField
from django.utils.translation import ugettext_lazy as _

username_regex_field = RegexField(label = _("Username"),
                                    max_length = 30,
                                    regex = r"^[\w-]+$",
                                    help_text = _("Required. 30 characters or fewer. Letters, digits, - and _ only."),
                                    widget=forms.TextInput(attrs={"class": "form-control"}))

class SignUpForm(UserCreationForm):
    """
    Sign up formular.
    """
    first_name = forms.CharField(max_length=30, required=False, help_text=_("Optional."),
                                    widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(max_length=30, required=False, help_text=_("Optional."),
                                    widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(max_length=254, help_text=_("Required. Inform a valid email address."),
                                    widget=forms.EmailInput(attrs={"class": "form-control"}))
    username = username_regex_field

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

class SearchForm():
    """
    Search formular.
    """
    username = username_regex_field

class WishlistCreationForm(forms.ModelForm):
    """
    Wishlist creation formular.
    """
    title = forms.CharField(label="", max_length=128, widget=forms.TextInput(attrs={
                            "class": "form-control",
                            "placeholder" : "Wishlist's name"}))
    description = forms.CharField(label="", widget=forms.Textarea (attrs={
                            "class": "form-control",
                            "placeholder" : "Wishlist's description",
                            "rows" : "3"}))

    class Meta:
        model = Wishlist
        fields = ["title", "description"]

class GiftCreationForm(forms.ModelForm):
    """
    Gift creation formular.
    """
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    price = forms.CharField(widget=forms.NumberInput(attrs={"class": "form-control"}))
    image = ImageField(label=_("Image"), required=False)
    link = URLField(label=_("Link"), required=False, widget=forms.URLInput(attrs={"class": "form-control"}))

    class Meta:
        model = Gift
        fields = ["name", "image", "price", "link"]
