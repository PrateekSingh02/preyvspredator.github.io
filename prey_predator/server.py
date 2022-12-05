import os
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from prey_predator.agents import Wolf, Sheep, GrassPatch
from prey_predator.model import WolfSheep


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if isinstance(agent, Sheep):
        # ... to be completed
        portrayal = {"Shape": f"{os.path.dirname(os.path.realpath(__file__))}/sheep.png",
                    "x": 0,
                    "y": 0,
                    "scale": 0.5,
                    "Layer": 1,
                    "text": agent.energy}

        # portrayal = {"Shape": "circle",
        #             "Color": "white",
        #             "Filled": "true",
        #             "Layer": 1,
        #             "r": 0.5}

    elif isinstance(agent, Wolf):
        # ... to be completed
        portrayal = {"Shape": f"{os.path.dirname(os.path.realpath(__file__))}/wolf.png",
                    "x": 0,
                    "y": 0,
                    "scale": 0.5,
                    "Layer": 1,
                    "text": agent.energy}
        
        # portrayal = {"Shape": "circle",
        #             "Color": "red",
        #             "Filled": "true",
        #             "Layer": 2,
        #             "r": 0.5}

    elif isinstance(agent, GrassPatch):
        if agent.fully_grown:
        # ... to be completed
            portrayal = {"Shape": "rect",
                        "Color": "green",
                        "Filled": "true",
                        "Layer": 0,
                        "w": 1,
                        "h": 1}
        else:
            portrayal = {"Shape": "rect",
                        "Color": "#ffffe0",
                        "Filled": "true",
                        "Layer": 0,
                        "w": 1,
                        "h": 1}

    return portrayal

model_params = {
    # ... to be completed
    "initial_wolves": UserSettableParameter("slider", "Initial number of wolves", 10, 10, 200, 1),
    "wolf_reproduce": UserSettableParameter("slider", "Wolf reproduce rate", 0.09, 0, 1, 0.01),
    "wolf_gain_from_food": UserSettableParameter("slider", "Energy gained from eating sheep", 10, 1, 50, 1),
    "initial_wolf_energy": UserSettableParameter("slider", "Wolf energy at creation", 4, 1, 100, 1),

    "initial_sheep": UserSettableParameter("slider", "Initial number of sheeps", 40, 10, 200, 1),
    "sheep_reproduce": UserSettableParameter("slider", "Sheep reproduce rate", 0.09, 0, 1, 0.01),
    "sheep_gain_from_food": UserSettableParameter("slider", "Energy gained from eating grass", 10, 1, 20, 1),
    "initial_sheep_energy": UserSettableParameter("slider", "Sheep energy at creation", 10, 1, 100, 1),
    
    "grass_countdown": UserSettableParameter("slider", "Grass growing time after being eaten", 16, 1, 100, 1),
    "chasing_mode": UserSettableParameter("checkbox", "Chasing mode", False)
}

canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Wolves", "Color": "#AA0000"}, {"Label": "Sheep", "Color": "#666666"}]
)

server = ModularServer(
    WolfSheep, [canvas_element, chart_element], "Prey Predator Model", model_params
)
server.port = 8521