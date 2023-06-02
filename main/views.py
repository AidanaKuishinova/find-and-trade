import uuid

from django.shortcuts import render, redirect
from .models import CustomUser, Profile, Ad, RespondState
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView,DetailView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserForm, CustomUserEditForm, ProfileForm, AuthUserForm, AdCreateForm
from multi_form_view import MultiModelFormView
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FavoriteAd, Respond
from chat.models import Thread
from .utils import *
# Create your views here.
def index(request):
    ads=Ad.objects.order_by('create_date')
    return render(request, 'main/index.html', {'ads':ads[0:8]})


def chatt(request):
    users = CustomUser.objects.all()
    for user in users:
        if request.user != user:
            try:
                thread = Thread.objects.get(first_person=request.user, second_person=user)
                print(thread)
            except:
                try:
                    thread = Thread(first_person=request.user, second_person=user)
                    thread2 = Thread.objects.get(first_person=user, second_person=request.user)
                except Exception as e:
                    print(e)
                    thread.save()
                    pass
                pass
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    print(threads, "THREADS")
    context = {
        'Threads':threads
    }
    return render(request, "main/admin chat.html",context)

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
        ctx['id'] = self.request.user.id
        self.model = CustomUser.objects.get(id=ctx['id'])
        ctx['model'] = self.model
        return ctx


class OtherProfileView(TemplateView):
    template_name = "main/other_user_profile.html"

    def get_context_data(self, **kwargs):
        ctx = super(OtherProfileView, self).get_context_data(**kwargs)
        ctx['id'] = self.kwargs['id']
        ctx['ads'] = Ad.objects.filter(user__id=ctx['id'])[0:3]
        print(ctx)
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
        print(forms)
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

        forms['profile_form'].fields['company_name'].initial = self.model.profile.company_name
        forms['profile_form'].fields['description'].initial = self.model.profile.description
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

class LoginUserView(LoginView):
    template_name = "main/login.html"
    success_url = reverse_lazy('index')
    form_class = AuthUserForm

class MyLogoutView(LogoutView):
    next_page = reverse_lazy("index")

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
    paginate_by = 16

    def get_queryset(self):
        query=self.request.GET.get("q")
        if query:
            object_list=Ad.objects.filter(
                Q(title__icontains=query)
            )
            print(self.request.GET)
        if self.request.GET.get("filter_type"):
            filter_type=self.request.GET.get("filter_type")
            if filter_type== "price_down":
                object_list = Ad.objects.order_by('-cost')
            if filter_type == "price_up":
                object_list = Ad.objects.order_by('cost')
            if filter_type == "alphabet":
                object_list = Ad.objects.order_by('title')
            if filter_type == "create_date":
                object_list = Ad.objects.order_by('-create_date')
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
            responders__user=self.request.user,
            is_active=True
        )
        return new_context


def add_responders(request):
    if request.method == "POST":
        id_ad = request.POST.get("id_ad")
        id_user = request.POST.get("id_user")
        ad = Ad.objects.get(id=id_ad)
        user = CustomUser.objects.get(id=id_user)
        respond = Respond(user=user, state=RespondState.PROCESSING)
        respond.save()
        ad.responders.add(respond)
        ad.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def blog(request):
    return render(request, 'main/blog.html', {})

def blog_article(request):
    return render(request, 'main/blog_article.html', {})

def about_us(request):
    return render(request, 'main/about_us.html', {})

def offers(request):
    return render(request, 'main/offers.html', {})


def chatbox(request):
    users = CustomUser.objects.all()
    for user in users:
        if request.user != user:
            try:
                thread = Thread.objects.get(first_person=request.user, second_person=user)
                print(thread)
            except:
                try:
                    thread = Thread(first_person=request.user, second_person=user)
                    thread2 = Thread.objects.get(first_person=user, second_person=request.user)
                except Exception as e:
                    print(e)
                    thread.save()
                    pass
                pass
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    print(threads, "THREADS")
    context = {
        'Threads': threads
    }
    return render(request, 'main/chatbox.html', context)


def forgot1(request):
    return render(request, 'main/forgot_password_1.html', {})


def forgot2(request):
    return render(request, 'main/forgot_password_2.html', {})


def forgot3(request):
    return render(request, 'main/forgot_password_3.html', {})


def congrats_password(request):
    return render(request, 'main/congrats_password.html', {})

def reset_password(request):
    if request.method == "POST":

        try:
            email = request.POST.get("email")
            user = CustomUser.objects.get(email=email)
            print(user)
            id = user.id
            token = uuid.uuid4()
            user.reset_password_token = token
            user.save()
            send_reset_password_mail(email=email, token=str(token),  id=id)
            return render(request, 'main/inform_email.html')
        except Exception as e:
            print(e)
    else:
        return render(request, 'main/forgot_password_1.html')


def password_reset_confirm(request, user, token):
    if request.method == "POST":
        print(request.POST)
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        print(password1)
        if password1 == password2:
            user = CustomUser.objects.get(id=user)
            user.set_password(password1)
            user.save()
            return redirect('congrats_password')
        else:
            return render(request, 'main/error.html', {"error": "We have error"})
    else:
        try:
            user = CustomUser.objects.get(id=user)
            if str(user.reset_password_token) == token:
                # user.reset_password_token = None
                user.save()
                return render(request, 'main/forgot_password_3.html',{'id':user.id, 'token':token})
            else:
                print('no')
                return render(request, 'main/error.html', {'message': "Недействительный токен"})
        except Exception as e:
            print(e)
            return render(request, 'main/error.html', {'message': "Недействительный токен"})

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

def contact(request):
    return render(request, 'main/contact.html', {})

def loading(request):
    return render(request, 'main/loading.html', {})

def error(request):
    return render(request, 'main/error.html', {})

def payment(request):
    return render(request, 'main/payment.html', {})

def tariff(request):
    return render(request, 'main/tariff.html', {})

def termscond(request):
    return render(request, 'main/termscond.html', {})

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