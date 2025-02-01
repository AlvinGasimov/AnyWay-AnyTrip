from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name = 'home'),
    path('announcements/<slug:slug>', views.AnnouncementDetailPageView.as_view(), name = 'announcement-detail'),
    path('search-result/', views.search_result, name = 'search-result'),
    path('subscribe/', views.subscribe, name = 'subscribe'),
    path('rules/', views.rules, name = 'rules'),
    path('api/get-price', views.PriceResponse.as_view(), name = 'api-get-price'),
    path('subscribe/send_email_to_subscribers/', views.send_email_to_subscribers, name='booking_subscribe_send_email_to_subscribers'),
    path('rooms/<int:pk>/', views.rooms, name = 'rooms'),
    path('room/<int:pk>/', views.room_detail, name = 'room_detail'),
]