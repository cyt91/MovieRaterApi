from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=360)

    def no_of_ratings(self):
        ratings = Rating.objects.filter(movie=self)
        return len(ratings)

    def avg_rating(self):
        sum_of_ratings = 0
        ratings = Rating.objects.filter(movie=self)
        for rating in ratings:
            sum_of_ratings += rating.stars

        if len(ratings) > 0:
            return sum_of_ratings/len(ratings)
        else:
            return 0


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        # unique_together = [['user', 'movie']]
        # index_together = [['user', 'movie']]
        constraints = [
            models.UniqueConstraint(fields=['user', 'movie'], name='unique_user_movie'),
        ]
        indexes = [
            models.Index(fields=['user', 'movie'], name='user_movie_idx'),
        ]
