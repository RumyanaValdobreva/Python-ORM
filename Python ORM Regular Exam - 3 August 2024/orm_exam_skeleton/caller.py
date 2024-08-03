import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Astronaut, Mission, Spacecraft
from django.db.models import Q, Count, F, Sum


# Create queries within functions
def get_astronauts(search_string=None):
    astronauts = Astronaut.objects.filter(
        Q(name__icontains=search_string) | Q(phone_number__icontains=search_string)
    ).order_by('name')

    if search_string is None or not astronauts.exists():
        return ''

    result = []

    for astronaut in astronauts:
        status = 'Active' if astronaut.is_active else 'Inactive'

        result.append(f"Astronaut: {astronaut.name}, phone number: {astronaut.phone_number}, status: {status}")

    return '\n'.join(result)


def get_top_astronaut():
    top_astronaut = Astronaut.objects.annotate(missions_count=Count('astronaut_mission')
                                               ).order_by('-missions_count', 'phone_number').first()

    if not top_astronaut or top_astronaut.missions_count == 0:
        return 'No data.'

    return f"Top Astronaut: {top_astronaut.name} with {top_astronaut.missions_count} missions."


def get_top_commander():
    top_commander = Astronaut.objects.annotate(commander_count=Count('commander_mission')
                                               ).order_by('-commander_count', 'phone_number').first()

    if not top_commander or top_commander.commander_count == 0:
        return 'No data.'

    return f"Top Commander: {top_commander.name} with {top_commander.commander_count} commanded missions."


def get_last_completed_mission():
    last_mission = Mission.objects.filter(status=Mission.StatusChoices.COMPLETED).order_by('-launch_date').first()

    if not last_mission:
        return 'No data.'

    commander_name = last_mission.commander.name if last_mission.commander else 'TBA'
    astronauts = ', '.join(last_mission.astronauts.order_by('name').values_list('name', flat=True))
    num_of_spacewalks = sum(astronaut.spacewalks for astronaut in last_mission.astronauts.all())

    return f"The last completed mission is: {last_mission.name}. Commander: {commander_name}. Astronauts: {astronauts}. Spacecraft: {last_mission.spacecraft.name}. Total spacewalks: {num_of_spacewalks}."


def get_most_used_spacecraft():
    most_used_spacecraft = Spacecraft.objects.annotate(num_missions=Count('spacecraft_mission')).order_by('name', '-num_missions').first()

    if not most_used_spacecraft:
        return 'No data.'

    num_missions = most_used_spacecraft.num_missions
    num_astronauts = most_used_spacecraft.spacecraft_mission.values_list('astronauts', flat=True).distinct().count()

    return f"The most used spacecraft is: {most_used_spacecraft.name}, manufactured by {most_used_spacecraft.manufacturer}, used in {num_missions} missions, astronauts on missions: {num_astronauts}."


def decrease_spacecrafts_weight():
    planned_missions = Spacecraft.objects.filter(spacecraft_mission__status=Mission.StatusChoices.PLANNED, weight__gte=200.0).distinct()

    affected_spacecrafts = planned_missions.update(weight=F('weight') - 200.0)

    if affected_spacecrafts == 0:
        return "No changes in weight."

    total_weight = sum(spacecraft.weight for spacecraft in Spacecraft.objects.all())
    avg_weight = total_weight / Spacecraft.objects.count()

    return f"The weight of {affected_spacecrafts} spacecrafts has been decreased. The new average weight of all spacecrafts is {avg_weight:.1f}kg"
