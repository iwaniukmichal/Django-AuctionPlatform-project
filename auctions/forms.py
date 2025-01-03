from django import forms
from .models import AuctionItem, Comment
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class AuctionItemForm(forms.ModelForm):
    ends_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="End Date and Time",
    )

    class Meta:
        model = AuctionItem
        fields = ['title', 'description', 'starting_bid', 'image', 'category', 'ends_at']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match.")
        return cleaned_data
