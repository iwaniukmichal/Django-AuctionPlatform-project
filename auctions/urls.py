from django.urls import path
from . import views

urlpatterns = [
    path('', views.auctions, name='auctions'),
    path('home', views.home, name='home'),
    path('active_auctions', views.active_auctions, name='active_auctions'),
    path('auction_item_details/<int:item_id>/', views.auction_item_detail, name='auction_item_detail'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('bid/<int:item_id>/', views.bid, name='bid'),
    path('my_profile/', views.my_profile, name='my_profile'),
]

