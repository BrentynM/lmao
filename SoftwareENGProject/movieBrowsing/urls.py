from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('admin/movie_search/', views.admin_movie_search, name='admin_movie_search'),
    path('add_theater/', views.add_theater, name='add_theater'),
    path('add_showtime/<int:movie_id>/', views.add_showtime, name='add_showtime'),
    path('purchase_tickets/', views.purchase_tickets, name='purchase_tickets'),
    path('print_ticket/<int:movie_id>/<int:quantity>/<int:showtime_id>/', views.print_ticket, name='print_ticket'),
]