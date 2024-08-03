from django.db import models
from django.db.models import Count


class AstronautManager(models.Manager):
    def get_astronauts_by_missions_count(self):
        return self.annotate(missions_count=Count('astronaut_mission')).order_by('-missions_count', 'phone_number')