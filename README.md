# Title: Trade-off of Three Pack-opening Strategies in Hearthstone —— Using Monte Carlo Simulation


## Team Member(s): Jianzhang Chen, Xiaokai Cui, Yichong Guo


# Monte Carlo Simulation Scenario & Purpose:
There are four rules for opening packs in Hearthstone:
1. Each pack contains 5 cards.
2. There are maximum numbers for each type of cards: 2 Common, 2 Rare, 2 Epic and 1 Legendary.
3. Cards can be disenchanted into dust.
4. Dust can be used to craft any certain card.

Now Blizzard has three strategies to decrease the number of packs to get all the cards of a certain expansion card set:
1. Every time you open a Legendary in a card pack, it will be a Legendary card from the same set that you don’t already own.
2. You can exchange a certain number of dust for a new pack but you cannot craft cards with dust. 
3. You can obtain a pack containing only Epic and Legendary cards after you have opened a certain number of packs. 

Blizzard decides to take the first strategy. We want to find out the certain parameters of the second and the third strategies so that they can expect a same number of packs we need to open to get all the cards on average.


## Simulation's variables of uncertainty
We decide to use the expansion card set ‘Knights of the Frozen Throne’. It has 49 Common cards, 36 Rare cards, 27 Epic cards and 23 Legendary cards. Our simulation's variables of uncertainty are the probabilities of opening each type of card when we open a pack. The probabilities of getting a card of Common, Rare, Epic, Legendary, Golden Common, Golden Rare, Golden Epic and Golden Legendary are 70.16%, 21.74%, 3.95%, 0.84%, 1.47%, 1.47%, 0.26% and 0.11%. We think the outcome of running 5,000 times of simulations (we decide this number by running different times and observe when the lines converge) is a good representation of reality.


## Hypothesis or hypotheses before running the simulation:
We run the simulations for the first strategy and get an expectation of 317 packs, which means that after Blizzard used the first strategy, we need to open 317 packs on average in order to collect all the cards of the expansion card set ‘Knights of the Frozen Throne’.

## Analytical Summary of your findings: (e.g. Did you adjust the scenario based on previous simulation outcomes?  What are the management decisions one could make from your simulation's output, etc.)
We run simulations and calculate the two 'certain number's in the second and the third strategies by using the result of runing the first simulation. These two numbers are 125 and 115. In other words, if Blizzard used the other two strategies to decrease the number of packs to get all the cards of a certain expansion card set and wanted to get a same expectation of packs opened as using the first strategy now, it can use either the strategy of 'Players can exchange 125 dust for a new pack but they cannot craft cards with dust.' or the strategy of 'Players can obtain an pack containing only Epic and Legendary cards after they have opened 115 packs.'

## Instructions on how to use the program:
Run 'Main.py' file and it will call the class in written in 'HearthStone.py' file.


## All Sources Used:
* Programming language: Python 3  

1. The official website of HearthStone (https://hearthstone.gamepedia.com/Hearthstone_Wiki) to get the probabilities of getting different types of card.  
2. The Wikipidia of HearthStone (https://en.wikipedia.org/wiki/Hearthstone) for every expansion's collectible cards breakdown.

