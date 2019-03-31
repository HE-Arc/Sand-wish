from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic, View
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from .forms import WishlistCreationForm, GiftCreationForm
import json as json
from django.core import serializers

# for signup
from django.contrib.auth import login, authenticate
from .models import User, Wishlist, Gift, Contribution
from sandwish_app.forms import SignUpForm

def index(request, search=None):
    search = "" if search == None else search
    context = {}
    context["search"] = search
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


# - USERS VIEWS ----------------------------------------------------------------

def create_contribution(request):
    if request.method == 'POST':
        value = request.POST.get('value')
        giftId = request.POST.get('giftId')
        gift = Gift.objects.get(id=giftId)

        response_data = {}

        # check that the value is correct
        currentContributionValue = 0
        for contribution in Contribution.objects.filter(fk_gift=gift.id).exclude(fk_user=request.user.id):
            currentContributionValue += contribution.value
        if float(value) < 1 or float(value) > (gift.price - currentContributionValue):
            response_data['result'] = 'fail'
            response_data['error_message'] = "the total contribution exceeded the price of the gift"
            try:
                contribution = Contribution.objects.get(fk_gift=gift.id, fk_user=request.user.id)
                response_data['old_value'] = float(contribution.value)
            except Exception as e:
                response_data['old_value'] = 0
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )

        try:
            contribution = Contribution.objects.get(fk_gift=gift.id, fk_user=request.user.id)
            contribution.value = value
            contribution.save()
            response_data['value'] = contribution.value
            response_data['result'] = 'success'
        except ObjectDoesNotExist as e:
            contribution = Contribution(value=value, fk_gift=gift, fk_user=request.user)
            contribution.save()
            response_data['value'] = contribution.value
            response_data['result'] = 'success'
        except Exception as e:
            print(e)
            response_data['result'] = 'fail'
            response_data['error_message'] = "the gift doesn't exist"
            response_data['old_value'] = 0
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )

        response_data["new_total_contribution"] = str(float(currentContributionValue) + float(value))

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"result": "not_post"}),
            content_type="application/json"
        )

def search(request):
    if request.method == "POST":
        search = request.POST.get("search")
        search = "" if search == None else search

        response_data = {}
        response_data["results"] = serializers.serialize("json", User.objects.filter(username__icontains=search))

        return JsonResponse(response_data)

def search_redirect(request):
    search = request.POST.get("search")
    search = "" if search == None else search
    return JsonResponse({'success': True,
                         'url': reverse_lazy("index_search", kwargs={"search": search})})

class ProfileView(generic.DetailView):
    model = User
    slug_field = "username"
    template_name = "sandwish_app/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profiles_user = context["object"]

        context["profiles_owner"] = profiles_user
        context["is_profiles_owner"] = context["profiles_owner"] == self.request.user
        context["user"] = self.request.user
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

# - WISHLISTS VIEWS ------------------------------------------------------------

class WishlistView(generic.DetailView):
    model = Wishlist
    template_name = "sandwish_app/wishlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["wishlists_owner"] = User.objects.get(username=self.kwargs["username"])
        context["wishlist"] = self.object
        context["is_wishlists_owner"] = context["wishlists_owner"] == self.request.user

        # faut faire une liste des cadeau associé à leur contribution et à la courante
        gifts = []
        for gift in Gift.objects.filter(fk_wishlist=context["wishlist"].id):
            full_gift = []
            full_gift.append(gift)

            total_contribution = 0
            user_contribution = 0
            contributors = []
            for contribution in Contribution.objects.filter(fk_gift=gift.id):
                total_contribution += contribution.value
                if contribution.fk_user.id == self.request.user.id:
                    user_contribution = contribution.value
                contributors.append(contribution.fk_user.username)
            full_gift.append(total_contribution)
            full_gift.append(user_contribution)
            full_gift.append(gift.price - total_contribution + user_contribution)
            full_gift.append(contributors)
            gifts.append(full_gift)
        context["gifts"] = gifts
        return context

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

# - GIFTS VIEWS ----------------------------------------------------------------

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

class GiftValidateView(generic.UpdateView):
    model = Gift
    fields = []
    template_name = "sandwish_app/gift_confirm_validate.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gift_to_validate = self.get_object()
        context["wishlist"] = gift_to_validate.fk_wishlist
        context["wishlists_owner"] = context["wishlist"].fk_user
        return context

    def form_valid(self, form):
        gift_to_validate = form.instance
        gift_wishlist = gift_to_validate.fk_wishlist
        gift_owner = gift_wishlist.fk_user

        if gift_owner == self.request.user: # verify user is the wishlisht's owner
            gift_to_validate.validated = True
            super(GiftValidateView, self).form_valid(form)

        return HttpResponseRedirect(reverse_lazy("wishlist", kwargs={"username": gift_owner.username,
                                                                      "pk": gift_wishlist.id}))

    def get_success_url(self):
        validated_gift = self.object
        wishlist = validated_gift.fk_wishlist
        wishlist_owner = wishlist.fk_user
        return reverse_lazy("wishlist", kwargs={"username" : wishlist_owner.username, "pk" : wishlist.id})

class GiftCreateView(generic.CreateView):
    model = Gift
    form_class = GiftCreationForm

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
