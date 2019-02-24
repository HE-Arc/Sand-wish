from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic, View
from django.urls import reverse_lazy

# for signup
from django.contrib.auth import login, authenticate
from .models import User, Wishlist
from sandwish_app.forms import SignUpForm


def index(request):
    context = {}
    return render(request, "sandwish_app/index.html", context)

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("index")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})

class ProfileView(generic.DetailView):
    model=User
    slug_field = "username"
    template_name = "sandwish_app/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profiles_user = context["object"]

        context["wishlists"] = Wishlist.objects.filter(user_id=profiles_user.id)

        return context

class WhishlistView(generic.ListView):
    template_name = "sandwish_app/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # profiles_user = context["object"]

        # context["wishlists"] = Wishlist.objects.filter(user_id=profiles_user.id)

        return context

    def get_queryset(self):
        username = self.kwargs["username"]
        pk = self.kwargs["pk"]

        whishlists_user = User.objects.get(username=username)
        wishlist = Wishlist.objects.filter(id=pk).filter(user_id=whishlists_user.id)
        return wishlist