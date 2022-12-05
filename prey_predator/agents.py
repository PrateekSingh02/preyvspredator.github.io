from mesa import Agent
from prey_predator.random_walk import RandomWalker


class Sheep(RandomWalker):

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None, chasing_mode=False):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.chasing_mode = chasing_mode

    def try_reproduce(self):
        if self.random.random() <= self.model.sheep_reproduce:
            self.energy //= 2
            a = Sheep(self.model.next_id(), self.pos,
                      self.model, self.moore, energy=self.energy)
            self.model.schedule.add(a)
            self.model.grid.place_agent(a, self.pos)

    def try_eat(self):
        cell_agents = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cell_agents:
            if isinstance(agent, GrassPatch) and agent.fully_grown:
                self.energy += self.model.sheep_gain_from_food
                agent.fully_grown = False
                break

    def try_die_from_energy(self):
        if self.energy <= 0:
            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)

    def runaway_move(self):
        neighbor_cells = self.model.grid.get_neighborhood(
            self.pos, moore=self.moore, include_center=False)

        neighbor_score = {neighbor_cell: 0 for neighbor_cell in neighbor_cells}
        for neighbor_cell in neighbor_cells:
            cell_agents = self.model.grid.get_cell_list_contents(
                [neighbor_cell])
            for agent in cell_agents:
                if isinstance(agent, Wolf):
                    neighbor_score[agent.pos] -= 2
                    enemy_possible_moves = self.model.grid.get_neighborhood(
                        agent.pos, moore=self.moore, include_center=False)
                    for bad_position in (set(enemy_possible_moves) & set(neighbor_cells)):
                        neighbor_score[bad_position] -= 1
                if isinstance(agent, GrassPatch) and agent.fully_grown:
                    neighbor_score[agent.pos] += 1
        move_score = list(neighbor_score.items())
        self.random.shuffle(move_score)
        next_move = max(move_score, key=lambda x: x[1])[0]
        self.model.grid.move_agent(self, next_move)

    def step(self):
        # ... to be completed
        if self.chasing_mode:
            self.runaway_move()
        else:
            self.random_move()
        self.energy -= 1
        self.try_reproduce()
        self.try_eat()
        self.try_die_from_energy()


class Wolf(RandomWalker):

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None, chasing_mode=False):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.chasing_mode = chasing_mode

    def try_reproduce(self):
        if self.random.random() <= self.model.wolf_reproduce:
            self.energy //= 2
            a = Wolf(self.model.next_id(), self.pos,
                     self.model, self.moore, energy=self.energy)
            self.model.schedule.add(a)
            self.model.grid.place_agent(a, self.pos)

    def try_eat(self):
        cell_agents = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cell_agents:
            if isinstance(agent, Sheep):
                self.energy += int(self.model.wolf_gain_from_food * (
                    min(1, agent.energy / self.model.initial_sheep_energy)))
                self.model.schedule.remove(agent)
                self.model.grid.remove_agent(agent)
                break

    def try_die_from_energy(self):
        if self.energy <= 0:
            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)

    def chasing_move(self):
        neighbor_cells = self.model.grid.get_neighborhood(self.pos, moore=self.moore,include_center=False)

        neighbor_score = {neighbor_cell: 0 for neighbor_cell in neighbor_cells}
        for neighbor_cell in neighbor_cells:
            cell_agents = self.model.grid.get_cell_list_contents(
                [neighbor_cell])
            for agent in cell_agents:
                if isinstance(agent, Sheep):
                    neighbor_score[agent.pos] += 1
        move_score = list(neighbor_score.items())
        self.random.shuffle(move_score)
        next_move = max(move_score, key=lambda x: x[1])[0]
        self.model.grid.move_agent(self, next_move)

    def step(self):
        if self.chasing_mode:
            self.chasing_move()
        else:
            self.random_move()
        self.energy -= 1
        self.try_reproduce()
        self.try_eat()
        self.try_die_from_energy()


class GrassPatch(Agent):

    def __init__(self, unique_id, pos, model, fully_grown, countdown):

        super().__init__(unique_id, model)
        # ... to be completed
        self.fully_grown = fully_grown
        self.countdown = countdown
        self.current_countdown = self.countdown

    def grow(self):
        self.current_countdown -= 1
        if self.fully_grown or self.current_countdown == 0:
            self.current_countdown = self.countdown
            self.fully_grown = True

    def step(self):
        # ... to be completed
        self.grow()
