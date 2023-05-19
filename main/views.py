from django.shortcuts import render, redirect
from .models import CustomUser, Profile, Ad
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView,DetailView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from .forms import CustomUserForm, CustomUserEditForm, ProfileForm, AuthUserForm, AdCreateForm
from multi_form_view import MultiModelFormView
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FavoriteAd

# Create your views here.
def index(request):
    return render(request, 'main/index.html', {})


def register_view(request):
    if request.method == "POST":
        print(request.POST)
    return render(request, 'main/index.html', {})


class RegisterUserView(MultiModelFormView):
    form_classes = {
        'custom_user_form': CustomUserForm,
        'profile_form': ProfileForm,
    }
    template_name = "main/registration.html"
    success_url = reverse_lazy('login')
    success_msg = "Пользователь успешно создан"

    def forms_valid(self, forms):
        custom_user = forms['custom_user_form'].save(commit=False)
        profile = forms['profile_form'].save(commit=True)
        custom_user.profile = profile
        custom_user.save()
        return super(RegisterUserView, self).forms_valid(forms)


class ProfileView(TemplateView):
    template_name = "main/profile.html"

    def get_context_data(self, **kwargs):
        ctx = super(ProfileView, self).get_context_data(**kwargs)
        ctx['id'] = self.kwargs['id']
        self.model = CustomUser.objects.get(id=ctx['id'])
        ctx['model'] = self.model
        return ctx


class ProfileUpdateView(MultiModelFormView, UpdateView):
    template_name = "main/editprofile.html"
    form_classes = {
        'custom_user_form': CustomUserEditForm,
        'profile_form': ProfileForm,
    }
    success_url = reverse_lazy('profile edit')

    def get_context_data(self, **kwargs):
        ctx = super(ProfileUpdateView, self).get_context_data(**kwargs)
        ctx['model'] = self.model
        return ctx

    def forms_valid(self, forms):
        custom_user = forms['custom_user_form'].save(commit=True)
        profile = forms['profile_form'].save(commit=True)
        custom_user.profile = profile
        custom_user.save()
        print("forms is valid")
        self.object = custom_user
        return super(ProfileUpdateView, self).forms_valid(forms)

    def get_forms(self):
        self.model = CustomUser.objects.get(id=self.request.user.id)
        forms = super(ProfileUpdateView, self).get_forms()
        forms['custom_user_form'].fields['name'].initial = self.model.name
        forms['custom_user_form'].fields['surname'].initial = self.model.surname
        forms['custom_user_form'].fields['email'].initial = self.model.email

        forms['profile_form'].fields['phone_number'].initial = self.model.profile.phone_number
        forms['profile_form'].fields['role'].initial = self.model.profile.role
        forms['profile_form'].fields['image_link'].initial = self.model.profile.image_link
        forms['custom_user_form'].instance = self.request.user
        forms['profile_form'].instance = self.model.profile


        return forms


class AdEditView(UpdateView):
    template_name = "main/edit_ad.html"
    model=Ad
    form_class = AdCreateForm


    # def get_initial(self):
    #     initial = super().get_initial()
    #     initial['pk'] = self.kwargs['pk']
    #     return initial

    def get_success_url(self):
        return reverse('edit ad', kwargs={'pk': self.object.pk})

    def get_initial(self):
        model = CustomUser.objects.get(id=self.request.user.id)
        ad = Ad.objects.get(id=self.kwargs['pk'], user=model)
        return {'title': ad.title}

    # def get_context_data(self, **kwargs):
    #     ctx = super(AdEditView, self).get_context_data(**kwargs)
    #     ctx['model'] = self.model
    #     return ctx
    #
    # def forms_valid(self, forms):
    #     ad_edit_form = forms['ad_edit_form'].save(commit=False)
    #     print("forms is valid")
    #
    #     return super(AdEditView, self).forms_valid(forms)
    #
    # def get_form_class(self):
    #     self.model = CustomUser.objects.get(id=self.request.user.id)
    #     self.ad = Ad.objects.get(id=self.kwargs['pk'], user=self.model)
    #     form = super(AdEditView, self).get_form_class()
    #     form['ad_edit_form'].fields['title'].initial = self.ad.title
    #     form.fields['company_name'].initial = self.ad.company_name
    #     form.fields['image_link'].initial = self.ad.image_link
    #     form.fields['description'].initial = self.ad.description
    #     form.fields['cost'].initial = self.ad.cost
    #
    #
    #     return form


class LoginUserView(LoginView):
    template_name = "main/login.html"
    success_url = reverse_lazy('index')
    form_class = AuthUserForm


class AdCreateView(CreateView):
    template_name = "main/create_ad.html"
    form_class = AdCreateForm
    success_url = reverse_lazy('ad list')


class AdListView(ListView):
    template_name = "main/ad_list.html"
    model = Ad

class SearchResultView(ListView):
    template_name = "main/search_result.html"
    model = Ad
    paginate_by = 8

    def get_queryset(self):
        query=self.request.GET.get("q")
        if query:
            object_list=Ad.objects.filter(
                Q(title__icontains=query)
            )
        else:
            object_list=Ad.objects.all()
        return object_list

class DetailAdView(DetailView):
    template_name = "main/ad_details.html"
    model = Ad
    def get_object(self, queryset=None):
        id= self.kwargs.get("id", None)
        return Ad.objects.get(id=id)



class ActiveAdListView(ListView):
    template_name = "main/active_ads.html"
    model = Ad
    paginate_by = 4

    def get_queryset(self):
        new_context = Ad.objects.filter(
            user=self.request.user,
            is_active=True
        )
        return new_context


class ArchivedAdListView(ListView):
    template_name = "main/archived_ads.html"
    model = Ad
    paginate_by = 4

    def get_queryset(self):
        new_context = Ad.objects.filter(
            user=self.request.user,
            is_active=False
        )
        return new_context


class RespondsListView(ListView):
    template_name = "main/responds.html"
    model = Ad

    def get_queryset(self):
        new_context = Ad.objects.filter(
            user=self.request.user,

            is_active=True
        )
        return new_context


def add_responders(request):
    if request.method == "POST":
        id_ad = request.POST.get("id_ad")
        id_user = request.POST.get("id_user")
        ad = Ad.objects.get(id=id_ad)
        user = CustomUser.objects.get(id=id_user)
        ad.responders.add(user)
        ad.save()
        return redirect("ad list")


def blog(request):
    return render(request, 'main/blog.html', {})

def blog_article(request):
    return render(request, 'main/blog_article.html', {})

def about_us(request):
    return render(request, 'main/about_us.html', {})

def offers(request):
    return render(request, 'main/offers.html', {})


def chatbox(request):
    return render(request, 'main/chatbox.html', {})


def forgot1(request):
    return render(request, 'main/forgot_password_1.html', {})


def forgot2(request):
    return render(request, 'main/forgot_password_2.html', {})


def forgot3(request):
    return render(request, 'main/forgot_password_3.html', {})


def myprofile(request):
    return render(request, 'main/myprofile.html', {})


def categories(request):
    return render(request, 'main/categories.html', {})

def categories2(request):
    return render(request, 'main/categories2.html', {})


def search_results(request):
    return render(request, 'main/search_results.html', {})



def other_user_profile(request):
    return render(request, 'main/other_user_profile.html', {})

def support_chat(request):
    return render(request, 'main/support_chat.html', {})

def favs(request):
    return render(request, 'main/favs.html', {})

def delete_photo(request):
    print(request.user)
    user = CustomUser.objects.get(id=request.user.id)
    profile = user.profile
    profile.image_link=None
    profile.save()

    return redirect("profile edit")


def delete_ad(request):
    ad = Ad.objects.get(id=request.POST["id"])
    ad.delete()
    return redirect("archived ads")

def archive_ad(request):
    ad = Ad.objects.get(id=request.POST["id"])
    ad.is_active=False
    ad.save()
    return redirect("active ads")

def active_ad(request):
    ad = Ad.objects.get(id=request.POST["id"])
    ad.is_active=True
    ad.save()
    return redirect("archived ads")

class FavouriteAdView(ListView):
    template_name = "main/favs.html"
    model = FavoriteAd

def favs_delete(request):
    favorite_ad = FavoriteAd.objects.get(id=request.POST["id"])
    favorite_ad.delete()
    return redirect("favs")