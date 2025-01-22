from rest_framework import serializers
from .models import Song, Review


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'name', 'author', 'category', 'chords', 'average_rating', 'rating_count', 'nr_viewed']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['song', 'rating', 'comment']
