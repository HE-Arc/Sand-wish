from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic, View
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .forms import WishlistCreationForm#, ContributionForm
import json as json
from django.contrib.auth import login, authenticate
from .models import User, Wishlist, Gift, Contribution
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

def create_contribution(request):
    if request.method == 'POST':
        print("------------------YEAAAAAAAH-------------------")
        value = request.POST.get('value')
        giftId = request.POST.get('giftId')

        gift = Gift.objects.get(id=giftId)

        response_data = {}

        # TODO : check si existe déja et update ou créer en fonction :
        try:
            contribution = Contribution.objects.get(fk_gift=gift.id, fk_user=request.user.id).update(value=value)
            response_data['value'] = contribution.value
            response_data['result'] = 'updated'
        except Entry.DoesNotExist as e:
            contribution = Contribution(value=value, fk_gift=gift, fk_user=request.user)
            contribution.save()
            response_data['value'] = contribution.value
            response_data['result'] = 'created'
        except Exception as e:
            response_data['result'] = 'failed'
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )


        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

class ProfileView(generic.DetailView):
    model = User
    slug_field = "username"
    template_name = "sandwish_app/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profiles_user = context["object"]

        context["profiles_owner"] = profiles_user
        context["is_profiles_owner"] = context["profiles_owner"] == self.request.user
        context["wishlists"] = Wishlist.objects.filter(fk_user=profiles_user.id)

        if "form" not in kwargs:
            context["form"] = WishlistCreationForm()

        return context

    def post(self, request, *args, **kwargs):
        # handle wishlist creation
        self.object = self.get_object() # owner
        form = WishlistCreationForm(request.POST)

        form.instance.fk_user = self.object # add foreign key

        if form.is_valid(): # validate form
            if self.object == self.request.user: # verify user is the profile's owner
                form.save()
                return HttpResponseRedirect(reverse_lazy("wishlist", kwargs={"username": self.object.username, "pk": form.instance.id}))
            return HttpResponseRedirect(reverse_lazy("profile", kwargs={"slug": self.object.username}))
        else:
            # handle invalid form values
            context = self.get_context_data(**kwargs)
            context.update({"form": form})
            return self.render_to_response(context)

class WishlistView(generic.ListView):
    template_name = "sandwish_app/wishlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["wishlists_owner"] = context["object_list"][0]
        context["wishlist"] = context["object_list"][1]
        context["gifts"] = Gift.objects.filter(fk_wishlist=context["wishlist"].id)
        context["is_wishlists_owner"] = context["wishlists_owner"] == self.request.user

        # context["contribution_form"] = ContributionForm()
        return context

    def get_queryset(self):
        username = self.kwargs["username"]
        pk = self.kwargs["pk"]

        wishlists_user = User.objects.get(username=username)
        wishlist = Wishlist.objects.get(id=pk, fk_user=wishlists_user.id)
        return wishlists_user, wishlist

class WishlistDeleteView(generic.DeleteView):
    model = Wishlist

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["wishlist_to_remove"] = self.get_object()
        context["wishlists_owner"] = context["wishlist_to_remove"].fk_user
        return context

    def delete(self, *args, **kwargs):
        wishlist_to_remove = self.get_object()
        wishlist_owner = wishlist_to_remove.fk_user

        if wishlist_owner == self.request.user: # verify user is the wishlisht's owner
            return super(WishlistDeleteView, self).delete(*args, **kwargs)
        return HttpResponseRedirect(reverse_lazy("wishlist", kwargs={"username": wishlist_owner.username,
                                                                      "pk": wishlist_to_remove.id}))

    def get_success_url(self):
        removed_wishlist = self.object
        wishlist_owner = removed_wishlist.fk_user
        return reverse_lazy("profile", kwargs={"slug": wishlist_owner.username})

class GiftDeleteView(generic.DeleteView):
    model = Gift

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gift_to_remove = self.get_object()
        context["wishlist"] = gift_to_remove.fk_wishlist
        context["wishlists_owner"] = context["wishlist"].fk_user
        return context

    def delete(self, *args, **kwargs):
        gift_wishlist = self.get_object().fk_wishlist
        gift_owner = gift_wishlist.fk_user

        if gift_owner == self.request.user: # verify user is the wishlisht's owner
            return super(GiftDeleteView, self).delete(*args, **kwargs)
        return HttpResponseRedirect(reverse_lazy("wishlist", kwargs={"username": gift_owner.username,
                                                                      "pk": gift_wishlist.id}))

    def get_success_url(self):
        removed_gift = self.object
        wishlist = removed_gift.fk_wishlist
        wishlist_owner = wishlist.fk_user
        return reverse_lazy("wishlist", kwargs={"username" : wishlist_owner.username, "pk" : wishlist.id})

class GiftCreateView(generic.CreateView):
    model = Gift
    fields = ["name", "price", "image", "link"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["wishlist"] = Wishlist.objects.get(id=self.kwargs.get("pk"))
        context["wishlists_owner"] = context["wishlist"].fk_user
        return context

    def form_valid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        gift_wishlist = context["wishlist"]
        gift_owner = context["wishlists_owner"]

        gift_to_create = form.instance
        gift_to_create.fk_wishlist = gift_wishlist # add foreign key

        if gift_owner == self.request.user: # verify user is the wishlisht's owner
            return super(GiftCreateView, self).form_valid(form)
        return HttpResponseRedirect(reverse_lazy("wishlist", kwargs={"username": gift_owner.username,
                                                                      "pk": gift_wishlist.id}))

    def get_success_url(self):
        new_gift = self.object
        wishlist = new_gift.fk_wishlist
        owner = wishlist.fk_user
        return reverse_lazy("wishlist", kwargs={"username": owner.username, "pk": wishlist.id})
