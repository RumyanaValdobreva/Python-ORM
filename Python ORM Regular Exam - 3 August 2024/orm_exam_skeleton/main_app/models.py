from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator, MinValueValidator
from django.db.models import CASCADE
from main_app.managers import AstronautManager


# Create your models here.
class UpdatedAtMixin(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class NameMixin(models.Model):
    name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(120)
        ]
    )

    class Meta:
        abstract = True


class Astronaut(NameMixin, UpdatedAtMixin, models.Model):
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[
            RegexValidator(regex=r'^\d+$', ),
            MaxLengthValidator(15)
        ]
    )
    is_active = models.BooleanField(default=True)
    date_of_birth = models.DateField(null=True, blank=True)
    spacewalks = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0)
        ]
    )

    objects = AstronautManager()


class Spacecraft(NameMixin, UpdatedAtMixin, models.Model):
    manufacturer = models.CharField(
        max_length=100,
        validators=[
            MaxLengthValidator(100)
        ]
    )
    capacity = models.SmallIntegerField(validators=[MinValueValidator(1)])
    weight = models.FloatField(validators=[MinValueValidator(0.0)])
    launch_date = models.DateField()


class Mission(NameMixin, UpdatedAtMixin, models.Model):
    class StatusChoices(models.TextChoices):
        PLANNED = 'Planned', 'Planned'
        ONGOING = 'Ongoing', 'Ongoing'
        COMPLETED = 'Completed', 'Completed'

    description = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=9,
        choices=StatusChoices.choices,
        default=StatusChoices.PLANNED,
        validators=[
            MaxLengthValidator(9)
        ]
    )
    launch_date = models.DateField()
    spacecraft = models.ForeignKey(Spacecraft, on_delete=models.CASCADE, related_name='spacecraft_mission')
    astronauts = models.ManyToManyField(Astronaut, related_name='astronaut_mission')
    commander = models.ForeignKey(Astronaut, on_delete=models.SET_NULL, null=True, related_name='commander_mission')
