from django import forms
from django.contrib.auth.models import User
from .models import Theater, Showtime
from datetime import datetime

class TheaterForm(forms.ModelForm):
    class Meta:
        model = Theater
        fields = ['name', 'address', 'city', 'state', 'zip_code']

class ShowtimeForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Showtime
        fields = ['theater', 'date', 'time']
        
    def save(self, commit=True):
        showtime = super().save(commit=False)
        showtime.showtime = datetime.combine(self.cleaned_data['date'], self.cleaned_data['time'])
        if commit:
            showtime.save()
        return showtime

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    address = forms.CharField(max_length=255)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    zip = forms.CharField(max_length=10)
    phone_number = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data
    
    

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    

class MovieSearchForm(forms.Form):
    movie_title = forms.CharField(max_length=100, label='Movie Title')

class TicketPurchaseForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label='Number of Tickets')