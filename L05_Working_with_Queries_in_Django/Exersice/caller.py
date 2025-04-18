import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from typing import List

from main_app.models import ArtworkGallery, Meal, Dungeon, Workout
from main_app.models import Laptop
from main_app.models import ChessPlayer


def show_highest_rated_art():
    best_artwork = ArtworkGallery.objects.order_by('-rating', 'id').first()

    return f"{best_artwork.art_name} is the highest-rated art with a {best_artwork.rating} rating!"


def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery):
    ArtworkGallery.objects.bulk_create([first_art, second_art])


def delete_negative_rated_arts():
    ArtworkGallery.objects.filter(rating__lt=0).delete()


def show_the_most_expensive_laptop():
    most_expensive_laptop = Laptop.objects.order_by('-price', '-id').first()

    return f"{most_expensive_laptop.brand} is the most expensive laptop available for {most_expensive_laptop.price}$!"


def bulk_create_laptops(args: List[Laptop]):
    Laptop.objects.bulk_create(args)


def update_to_512_GB_storage():
    Laptop.objects.filter(brand__in=['Asus', 'Lenovo']).update(storage=512)


def update_to_16_GB_memory():
    Laptop.objects.filter(brand__in=['Apple', 'Dell', 'Acer']).update(memory=16)


def update_operation_systems():
    Laptop.objects.filter(brand='Asus').update(operation_system='Windows')
    Laptop.objects.filter(brand='Apple').update(operation_system='MacOS')
    Laptop.objects.filter(brand__in=['Dell', 'Acer']).update(operation_system='Linux')
    Laptop.objects.filter(brand='Lenovo').update(operation_system='Chrome OS')


def delete_inexpensive_laptops():
    Laptop.objects.filter(price__lt=1200).delete()


def bulk_create_chess_players(args: List[ChessPlayer]) -> None:
    ChessPlayer.objects.bulk_create(args)


def delete_chess_players() -> None:
    # TODO: Get the metadata of the title field
    ChessPlayer.objects.filter(title="no title").delete()


def change_chess_games_won() -> None:
    ChessPlayer.objects.filter(title="GM").update(games_won=30)


def change_chess_games_lost() -> None:
    ChessPlayer.objects.filter(title="no title").update(games_lost=25)


def change_chess_games_drawn() -> None:
    ChessPlayer.objects.update(games_drawn=10)
    # UPDATE chess
    # SET games_drawn = 10


def grand_chess_title_GM() -> None:
    ChessPlayer.objects.filter(rating__gte=2400).update(title="GM")
    # UPDATE chess
    # SET title = "GM"
    # WHERE rating >= 2400


def grand_chess_title_IM() -> None:
    ChessPlayer.objects.filter(rating__range=[2300, 2399]).update(title="IM")
    # UPDATE chess
    # SET title = "IM"
    # WHERE rating BETWEEN 2300 AND 2399


def grand_chess_title_FM() -> None:
    ChessPlayer.objects.filter(rating__range=[2200, 2299]).update(title="FM")


def grand_chess_title_regular_player() -> None:
    ChessPlayer.objects.filter(rating__range=[0, 2199]).update(title="regular player")


def set_new_chefs():
    meals = Meal.objects.all()
    for meal in meals:
        if meal.meal_type == 'Breakfast':
            meal.chef = 'Gordon Ramsay'
        elif meal.meal_type == 'Lunch':
            meal.chef = 'Julia Child'
        elif meal.meal_type == 'Dinner':
            meal.chef = 'Jamie Oliver'
        elif meal.meal_type == 'Snack':
            meal.chef = 'Thomas Keller'
        meal.save()


def set_new_preparation_times():
    meals = Meal.objects.all()
    for meal in meals:
        if meal.meal_type == 'Breakfast':
            meal.preparation_time = '10 minutes'
        elif meal.meal_type == 'Lunch':
            meal.preparation_time = '12 minutes'
        elif meal.meal_type == 'Dinner':
            meal.preparation_time = '15 minutes'
        elif meal.meal_type == 'Snack':
            meal.preparation_time = '5 minutes'
        meal.save()


def update_low_calorie_meals():
    Meal.objects.filter(meal_type__in=['Breakfast', 'Dinner']).update(calories=400)


def update_high_calorie_meals():
    Meal.objects.filter(meal_type__in=['Lunch', 'Snack']).update(calories=700)


def delete_lunch_and_snack_meals():
    Meal.objects.filter(meal_type__in=['Lunch', 'Snack']).delete()


def show_hard_dungeons():
    hard_dungeons = Dungeon.objects.filter(difficulty='Hard').order_by('-location')
    result = []
    for dungeon in hard_dungeons:
        result.append(f"{dungeon.name} is guarded by {dungeon.boss_name} who has {dungeon.boss_health} health points!")
    return '\n'.join(result)


def bulk_create_dungeons(args: List[Dungeon]):
    Dungeon.objects.bulk_create(args)


def update_dungeon_names():
    dungeons = Dungeon.objects.all()

    # Prepare a list to collect updated instances
    instances_to_update = []

    for dungeon in dungeons:
        new_name = None
        if dungeon.difficulty == 'Easy':
            new_name = 'The Erased Thombs'
        elif dungeon.difficulty == 'Medium':
            new_name = 'The Coral Labyrinth'
        elif dungeon.difficulty == 'Hard':
            new_name = 'The Lost Haunt'

        if new_name:
            dungeon.name = new_name
            instances_to_update.append(dungeon)

    Dungeon.objects.bulk_update(instances_to_update, ['name'])



def update_dungeon_bosses_health():
    dungeons = Dungeon.objects.all()

    for dungeon in dungeons:
        if dungeon.difficulty != 'Easy':
            dungeon.boss_health = 500
            dungeon.save()


def update_dungeon_recommended_levels():
    dungeons = Dungeon.objects.all()

    for dungeon in dungeons:
        if dungeon.difficulty == 'Easy':
            dungeon.recommended_level = 25
        elif dungeon.difficulty == 'Medium':
            dungeon.recommended_level = 50
        elif dungeon.difficulty == 'Hard':
            dungeon.recommended_level = 75

        dungeon.save()


def update_dungeon_rewards():
    dungeons = Dungeon.objects.all()

    for dungeon in dungeons:
        if dungeon.boss_health == 500:
            dungeon.reward = '1000 Gold'
        elif dungeon.location.startswith('E'):
            dungeon.reward = 'New dungeon unlocked'
        elif dungeon.location.endswith('s'):
            dungeon.reward = 'Dragonheart Amulet'

        dungeon.save()


def set_new_locations():
    dungeons = Dungeon.objects.all()

    for dungeon in dungeons:
        if dungeon.recommended_level == 25:
            dungeon.location = 'Enchanted Maze'
        elif dungeon.recommended_level == 50:
            dungeon.location = 'Grimstone Mines'
        elif dungeon.recommended_level == 75:
            dungeon.location = 'Shadowed Abyss'

        dungeon.save()


def show_workouts():
    workouts = Workout.objects.filter(workout_type__in=['Calisthenics', 'CrossFit']).order_by('id')
    output = []
    for workout in workouts:
        output.append(f"{workout.name} from {workout.workout_type} type has {workout.difficulty} difficulty!")
    return ' '.join(output)


def get_high_difficulty_cardio_workouts():
    workouts = Workout.objects.filter(workout_type='Cardio', difficulty='High').order_by('instructor')
    return workouts


def set_new_instructors():
    workouts = Workout.objects.all()
    for workout in workouts:
        if workout.workout_type == 'Cardio':
            workout.instructor = 'John Smith'
        elif workout.workout_type == 'Strength':
            workout.instructor = 'Michael Williams'
        elif workout.workout_type == 'Yoga':
            workout.instructor = 'Emily Johnson'
        elif workout.workout_type == 'CrossFit':
            workout.instructor = 'Sarah Davis'
        elif workout.workout_type == 'Calisthenics':
            workout.instructor = 'Chris Heria'
        workout.save()


def set_new_duration_times():
    workouts = Workout.objects.all()
    for workout in workouts:
        if workout.instructor == 'John Smith':
            workout.duration = '15 minutes'
        elif workout.instructor == 'Sarah Davis':
            workout.duration = '30 minutes'
        elif workout.instructor == 'Chris Heria':
            workout.duration = '45 minutes'
        elif workout.instructor == 'Michael Williams':
            workout.duration = '1 hour'
        elif workout.instructor == 'Emily Johnson':
            workout.duration = '1 hour and 30 minutes'
        workout.save()


def delete_workouts():
    workouts = Workout.objects.all()
    for workout in workouts:
        if workout.workout_type not in ['Strength', 'Calisthenics']:
            workout.delete()
