from django.contrib.auth import login
from django.contrib.auth import logout
from .forms import LoginForm, CommentForm, AuctionItemForm
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import AuctionItem
from django.utils.timezone import now
from .models import Bid
from .utils import get_filter_and_sort_params
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm


# Redirects to the home page of auctions
def auctions(request):
    return redirect('/auctions/home')


# Renders the home page based on user authentication status
def home(request):
    if request.user.is_authenticated:
        return render(request, 'home_logged_in.html')
    else:
        return render(request, 'home_logged_out.html')


# Handles user login functionality
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


# Logs out the user and redirects to auctions home page
def logout_view(request):
    logout(request)
    return redirect('/auctions/home')


# Handles user registration process
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


# Displays details of an auction item and allows comments
def auction_item_detail(request, item_id):
    item = get_object_or_404(AuctionItem, id=item_id)
    is_user_authenticated = request.user.is_authenticated

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.auction_item = item
            comment.save()
            return redirect('auction_item_detail', item_id=item.id)
    else:
        form = CommentForm()
    return render(request, 'auction_item_detail.html',
                  {'item': item, 'is_user_authenticated': is_user_authenticated, 'form': form})


# Allows authenticated users to place a bid on an auction item
@login_required
def bid(request, item_id):
    item = get_object_or_404(AuctionItem, id=item_id)
    success_bid = False
    new_bid = None

    if request.method == 'POST':
        success_bid = True      #Client side validation accepted a bid
        new_bid = float(request.POST.get('bid_amount'))
        item.current_bid = new_bid
        item.save()
        new_bid = Bid.objects.create(
            user=request.user,
            auction_item=item,
            amount=new_bid,
            bid_time=now()
        )
    return render(request, 'bid.html', {'item': item, 'success_bid': success_bid, 'new_bid': new_bid})


# Displays the user's profile with their bids and created auction items
@login_required
def my_profile(request):
    user_bids = Bid.objects.filter(user=request.user, auction_item__ends_at__gt=now()).order_by('auction_item__ends_at')
    user_items = AuctionItem.objects.filter(created_by=request.user).order_by('-created_at')

    #Sorting parameters for user bids
    category, title, sort_by = get_filter_and_sort_params(request)

    if sort_by == 'ends_at':
        user_bids = user_bids.order_by('auction_item__ends_at')
    elif sort_by == 'bid_time':
        user_bids = user_bids.order_by('-bid_time')

    if category:
        user_bids = user_bids.filter(auction_item__category__name__icontains=category)
    if title:
        user_bids = user_bids.filter(auction_item__title__icontains=title)

    if request.method == 'POST':
        form = AuctionItemForm(request.POST, request.FILES) #Form for adding new auctions
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('auction_item_detail', item_id=item.id)
    else:
        form = AuctionItemForm()

    context = {
        "user_bids": user_bids,
        "sort_by": sort_by,
        "form": form,
        'items': user_items
    }

    return render(request, "my_profile.html", context)

# Displays active auctions and allows filtering and sorting
def active_auctions(request):
    items = AuctionItem.objects.filter(ends_at__gte=datetime.now()).order_by('ends_at')
    is_user_authenticated = request.user.is_authenticated

    #Sorting parameters for active auctions
    category, title, sort_by = get_filter_and_sort_params(request)

    if category:
        items = items.filter(category__name__icontains=category)
    if title:
        items = items.filter(title__icontains=title)

    if sort_by == 'created_at':
        items = items.order_by('-created_at')
    elif sort_by == 'ends_at':
        items = items.order_by('ends_at')

    return render(request, 'active_auctions.html',
                  {'items': items, 'is_user_authenticated': is_user_authenticated, 'sort_by': sort_by})
