import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Astronaut, Mission, Spacecraft
from django.db.models import F, Q, Count, Sum, Avg


def get_astronauts(search_string=None):
    if search_string is None:
        return ""

    astronauts = Astronaut.objects.filter(
        Q(name__icontains=search_string) |
        Q(phone_number__icontains=search_string)
    ).order_by('name')

    if not astronauts:
        return ""

    result = []
    for astronaut in astronauts:
        status = "Active" if astronaut.is_active else "Inactive"
        result.append(f"Astronaut: {astronaut.name}, phone number: {astronaut.phone_number}, status: {status}")

    return "\n".join(result)


def get_top_astronaut():
    top_astronaut = Astronaut.objects.annotate(
        num_missions=Count('missions')
    ).order_by('-num_missions', 'phone_number').first()

    if not top_astronaut or top_astronaut.num_missions == 0:
        return "No data."

    return f"Top Astronaut: {top_astronaut.name} with {top_astronaut.num_missions} missions."


def get_top_commander():
    top_commander = Astronaut.objects.annotate(
        num_commanded_missions=Count('commanded_missions')
    ).order_by('-num_commanded_missions', 'phone_number').first()

    if not top_commander or top_commander.num_commanded_missions == 0:
        return "No data."

    return f"Top Commander: {top_commander.name} with {top_commander.num_commanded_missions} commanded missions."


def get_last_completed_mission():
    last_completed_mission = Mission.objects.filter(status='Completed').order_by('-launch_date').first()

    if not last_completed_mission:
        return "No data."

    mission_name = last_completed_mission.name
    commander = last_completed_mission.commander
    commander_name = commander.name if commander else "TBA"
    spacecraft_name = last_completed_mission.spacecraft.name

    astronauts = last_completed_mission.astronauts.order_by('name')

    astronaut_names = ", ".join(astronaut.name for astronaut in astronauts)

    total_spacewalks = astronauts.aggregate(Sum('spacewalks'))['spacewalks__sum'] or 0

    return (f"The last completed mission is: {mission_name}. "
            f"Commander: {commander_name}. "
            f"Astronauts: {astronaut_names}. "
            f"Spacecraft: {spacecraft_name}. "
            f"Total spacewalks: {total_spacewalks}.")


def get_most_used_spacecraft():
    spacecrafts = Spacecraft.objects.annotate(num_missions=Count('missions')).order_by('-num_missions', 'name')

    if not spacecrafts.exists() or spacecrafts.first().num_missions == 0:
        return "No data."

    most_used_spacecraft = spacecrafts.first()

    spacecraft_name = most_used_spacecraft.name
    manufacturer = most_used_spacecraft.manufacturer
    num_missions = most_used_spacecraft.num_missions

    unique_astronauts_count = Astronaut.objects.filter(missions__spacecraft=most_used_spacecraft).distinct().count()

    return (f"The most used spacecraft is: {spacecraft_name}, manufactured by {manufacturer}, "
            f"used in {num_missions} missions, astronauts on missions: {unique_astronauts_count}.")


def decrease_spacecrafts_weight():
    spacecrafts = Spacecraft.objects.filter(
        missions__status='Planned'
    ).distinct().filter(
        weight__gte=200.0
    )

    num_of_spacecrafts_affected = spacecrafts.count()

    if num_of_spacecrafts_affected == 0:
        return "No changes in weight."

    for spacecraft in spacecrafts:
        new_weight = spacecraft.weight - 200.0
        spacecraft.weight = max(new_weight, 0.0)
        spacecraft.save()

    avg_weight = Spacecraft.objects.all().aggregate(avg_weight=Avg('weight'))['avg_weight']

    avg_weight = round(avg_weight or 0.0, 1)

    return (f"The weight of {num_of_spacecrafts_affected} spacecrafts has been decreased. "
            f"The new average weight of all spacecrafts is {avg_weight}kg")
