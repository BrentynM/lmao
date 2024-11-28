from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .forms import RegistrationForm, LoginForm, MovieSearchForm, TheaterForm, ShowtimeForm, TicketPurchaseForm
from .models import Profile, Theater, Showtime
import requests
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime
import tmdbsimple as tmdb
from django.contrib.auth.decorators import login_required


@staff_member_required
def add_theater(request):
    if request.method == 'POST':
        form = TheaterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TheaterForm()
    return render(request, 'add_theater.html', {'form': form})


@staff_member_required
def add_showtime(request, movie_id):
    movie = tmdb.Movies(movie_id)
    response = movie.info()
    movie_title = response['title']
    if request.method == 'POST':
        form = ShowtimeForm(request.POST)
        if form.is_valid():
            showtime = form.save(commit=False)
            showtime.movie = TMDBMovie.objects.get(movie_id=movie_id)
            showtime.showtime = datetime.combine(form.cleaned_data['date'], form.cleaned_data['time'])
            showtime.save()
            return redirect('movie_detail', movie_id=movie_id)
    else:
        form = ShowtimeForm()
    return render(request, 'add_showtime.html', {'form': form, 'movie_title': movie_title})


def get_tmdb_movie_id(api_key, movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return data['results'][0]['id']  # Return the ID of the first search result
        else:
            return None
    else:
        response.raise_for_status()

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            profile = Profile(
                user=user,
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                zip=form.cleaned_data['zip'],
                phone_number=form.cleaned_data['phone_number']
            )
            profile.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'registrationpage.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=User.objects.get(email=email).username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page after successful login
            else:
                form.add_error(None, 'Invalid email or password')
    else:
        form = LoginForm()
    return render(request, 'loginpage.html', {'form': form})



from django.shortcuts import render, redirect
import tmdbsimple as tmdb
from .models import TMDBMovie

def home(request):
    movie_ids = TMDBMovie.objects.values_list('movie_id', flat=True)
    movies = []
    for movie_id in movie_ids:
        movie = tmdb.Movies(movie_id)
        response = movie.info()
        movies.append({
            'id': movie_id,
            'title': response['title'],
            'poster_path': response['poster_path']
        })
    return render(request, 'homepage.html', {'movies': movies})

def movie_detail(request, movie_id):
    movie = get_object_or_404(TMDBMovie, movie_id=movie_id)
    showtimes = Showtime.objects.filter(movie=movie)
    movieinfo = tmdb.Movies(movie_id)
    response = movieinfo.info()
    return render(request, 'movie_detail.html', {'movie': response, 'showtimes': showtimes})

def fetch_movie(request, movie_title):
    api_key = 'your_tmdb_api_key'  # Replace with your TMDB API key
    movie_id = get_tmdb_movie_id(api_key, movie_title)
    if movie_id:
        movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
        movie_response = requests.get(movie_url)
        if movie_response.status_code == 200:
            movie_data = movie_response.json()
            TMDBMovie.objects.create(
                movie_id=movie_id,
                title=movie_data['title'],
                poster_path=movie_data['poster_path']  # Save the poster path
            )
            return render(request, 'movie_detail.html', {'movie_id': movie_id})
        else:
            return render(request, 'movie_not_found.html', {'movie_title': movie_title})
    else:
        return render(request, 'movie_not_found.html', {'movie_title': movie_title})
    

@staff_member_required
def admin_movie_search(request):
    if request.method == 'POST':
        form = MovieSearchForm(request.POST)
        if form.is_valid():
            movie_title = form.cleaned_data['movie_title']
            api_key = '01dbaeff8f72fe91afd5bb7c054fbb15'  # Replace with your TMDB API key
            movie_id = get_tmdb_movie_id(api_key, movie_title)
            if movie_id:
                movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
                movie_response = requests.get(movie_url)
                if movie_response.status_code == 200:
                    movie_data = movie_response.json()
                    TMDBMovie.objects.create(
                        movie_id=movie_id,
                    )
                    return redirect('home')
                else:
                    return render(request, 'admin_movie_search.html', {'form': form, 'error': 'Failed to fetch movie details'})
            else:
                return render(request, 'admin_movie_search.html', {'form': form, 'error': 'Movie not found'})
    else:
        form = MovieSearchForm()
    return render(request, 'admin_movie_search.html', {'form': form})

@login_required
def purchase_tickets(request, movie_id):
    movie = get_object_or_404(TMDBMovie, movie_id=movie_id)
    showtime_id = request.GET.get('showtime_id')
    showtime = get_object_or_404(Showtime, id=showtime_id)

    if request.method == 'POST':
        form = TicketPurchaseForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            # Here you would handle the payment process and ticket generation
            return redirect('print_ticket', movie_id=movie_id, quantity=quantity, showtime_id=showtime_id)
    else:
        form = TicketPurchaseForm()

    return render(request, 'purchase_tickets.html', {'form': form, 'movie': movie, 'showtime': showtime})


import random
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import TMDBMovie, Showtime

def generate_barcode():
    return ''.join(random.choices('0123456789', k=12))

@login_required
def print_ticket(request, movie_id, quantity, showtime_id):
    movie = get_object_or_404(TMDBMovie, movie_id=movie_id)
    showtime = get_object_or_404(Showtime, id=showtime_id)

    # Fetch movie poster
    poster_image = None
    if movie.poster_path:
        poster_url = f"https://image.tmdb.org/t/p/w500{movie.poster_path}"
        poster_response = requests.get(poster_url)
        if (poster_response.status_code == 200):
            poster_buffer = BytesIO(poster_response.content)
            poster_image = ImageReader(poster_buffer)

    # Create PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="tickets_{movie_id}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    for _ in range(quantity):
        barcode_number = generate_barcode()

        # Generate barcode image
        barcode_class = barcode.get_barcode_class('code128')
        barcode_instance = barcode_class(barcode_number, writer=ImageWriter())
        barcode_buffer = BytesIO()
        barcode_instance.write(barcode_buffer)
        barcode_buffer.seek(0)
        barcode_image = ImageReader(barcode_buffer)

        # Draw movie details
        p.setFont("Helvetica", 12)
        p.drawString(1 * inch, height - 1 * inch, f"Movie: {movie.title}")
        p.drawString(1 * inch, height - 1.5 * inch, f"Showtime: {showtime.showtime} at {showtime.theater.name}")

        # Draw movie poster if available
        if poster_image:
            p.drawImage(poster_image, 1 * inch, height - 4.5 * inch, width=2 * inch, height=3 * inch)

        # Draw barcode
        p.drawImage(barcode_image, 1 * inch, height - 8 * inch, width=4 * inch, height=1 * inch)

        p.showPage()

    p.save()

    return response