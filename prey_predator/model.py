from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from prey_predator.agents import Sheep, Wolf, GrassPatch
from prey_predator.schedule import RandomActivationByBreed


class WolfSheep(Model):
    height = 20
    width = 20

    initial_sheep = 100
    initial_wolves = 50

    sheep_reproduce = 0.04
    wolf_reproduce = 0.05

    wolf_gain_from_food = 20

    grass = False
    grass_regrowth_time = 30
    sheep_gain_from_food = 4

    description = (
        "A model for simulating wolf and sheep (predator-prey) ecosystem modelling."
    )

    def __init__(self,
                 height=20,
                 width=20,
                 initial_sheep=100,
                 initial_wolves=50,
                 sheep_reproduce=0.04,
                 wolf_reproduce=0.05,
                 wolf_gain_from_food=20,
                 grass=True,
                 grass_regrowth_time=30,
                 sheep_gain_from_food=4,
                 grass_countdown=10,
                 initial_sheep_energy=10,
                 initial_wolf_energy=10,
                 chasing_mode=False):

        super().__init__()
        self.height = height
        self.width = width
        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves
        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.wolf_gain_from_food = wolf_gain_from_food
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.sheep_gain_from_food = sheep_gain_from_food
        self.grass_countdown = grass_countdown
        self.initial_sheep_energy = initial_sheep_energy
        self.initial_wolf_energy = initial_wolf_energy
        self.chasing_mode = chasing_mode

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector({
            "Wolves":
            lambda m: m.schedule.get_breed_count(Wolf),
            "Sheep":
            lambda m: m.schedule.get_breed_count(Sheep),
        })

        # Create sheep:
        # ... to be completed
        for _ in range(self.initial_sheep):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            a = Sheep(self.next_id(), (x, y), self, moore=True,
                      energy=self.initial_sheep_energy, chasing_mode=self.chasing_mode)
            self.schedule.add(a)
            self.grid.place_agent(a, (x, y))

        # Create wolves
        # ... to be completed
        for _ in range(self.initial_wolves):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            a = Wolf(self.next_id(), (x, y), self, moore=True,
                     energy=self.initial_wolf_energy, chasing_mode=self.chasing_mode)
            self.schedule.add(a)
            self.grid.place_agent(a, (x, y))

        # Create grass patches
        # ... to be completed
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                a = GrassPatch(self.next_id(), (x, y),
                               self,
                               fully_grown=True,
                               countdown=self.grass_countdown)
                self.schedule.add(a)
                self.grid.place_agent(a, (x, y))

    def step(self):
        # ... to be completed
        self.schedule.step()

        # Collect data
        self.datacollector.collect(self)

    def run_model(self, step_count=200):

        # ... to be completed
        for _ in range(step_count):
            self.step()
