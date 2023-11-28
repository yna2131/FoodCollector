'''
hhh
'''

from mesa import Model, Agent
from mesa.space import SingleGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import math

import numpy as np
import pandas as pd

# ##constants:
# WIDTH = 20
# HEIGHT = 20
# COUNT_FOOD = 47
# NUM_EXPLORERS = 3
# NUM_COLLECTORS = 2
# STEPS = 1500


# Agent Class
class ExplorerAgent(Agent):
    def __init__(self, id, model):
        super().__init__(id, model)
        self.random.seed(12345)

    def step(self):
        if not self.model.hasStorage:
            self.check_storage()
        else:
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

    def check_storage(self):
        x,y = self.pos
        if self.model.floor[x][y] == 10:
            self.model.hasStorage = True
            self.model.position_storage = (x, y)
        self.move()
    
    def lookforfood(self):
        x,y = self.pos
        if self.model.floor[x][y] > 0 and self.model.floor[x][y] < 10:
            if self.pos not in self.model.positions_food:
                self.model.positions_food.append(self.pos)
        self.move()

## CollectorAgent
class CollectorAgent(Agent):
    def __init__(self, id, model):
        super().__init__(id, model)
        self.random.seed(12345)
        self.hasFood = False
        self.target = None

    def shortest_distance(self, target_position):
        x1, y1 = self.pos
        x2, y2 = target_position

        # Manhattan distance
        return abs(x2 - x1) + abs(y2 - y1)
    
    def getTarget(self):
        distances = [self.shortest_distance(food) for food in self.model.positions_food]
        if distances:
            closests_food_index = distances.index(min(distances))
            closest_food_pos = self.model.positions_food[closests_food_index]
            self.target = closest_food_pos

    def random_move(self):
        neighbors = self.model.grid.get_neighborhood(self.pos, 
                                                     moore = True, 
                                                     include_center = False
        )

        is_possible = [step for step in neighbors if self.model.grid.is_cell_empty(step)]

        if is_possible:
            new_position = self.random.choice(is_possible)
            self.model.grid.move_agent(self, new_position)

    def move(self):
        x, y = self.pos
        x2, y2 = self.target

        dirx = x2 - x
        diry = y2 - y

        a = x
        b = y
        
        if dirx > 0:
            a = a + 1 
        elif dirx < 0:
            a = a - 1

        if diry > 0:
            b = b + 1
        elif diry < 0:
            b = b - 1

        new_position = (a, b)
                
        if self.model.grid.is_cell_empty(new_position):
            self.model.grid.move_agent(self, new_position)
        else:
            self.random_move()

    def pickup(self):
        x, y = self.pos
        if self.model.floor[x][y] > 0 and self.model.floor[x][y] < 10:
            if (x, y) in self.model.positions_food:
                self.hasFood = True
                self.target = self.model.position_storage
                self.model.floor[x][y] -= 1
                if (x, y) in self.model.positions_food and self.model.floor[x][y] == 0:
                    self.model.positions_food.remove((x, y))

    def drop(self):
        self.hasFood = False
        self.target = None
        self.model.collected_food += 1

    def step(self): 
        if self.pos == self.target:
            self.target = None

        if self.hasFood:
            if self.model.hasStorage:
                if self.pos == self.model.position_storage:
                    self.drop()
                else:
                    self.move()
        else:
            self.pickup()
            if self.hasFood:
                return
            else:
                if self.target != None:
                    self.move()
                else:
                    self.getTarget()

# Model Class
class FoodModel(Model):
    def __init__(self, width, height, num_explorers, num_collectors, count_food):
        self.random.seed(12345)
        self.hasStorage = False
        self.num_explorers = num_explorers
        self.num_collectors = num_collectors
        self.count_food = count_food
        self.positions_food = []
        self.position_storage = None
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
            agent_reporters={"hasFood": "hasFood", "hasStorage": "hasStorage"},
            model_reporters={"Floor": self.get_floor, "AgentPositions": self.get_agent_positions}
        )

    def get_floor(self):
        return self.floor.copy().tolist()


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

    def get_agent_positions(self):
        positions = np.zeros((self.grid.width, self.grid.height))

        for agent in self.schedule.agents:
            x, y = agent.pos
            positions[x][y] = 1

        return positions.tolist() 


    def step(self):
        self.step_count += 1
        if self.step_count % 5 == 0:
            self.place_food()
        self.schedule.step()
        self.datacollector.collect(self)