from random_agent import RandomAgent
from agent1 import Agent1
from game import Game

agents = [RandomAgent(name='r1'), 
        RandomAgent(name='r2'),  
        RandomAgent(name='r3'),  
        # RandomAgent(name='r4'),  
        RandomAgent(name='r5'),  
        RandomAgent(name='r6'),  
        RandomAgent(name='r7'),
        Agent1(name="TEST")]

game = Game(agents)
game.play()
print(game)


