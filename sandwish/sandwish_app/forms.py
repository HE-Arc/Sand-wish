from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Wishlist


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

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
