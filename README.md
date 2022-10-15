# Settlers of Catan Simulator

## How to run
Make sure to install the relevant dependencies using
```
pip3 install -r ./requirements.txt
```

Run the program
```
python3 main.py
```

## Todo List (probably incomplete and in no particular order)
* Player class
* Resource cards
* Water tiles (maybe version 2)
* Main game loop
* Tile connection
* Cities and settlements

## Notes
### Generating the board
The board is modeled as a hexagonal graph where each board space is a node and edges represent roads. This is done by first generating the individual board tiles. Each tile starts as a hexagonal subgraph with 6 nodes. Tiles are connected by merging four nodes together, two from each tile, effectively closing a "side" of each tile.