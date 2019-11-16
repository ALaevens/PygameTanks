# Pygame Tanks

A simple top down tank game

## Running:
1. First Make sure these prerequisites are installed
    * Python3
    * Pygame
2. Run main.py

This is an old unfinished project so there are no graphics settings for different screen sizes.
The game starts in 1280x720 resolution.

## Using the level creator:
Level files can be created and modified using the level creator.
* When started a tk window will prompt for a size and New or Load buttons
    * The size only matters for 'New'
    * The game loads the levels sequentially from the folder so it's easiest to just name them by number
* The slider in the top left indicates the 'layer'
* The fill button will fill an entire layer with the selected material (mostly useful for filling grass or dirt)
* The save button will save the file, I just never implemented a message

The game currently includes 11 tiles:
* Grass, Dirt, Bridges, and Gravel Paths (and variants)
    * Tanks and Bullets can pass over
* Walls (and variants), Crates
    * Nothing can pass over
* Water (and variants)
    * bullets can pass over

*Blocks are deleted with the regular red warning icon*   
*Blocks that can be rotated (paths, water, bridges, walls) can be done so with right click*

Spawnpoints can be set with the flag icons. They aren't bound to a layer and aren't visible in game.  
At the current state only the 1 and 2 players are supported.

*Spawnpoints are deleted with the special meta-data eraser (red warning icon with M inside)*


The level creator is names levelCreatorGUI.py
### Screenshots:
![Title](https://imgur.com/HvsdWnZ.png)
![Driving](https://i.imgur.com/rqdIvh4.png)
![Combat](https://i.imgur.com/IPUxBRM.png)
![Level Editor](https://i.imgur.com/jHlsKBS.png)