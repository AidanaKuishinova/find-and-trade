from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('profile/<str:id>/', views.ProfileView.as_view(), name='profile'),
    path('myprofile/', views.myprofile, name='myprofile'),
    path('other_user_profile/', views.other_user_profile, name='other_user_profile'),
    path('profile_edit/', views.ProfileUpdateView.as_view(), name='profile edit'),


    path('categories/', views.categories, name='categories'),
    path('categories2/', views.categories2, name='categories2'),
    path('search_result/', views.SearchResultView.as_view(), name='searchresult'),
    path('search_results/', views.search_results, name='searchresult2'),

    path('create_ad/', views.AdCreateView.as_view(), name='create ad'),
    path('edit_ad/<int:pk>/', views.AdEditView.as_view(), name='edit ad'),
    path('ad_list/', views.AdListView.as_view(), name='ad list'),
    path('ad_details/<int:id>/', views.DetailAdView.as_view(), name='ad_details'),

    path('active_ads/', views.ActiveAdListView.as_view(), name='active ads'),
    path('archived_ads/', views.ArchivedAdListView.as_view(), name='archived ads'),
    path('delete_photo/', views.delete_photo, name='delete_photo'),
    path('delete_ad/', views.delete_ad, name='delete_ad'),
    path('archive_ad/', views.archive_ad, name='archive_ad'),
    path('active_ad/', views.active_ad, name='active_ad'),

    path('blog/', views.blog, name='blog'),
    path('blog_article/', views.blog_article, name='blog_article'),
    path('responds/', views.RespondsListView.as_view(), name='responds'),
    path('add_responder/', views.add_responders, name='add responder'),
    path('offers/', views.offers, name='offers'),
    path('chatbox/', views.chatbox, name='chatbox'),
    path('support_chat/', views.support_chat, name='support_chat'),
    path('favs/', views.FavouriteAdView.as_view(), name='favs'),
    path('favs_delete/', views.favs_delete, name='favs_delete'),
    path('about_us/', views.about_us, name='about_us'),

    path('chat/', views.chatt, name='chat'),
    path('contact/', views.contact, name='contact'),
    path('loading/', views.loading, name='loading'),
    path('error/', views.error, name='error'),
    path('payment/', views.payment, name='payment'),
    path('tariff/', views.tariff, name='tariff'),
    path('termscond/', views.termscond, name='termscond'),

    path('forgot1/', views.forgot1, name='forgot1'),
    path('forgot2/', views.forgot2, name='forgot2'),
    path('forgot3/', views.forgot3, name='forgot3'),
    path('reset_password/', views.reset_password, name="reset_password"),
    path('reset/<str:user>/<str:token>/', views.password_reset_confirm, name="password_reset_confirm"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)