# <Name_of_this_thing>
## Overview
[Guild Wars 2](https://www.guildwars2.com/en/) is an MMORPG developed, distributed, and serviced by [ArenaNet](https://www.arena.net/). It is one of the largest and most active MMORPGs in the western market (aside from World of Warcraft). GW2 demonstrates very polished graphics, strategic combat, and meaningful worldbuilding.

Like most other MMORPGs, there is a Trading Post/Auction system where users can trade items and in-game currency real-time. The system works like trading softwares in real life; users can either put in a buy/sell order, or immediately buy/sell to the best order. For example, if player A has an item he wants to sell, he can either post the item at X golds OR sell it to the buy order with the highest price.

I have been a fan of the game for a long time and traded on the Trading Post for a little while. In order to make the most money in-game, I tried to identify the most profitable items - these usually have a very large margin (`highest buy order - lowest sell order`) and are traded frequently.

<Name_of_this_thing> is a website that connects to the [GW2 REST API](https://account.arena.net/applications) officially hosted by AreaNet to fetch Trading Post data in real-time. The script does very minimal analysis on the data, such as calculating the profit margin, before displaying them on the website. Items are also filtered behind the scene based on quantity traded. Currently, only those that have at least 1,000 buy and sell orders are shown on the website. The functionality for the user to choose the desired quantity will be added soon.

## Installation
It is a small website that runs entirely on Python. If you wish to run this website on your own machine for whatever reason, you may simply download this repository and use `pip` to install all dependencies. However, the executable has only been tested on UNIX environments and it _probably won't work on Windows_.

```bash
$ git clone https://github.com/tylerhslee/gw2tp
$ cd gw2tp/python
$ pip -r requirements.txt
$ ./app.py
```

## Usage
Assuming that the server is running, you can connect to the website by pointing your browser to `localhost:5000`. 5000 is the default port used by Flask.
