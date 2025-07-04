from django.db import models

# Create your models here.
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Index


# Create your models here.
class ReviewMixin(models.Model):
    review_content = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])

    class Meta:
        abstract = True
        ordering = ['-rating']


class Restaurant(models.Model):
    name = models.CharField(
        max_length=100,
        validators=(
            MinLengthValidator(2, "Name must be at least 2 characters long."),
            MaxLengthValidator(100, "Name cannot exceed 100 characters.")
        )
    )

    location = models.CharField(
        max_length=200,
        validators=(
            MinLengthValidator(2, "Location must be at least 2 characters long."),
            MaxLengthValidator(200, "Location cannot exceed 200 characters.")
        )
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=(
            MinValueValidator(0, "Rating must be at least 0.00."),
            MaxValueValidator(5, "Rating cannot exceed 5.00.")
        ),
    )

    def __str__(self):
        return self.name


def validate_menu_categories(desc):
    # Check if the description includes specific categories
    categories = ["Appetizers", "Main Course", "Desserts"]
    for category in categories:
        if category not in desc:
            all_categories_str = ', '.join([f'"{x}"' for x in categories])
            raise ValidationError(

                f'The menu must include each of the categories {all_categories_str}.'
            )


class Menu(models.Model):
    name = models.CharField(
        max_length=100,
    )

    description = models.TextField(
        validators=(
            validate_menu_categories,
        )
    )

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class RestaurantReview(ReviewMixin):
    class Meta(ReviewMixin.Meta):
        abstract = True
        verbose_name = "Restaurant Review"
        verbose_name_plural = "Restaurant Reviews"
        unique_together = ('reviewer_name', 'restaurant')

    reviewer_name = models.CharField(
        max_length=100,
    )

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
    )

    # review_content = models.TextField()
    # rating = models.PositiveIntegerField(validators=(MaxValueValidator(5)))


class RegularRestaurantReview(RestaurantReview):
    pass


class FoodCriticRestaurantReview(RestaurantReview):
    food_critic_cuisine_area = models.CharField(
        max_length=100,
    )

    class Meta(RestaurantReview.Meta):
        verbose_name = "Food Critic Review"
        verbose_name_plural = "Food Critic Reviews"


class MenuReview(ReviewMixin):
    reviewer_name = models.CharField(max_length=100)
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
    )

    # review_content = models.TextField()
    # rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])

    class Meta(ReviewMixin.Meta):
        verbose_name = "Menu Review"
        verbose_name_plural = "Menu Reviews"
        unique_together = ('reviewer_name', 'menu')
        indexes = [
            models.Index(fields=['menu'], name='main_app_menu_review_menu_id'),
        ]















