from django.contrib import admin
from .models import Category, AuctionItem, Bid, Comment

admin.site.register(Category)
admin.site.register(AuctionItem)
admin.site.register(Bid)
admin.site.register(Comment)
