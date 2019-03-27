from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Wishlist
from django.forms import RegexField
from django.utils.translation import ugettext_lazy as _

username_regex_field = RegexField(label = "Username",
                                    max_length = 30,
                                    regex = r"^[\w-]+$",
                                    help_text = _("Required. 30 characters or fewer. Letters, digits, - and _ only."))

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    username = username_regex_field

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class SearchForm():
    username = username_regex_field

class WishlistCreationForm(forms.ModelForm):
    title = forms.CharField(label="", max_length=128, widget=forms.TextInput(attrs={
                            'class': "form-control",
                            'placeholder' : "Wishlist's name"}))
    description = forms.CharField(label="", widget=forms.Textarea (attrs={
                            'class': "form-control",
                            'placeholder' : "Wishlist's description"}))

    class Meta:
        model = Wishlist
        fields = ["title", "description"]
