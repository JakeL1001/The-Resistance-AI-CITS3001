import pandas as pd

if __name__ == "__main__":
    files = ["BasicBayesBasic.csv", "BasicBayesCombination.csv", "BasicBayesJond.csv", "BasicBayesRandom.csv",  # List of files to analyse
             "BayesJondBasic.csv", "BayesJondCombination.csv", "BayesJondJond.csv", "BayesJondRandom.csv"]
    # files = ["RandomAgentBasic.csv", "RandomAgentCombination.csv", "RandomAgentJond.csv", "RandomAgentRandom.csv",] # Analyses the RandomAgent files if tested
    
    for x in files: # For all of the files in the list
        # print(x)
        df = pd.read_csv(x) # Reads the file
        df = df.reset_index(drop=True) # Resets the index of dataframe

        df.columns = ['Players','Role', 'Win']
        total_wins = df[df['Win'] == 'Won'] # creates a dataframe containing only wins
        spy_wins = df[df['Role'] == 'I was spy' ] # creates a dataframe containing only spy games
        games_as_spy = spy_wins['Win'].count() # Counts the number of games as spy
        spy_wins = spy_wins[spy_wins['Win'] == 'Won'] # creates a dataframe containing only spy wins

        res_wins = df[df['Role'] == 'I was not spy' ] # creates a dataframe containing only resistance games
        games_as_res = res_wins['Win'].count() # Counts the number of games as resistance
        res_wins = res_wins[res_wins['Win'] == 'Won'] # creates a dataframe containing only resistance wins

        wins = total_wins['Win'].count() # Counts the number of wins
        total_winrate =  (spy_wins['Win'].count() + res_wins['Win'].count()) / (games_as_res + games_as_spy) # Calculates the winrate
        spy_winrate = spy_wins['Win'].count()/games_as_spy # Calculates the winrate of spy games
        res_winrate = res_wins['Win'].count()/games_as_res # Calculates the winrate of resistance games
        print('Total winrate was:', total_winrate) # Prints the winrate
        print('Spy winrate was:', spy_winrate) # Prints the spy winrate
        print("Games as spy =", games_as_spy) # Prints the number of games as spy
        print('Resistance winrate was:', res_winrate) # Prints the resistance winrate
        print("Games as Resistance =", games_as_res) # Prints the number of games as resistance
        print()