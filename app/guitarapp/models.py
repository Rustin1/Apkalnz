from django.db import models
from django.db.models import Avg


class RatingBase(models.Model):
    average_rating = models.FloatField(default=0)
    rating_count = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True


class Song(RatingBase):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=[('akordy', 'Akordy'), ('tabulatura', 'Tabulatura')], default='akordy')
    chords = models.TextField()
    nr_viewed = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def update_rating(self):
        # Pobieramy wszystkie recenzje powiązane z piosenką
        reviews = self.reviews.all()
        self.rating_count = reviews.count()

        # Jeśli istnieją recenzje, obliczamy średnią ocen
        if self.rating_count > 0:
            self.average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        else:
            self.average_rating = 0  # Jeśli brak recenzji, średnia wynosi 0

        self.save()


class Review(models.Model):
    song = models.ForeignKey(Song, related_name="reviews", on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(max_length=1000)

    def __str__(self):
        return f"Review for {self.song.name} - Rating: {self.rating}"

    def save(self, *args, **kwargs):
        # Zapisujemy recenzję
        super().save(*args, **kwargs)
        # Po zapisaniu recenzji, aktualizujemy ocenę piosenki
        self.song.update_rating()
