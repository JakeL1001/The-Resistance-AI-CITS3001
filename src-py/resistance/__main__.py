from random_agent import RandomAgent
from agent1 import Agent1
from agent2 import Agent2
from agent3 import Agent3
from game import Game
import pandas as pd


agents = [RandomAgent(name='r1'), 
        RandomAgent(name='r2'),  
        RandomAgent(name='r3'),  
        # RandomAgent(name='r4'),  
        RandomAgent(name='r5'),  
        RandomAgent(name='r6'),  
        RandomAgent(name='r7'),
        Agent3(name="TEST")]



# agents = [Agent1(name='TEST'), 
#         Agent2(name='r2'),  
#         RandomAgent(name='r3'),  
#         # RandomAgent(name='r4'),  
#         RandomAgent(name='r5'),  
#         RandomAgent(name='r6'),  
#         RandomAgent(name='r7'),
#         Agent3(name="r8")]


# agents = [Agent3(name='r1'), 
#         Agent3(name='r2'),  
#         Agent3(name='r3'),  
#         # RandomAgent(name='r4'),  
#         Agent3(name='r5'),  
#         Agent3(name='r6'),  
#         Agent3(name='r7'),
#         Agent3(name="TEST")]


# agents = [Agent1(name='r1'), 
#         Agent1(name='r2'),  
#         Agent1(name='r3'),  
#         # RandomAgent(name='r4'),  
#         Agent1(name='r5'),  
#         Agent1(name='r6'),  
#         Agent1(name='r7'),
#         Agent1(name="TEST")]

# agents = [Agent2(name='r1'), 
#         Agent2(name='r2'),  
#         Agent2(name='r3'),  
#         # RandomAgent(name='r4'),  
#         Agent2(name='r5'),  
#         Agent2(name='r6'),  
#         Agent2(name='r7'),
#         Agent2(name="TEST")]        

# game = Game(agents)
# game.play()
# print(game.missions_lost)



df = pd.DataFrame(list())
df.to_csv('outcomes.csv')

NO_GAMES = 10000

for i in range(NO_GAMES):
        game = Game(agents)
        game.play()


df = pd.read_csv('outcomes.csv')
df = df.reset_index()
df.columns = ['Role', 'Win']
total_wins = df[df['Win'] == 'Won']
spy_wins = df[df['Role'] == 'I was spy' ]
games_as_spy = spy_wins['Win'].count()
spy_wins = spy_wins[spy_wins['Win'] == 'Won']

res_wins = df[df['Role'] == 'I was not spy' ]
games_as_res = res_wins['Win'].count()
res_wins = res_wins[res_wins['Win'] == 'Won']

wins = total_wins['Win'].count()
total_winrate =  wins/NO_GAMES
spy_winrate = spy_wins['Win'].count()/games_as_spy
res_winrate = res_wins['Win'].count()/games_as_res
print('Total winrate was:', total_winrate)
print('Spy winrate was:', spy_winrate)
print('Resistance winrate was:', res_winrate)
