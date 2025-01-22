from django.urls import path
from guitarapp.views import SongSearchView, SongDetailView, ReviewAPIView, ReviewAPIPost, TransposeChords
from django.views.generic import TemplateView  # Importuj TemplateView
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', SongSearchView.as_view(), name='song_search'),
    path('songs/<int:pk>/', SongDetailView.as_view(), name='song_detail'),
    path('reviews/', ReviewAPIView.as_view(), name='reviews_list'),
    path('reviews/<int:pk>/', ReviewAPIView.as_view(), name='reviews_song_list'),
    path('reviews/create/', ReviewAPIPost.as_view(), name='create_review'),
    path('transpose/', TransposeChords.as_view(), name='transpose_chords'),
    path('', TemplateView.as_view(template_name='./index.html'), name='home'),
    path('tab', TemplateView.as_view(template_name='./song.html'), name='tab'),
    path('tuner', TemplateView.as_view(template_name='./tuner.html'), name='tuner'),
]
