'''
hhh
'''

from mesa import Model, Agent
from mesa.space import SingleGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import math

import numpy as np



# Agent Class
## ExplorerAgent
class ExplorerAgent(Agent):
    def __init__(self, id, model):
        super().__init__(id, model)
        self.random.seed(12345)

    def step(self):
        if not self.model.hasStorage:
            self.lookforstorage()
        else:
            unfound_food = 47 - self.model.found_food
            if unfound_food > 0:
                self.lookforfood()

    def move(self):
        neighbors = self.model.grid.get_neighborhood(self.pos, 
                                                     moore = True, 
                                                     include_center = False
        )

        is_possible = [step for step in neighbors if self.model.grid.is_cell_empty(step)]

        if is_possible:
            new_position = self.random.choice(is_possible)
            self.model.grid.move_agent(self, new_position)

    def lookforstorage(self):
        neighbors = self.model.grid.get_neighborhood(self.pos, 
                                                        moore = True, 
                                                        include_center = False
        )

        for neighbor in neighbors:
            x, y = neighbor
            if self.model.floor[x][y] == 10:
                self.model.hasStorage = True
                self.model.position_storage.append(neighbor)
                break
        self.move()
    
    def lookforfood(self):
        neighbors = self.model.grid.get_neighborhood(self.pos, 
                                                        moore = True, 
                                                        include_center = False
        )

        for neighbor in neighbors:
            x, y = neighbor
            if self.model.floor[x][y] > 0:
                self.model.found_food += self.model.floor[x][y]
                self.model.positions_food.append(neighbor)
                break
        self.move()

## CollectorAgent
class CollectorAgent(Agent):
    def __init__(self, id, model):
        super().__init__(id, model)
        self.random.seed(12345)
        self.hasFood = False

    def pickup(self):
        neighbors = self.model.grid.get_neighborhood(self.pos, 
                                                     moore = True, 
                                                     include_center = False
        )

        for neighbor in neighbors:
            x, y = neighbor
            if self.model.floor[x][y] > 0 and self.model.floor[x][y] < 10:
                self.hasFood = True
                self.model.floor[x][y] -= 1
                if (x, y) in self.model.positions_food and self.model.floor[x][y] == 0:
                    self.model.positions_food.remove((x, y))
                break

    def drop(self):
        neighbors = self.model.grid.get_neighborhood(self.pos, 
                                                     moore = True, 
                                                     include_center = False
        )

        for neighbor in neighbors:
            if neighbor == self.model.position_storage[0]:
                self.hasFood = False
                self.model.collected_food += 1

    def step(self):
        self.move()
        if self.hasFood and self.model.hasStorage:
            self.drop()
        elif self.hasFood and not self.model.hasStorage:
            self.move()
        else:
            self.pickup()

    def move(self):
        # We have to implement the shortest path movement instead of the random one
        neighbors = self.model.grid.get_neighborhood(self.pos, 
                                                     moore = True, 
                                                     include_center = False
        )

        is_possible = [step for step in neighbors if self.model.grid.is_cell_empty(step)]

        if is_possible:
            new_position = self.random.choice(is_possible)
            self.model.grid.move_agent(self, new_position)

# Model Class
class FoodModel(Model):
    def __init__(self, width, height, num_explorers, num_collectors, count_food):
        self.random.seed(12345)
        self.hasStorage = False
        self.num_explorers = num_explorers
        self.num_collectors = num_collectors
        self.count_food = count_food
        self.positions_food = []
        self.position_storage = []
        self.found_food = 0
        self.collected_food = 0
        self.placed_food = 0
        self.step_count = 0

        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(width, height, torus = False)

        self.floor = np.zeros((width, height))
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        self.floor[x][y] = 10

        for i in range(self.num_explorers):
            agent = ExplorerAgent(i, self)
            self.schedule.add(agent)
            unplaced = True
            while unplaced:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                if self.floor[x][y] == 0:
                    if self.grid.is_cell_empty((x, y)):
                        unplaced = False
            self.grid.place_agent(agent, (x,y))

        for i in range(self.num_collectors):
            agent = CollectorAgent(i+self.num_explorers, self)
            self.schedule.add(agent)
            unplaced = True
            while unplaced:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                if self.floor[x][y] == 0:
                    if self.grid.is_cell_empty((x, y)):
                        unplaced = False
            self.grid.place_agent(agent, (x,y))

        self.datacollector = DataCollector(
            agent_reporters = {"hasFood": "hasFood", "hasStorage": "hasStorage"},
            model_reporters = {"Floor": self.get_floor}
        )

    def get_floor(self):
        return self.floor.copy()

    def place_food(self):
        if self.placed_food < self.count_food:
            num = self.random.randint(2,5)
            missing_food = self.count_food - self.placed_food
            val = min(num, missing_food)

            for i in range(val):
                unplaced = True
                while unplaced:
                    x = self.random.randrange(self.grid.width)
                    y = self.random.randrange(self.grid.height)
                    if self.floor[x][y] < 100:
                        if self.grid.is_cell_empty((x, y)):
                            unplaced = False
                self.floor[x][y] += 1
            self.placed_food += val

    def step(self):
        self.step_count += 1
        if self.step_count % 5 == 0:
            self.place_food()
        self.schedule.step()
        self.datacollector.collect(self)