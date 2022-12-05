"""Unit tests on agents"""
from prey_predator.agents import Wolf, Sheep, GrassPatch
from prey_predator.model import WolfSheep

def test_reproduce_Wolf():

    model = WolfSheep(initial_wolves=1, initial_sheep=0, wolf_reproduce=1)
    initial_wolf_num = model.initial_wolves

    first_wolf = next(iter(model.schedule.agents_by_breed[Wolf].values()))
    first_wolf.try_reproduce()

    assert model.schedule.get_breed_count(Wolf) == initial_wolf_num + 1
    

def test_reproduce_Sheep():

    model = WolfSheep(initial_wolves=0, initial_sheep=1, sheep_reproduce=1)
    initial_sheep_num = model.initial_sheep

    first_sheep = next(iter(model.schedule.agents_by_breed[Sheep].values()))
    first_sheep.try_reproduce()

    assert model.schedule.get_breed_count(Sheep) ==  initial_sheep_num + 1



def test_try_eat_Wolf():

    model = WolfSheep(width=1, height=1, initial_wolves=1, initial_sheep=1)
    initial_sheep_num = model.initial_sheep
    initial_wolf_energy = model.initial_wolf_energy

    first_wolf = next(iter(model.schedule.agents_by_breed[Wolf].values()))
    first_wolf.try_eat()
    
    assert model.schedule.get_breed_count(Sheep) == initial_sheep_num - 1
    assert first_wolf.energy == initial_wolf_energy + model.wolf_gain_from_food
    

def test_try_eat_Sheep():

    model = WolfSheep(width=1, height=1, initial_wolves=0, initial_sheep=1)
    initial_sheep_energy = model.initial_sheep_energy

    first_sheep = next(iter(model.schedule.agents_by_breed[Sheep].values()))
    first_sheep.try_eat()

    grass_patch = next(iter(model.schedule.agents_by_breed[GrassPatch].values()))

    assert first_sheep.energy == initial_sheep_energy + model.sheep_gain_from_food
    assert grass_patch.fully_grown == False

    first_sheep.try_eat()

    assert first_sheep.energy == initial_sheep_energy + model.sheep_gain_from_food
    assert grass_patch.fully_grown == False


def test_try_die_from_energy():

    model = WolfSheep(width=1, height=1, initial_wolves=1, initial_sheep=1, initial_sheep_energy=1, initial_wolf_energy=1)
    initial_wolves = model.initial_wolves
    initial_sheeps = model.initial_sheep

    first_wolf = next(iter(model.schedule.agents_by_breed[Wolf].values()))
    first_wolf.energy -= 1
    assert first_wolf.energy == 0
    
    first_wolf.try_die_from_energy()
    assert model.schedule.get_breed_count(Wolf) == initial_wolves - 1

    first_sheep = next(iter(model.schedule.agents_by_breed[Sheep].values()))
    first_sheep.energy -= 1
    assert first_sheep.energy == 0
    
    first_sheep.try_die_from_energy()
    assert model.schedule.get_breed_count(Sheep) == initial_sheeps - 1


def test_grow():

    model = WolfSheep(width=1, height=1, initial_wolves=0, initial_sheep=1, initial_sheep_energy=1)

    first_sheep = next(iter(model.schedule.agents_by_breed[Sheep].values()))
    first_sheep.try_eat()

    grass_patch = next(iter(model.schedule.agents_by_breed[GrassPatch].values()))
    assert grass_patch.fully_grown == False
    
    for _ in range(grass_patch.countdown):
        grass_patch.grow()
    
    assert grass_patch.fully_grown == True