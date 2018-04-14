import random
import ggplot as gp
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

common=49
rare=36
epic=27
legendary=23
frozen=[common,rare,epic,legendary]
pc=0.7016
pr=0.2174
pe=0.0395
pl=0.0084
pgc=0.0147
pgr=0.0147
pge=0.0026
pgl=0.0011
weights=[pc,pr,pe,pl,pgc,pgr,pge,pgl]


def packopen(expansion,weights):
    level=['common','rare','epic','legendary','goldencommon','goldenrare','goldenepic','goldenlegendary']
    cardsget=[]
    cardlevel = random.choices(level, weights, k=5)

    for level in cardlevel:
        if level == 'common' or level == 'goldencommon':
            cardsget.append((level, random.randint(1,expansion[0])))
        elif level == 'rare' or level == 'goldenrare':
            cardsget.append((level, random.randint(1, expansion[1])))
        elif level == 'epic' or level == 'goldenepic':
            cardsget.append((level, random.randint(1, expansion[2])))
        elif level == 'legendary' or level == 'goldenlegendary':
            cardsget.append((level, random.randint(1, expansion[3])))
    #print(cardsget)
    return cardsget

dustgetc=5
dustgetr=20
dustgete=100
dustgetl=400
dustgetgc=50
dustgetgr=100
dustgetge=400
dustgetgl=1600
dustusec=40
dustuser=100
dustusee=400
dustusel=1600

def get_all_cards(common:int, rare:int, epic:int, legendary:int):
    owned = {}
    packopened = 0
    dustneeded = 2 * common * dustusec + 2 * rare * dustuser + 2 * epic * dustusee + legendary * dustusel
    dusthave = 0

    while dustneeded > dusthave:

        cardsget = packopen(frozen,weights)
        packopened += 1

        for card in cardsget:
            if card[0]=='goldencommon':
                dusthave += dustgetgc
            elif card[0]=='goldenrare':
                dusthave += dustgetgr
            elif card[0]=='goldenepic':
                dusthave += dustgetge
            elif card[0]=='goldenlegendary':
                dusthave += dustgetgl
            elif card[0] == 'common':
                if card not in owned.keys():
                    owned[card] = 1
                    dustneeded -= dustusec
                elif owned[card] == 1:
                    owned[card] = 2
                    dustneeded -= dustusec
                else:
                    dusthave += dustgetc
            elif card[0] == 'rare':
                if card not in owned.keys():
                    owned[card] = 1
                    dustneeded -= dustuser
                elif owned[card] == 1:
                    owned[card] = 2
                    dustneeded -= dustuser
                else:
                    dusthave += dustgetr
            elif card[0] == 'epic':
                if card not in owned.keys():
                    owned[card] = 1
                    dustneeded -= dustusee
                elif owned[card] == 1:
                    owned[card] = 2
                    dustneeded -= dustusee
                else:
                    dusthave += dustgete
            elif card[0] == 'legendary':
                if card not in owned.keys():
                    owned[card] = 1
                    dustneeded -= dustusel
                else:
                    dusthave += dustgetl
    return packopened

total=0
outcome = []

for i in range(1000):
    time = get_all_cards(common, rare, epic, legendary)
    total += time
    #print(time)
    outcome.append(time)

outcome = pd.DataFrame(outcome,columns=['times'])
# print(outcome['times'].value_counts())
hist = gp.ggplot(gp.aes(x='times',fill = 'times'.value_counts()), data=outcome) + gp.geom_histogram(bins = 30)
print(hist)
#scatter = gp.ggplot(gp.aes(y='times'), data=outcome) + gp.geom_point(color = 'red')
# print(scatter)
