from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic, View
from django.urls import reverse_lazy

# for signup
from django.contrib.auth import login, authenticate
from .models import User, Wishlist, Gift
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

def login_redirect(request):
    return redirect("profile", request.user.username)

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
    template_name = "sandwish_app/wishlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["wishlists_user"] = context["object_list"][0]
        context["wishlist"] = context["object_list"][1]

        context["gifts"] = Gift.objects.filter(wishlist_id=context["wishlist"].id)

        return context

    def get_queryset(self):
        username = self.kwargs["username"]
        pk = self.kwargs["pk"]

        whishlists_user = User.objects.get(username=username)
        wishlist = Wishlist.objects.get(id=pk, user_id=whishlists_user.id)
        return whishlists_user, wishlist


class GiftDelete(generic.DeleteView):
    model = Gift

    def get_success_url(self):
        removed_gift = self.object
        wishlist = removed_gift.wishlist_id
        user = wishlist.user_id
        return reverse_lazy("whishlist", kwargs={"username" : user.username, "pk" : wishlist.id})

class GiftCreateView(generic.CreateView):
    model = Gift
    fields = ["name", "price", "image", "link"]

    def form_valid(self, form):
        form.instance.wishlist_id = Wishlist.objects.get(id=self.kwargs.get("pk")) # add foreign key
        return super(GiftCreateView, self).form_valid(form)

    def get_success_url(self):
        new_gift = self.object
        wishlist = new_gift.wishlist_id
        user = wishlist.user_id
        return reverse_lazy("whishlist", kwargs={"username": user.username, "pk": wishlist.id})
