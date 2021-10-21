import pandas as pd

if __name__ == "__main__":
    files = ["BasicBayesBasic.csv", "BasicBayesCombination.csv", "BasicBayesJond.csv", "BasicBayesRandom.csv", 
            "BayesJondBasic.csv", "BayesJondCombination.csv", "BayesJondJond.csv", "BayesJondRandom.csv"]
    for x in files:
        print(x)
        df = pd.read_csv(x)
        df = df.reset_index(drop=True)
        # print(df)

        df.columns = ['Players','Role', 'Win']
        total_wins = df[df['Win'] == 'Won']
        spy_wins = df[df['Role'] == 'I was spy' ]
        games_as_spy = spy_wins['Win'].count()
        spy_wins = spy_wins[spy_wins['Win'] == 'Won']

        res_wins = df[df['Role'] == 'I was not spy' ]
        games_as_res = res_wins['Win'].count()
        res_wins = res_wins[res_wins['Win'] == 'Won']

        wins = total_wins['Win'].count()
        total_winrate =  (spy_wins['Win'].count() + res_wins['Win'].count()) / (games_as_res + games_as_spy)
        spy_winrate = spy_wins['Win'].count()/games_as_spy
        res_winrate = res_wins['Win'].count()/games_as_res
        print('Total winrate was:', total_winrate)
        print('Spy winrate was:', spy_winrate)
        print("Games as spy =", games_as_spy)
        print('Resistance winrate was:', res_winrate)
        print("Games as Resistance =", games_as_res)
        print()