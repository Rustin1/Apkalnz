from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Song, Review
from .serializers import SongSerializer, ReviewSerializer
from django.http import JsonResponse
from django.db.models import Q

class SongSearchView(generics.ListAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'category', 'author']  # Usunięto 'average'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.query_params.get('query', None)
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(category__icontains=query) |
                Q(author__icontains=query)
            )
        return queryset

class SongDetailView(generics.RetrieveAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    def retrieve(self, request, *args, **kwargs):
        song = self.get_object()

        # Increment the number of views for the song
        song.nr_viewed += 1
        song.save()

        return super().retrieve(request, *args, **kwargs)

class ReviewAPIView(APIView):
    def get(self, request, *args, **kwargs):
        song = self.kwargs['pk']
        if song:
            reviews = Review.objects.filter(song=song)
        else:
            reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class ReviewAPIPost(APIView):
    def post(self, request, *args, **kwargs):
        review_data = request.data
        try:
            song = Song.objects.get(id=review_data["song_id"])
            new_review = Review.objects.create(
                song=song,
                rating=review_data["rating"],
                comment=review_data["comment"]
            )
            # Update the song's average rating after a new review is added
            song.update_rating()
            serializer = ReviewSerializer(new_review)
            return Response(serializer.data)
        except Song.DoesNotExist:
            return Response({"error": "Song not found"}, status=404)

class TransposeChords(APIView):
    def post(self, request, *args, **kwargs):
        song_data = request.data
        chords = song_data["chords"]
        transpose_value = int(song_data["transpose_value"])

        transposed_chords = self.transpose_chords(chords, transpose_value)
        return JsonResponse({"transposed_chords": transposed_chords})

    def transpose_chords(self, chords, transpose_value):
        chord_sequence = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        chord_map = {chord: i for i, chord in enumerate(chord_sequence)}

        transposed_chords = []
        for chord in chords.split():
            if chord in chord_map:
                new_index = (chord_map[chord] + transpose_value) % len(chord_sequence)
                transposed_chords.append(chord_sequence[new_index])
            else:
                transposed_chords.append(chord)  # Leave unrecognized chords as they are

        return ' '.join(transposed_chords)
