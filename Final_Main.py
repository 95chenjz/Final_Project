import random
common=49
rare=36
epic=27
lengendary=23
frozen=[common,rare,epic,lengendary]
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
    level=['common','rare','epic','lengendary','goldencommon','goldenrare','goldenepic','goldenlengendary']
    cardsget=[]
    for i in range(5):
        cardlevel=random.choices(level,weights)
        if cardlevel[0]=='common' or cardlevel[0]=='goldencommon':
            cardsget.append(cardlevel[0]+','+str(random.randint(1,expansion[0])))
        elif cardlevel[0]=='rare' or cardlevel[0]=='goldenrare':
            cardsget.append(cardlevel[0] + ','+str(random.randint(1, expansion[1])))
        elif cardlevel[0]=='epic' or cardlevel[0]=='goldenepic':
            cardsget.append(cardlevel[0] +','+ str(random.randint(1, expansion[2])))
        elif cardlevel[0]=='lengendary' or cardlevel[0]=='goldenlengendary':
            cardsget.append(cardlevel[0] +','+ str(random.randint(1, expansion[3])))
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
owned={}
dustneeded=2*common*dustusec+2*rare*dustuser+2*epic*dustusee+lengendary*dustusel
dusthave=0
packopened=0
while dustneeded>dusthave:
    cardsget=packopen(frozen,weights)
    packopened+=1
    for card in cardsget:
        if card.split(',')[0]=='goldencommon':
            dusthave+=dustgetgc
        elif card.split(',')[0]=='goldenrare':
            dusthave += dustgetgr
        elif card.split(',')[0]=='goldenepic':
            dusthave += dustgetge
        elif card.split(',')[0]=='goldenlengendary':
            dusthave += dustgetgl
        elif card.split(',')[0]=='common':
            if card not in owned.keys():
                owned[card]=1
                dustneeded-=dustusec
            elif owned[card]==1:
                owned[card]=2
                dustneeded -= dustusec
            else:
                dusthave+=dustgetc
        elif card.split(',')[0]=='rare':
            if card not in owned.keys():
                owned[card]=1
                dustneeded-=dustuser
            elif owned[card]==1:
                owned[card]=2
                dustneeded -= dustuser
            else:
                dusthave+=dustgetr
        elif card.split(',')[0]=='epic':
            if card not in owned.keys():
                owned[card]=1
                dustneeded-=dustusee
            elif owned[card]==1:
                owned[card]=2
                dustneeded -= dustusee
            else:
                dusthave+=dustgete
        elif card.split(',')[0]=='lengendary':
            if card not in owned.keys():
                owned[card]=1
                dustneeded-=dustusel
            else:
                dusthave+=dustgetl
total=0
for i in range(10000000):
    total+=packopened
print(total/10000000)
