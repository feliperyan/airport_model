# Kafka Foot Traffic Simulator 
Useful for visually demonstrating events streaming into Kafka.

### Description

The map on the screen represents an airport. On a pre-determined timeframe a group of passengers enters the airport at a random "Gate".

Each passenger has a destination, one of the transports options at the bottom or other exit points. Every sencond the simulation "scans" the airport and updates the location of the passengers. 

Sometimes passengers can get stuck, you'll see this reflected by the colour of the passenger changing to red. The passenger will then try to find a new path to her destination (by re-running the pathfinding algorithm)

### Usage

Clicking the start button will start the simulation in "simple" mode and you won't get many events in Kafka, around 1 a second.  Flood will however emit an event per passenger; with the example included it ends being around 100/sec after a few minutes.  This can be useful when you show or build Kafka Consumers down the track.

### Code and Caveats

This demo retains state in the dyno (not 12 factor) meaning it will **not** scale to more than one dyno.

The map on the screen is a png/jpg/etc however it contains a **textual** representation that governs the simulation; the one used by default is **sydney_airport.txt**. 

Behind the scenes the [A-Star algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm) is used for pathfinding. There are Classes for the 2d Grid itself and the elements on it, see the Grid folder for the code.

This is how you can build your own versions of the simulation, it's not a pretty process and involves a lot of manual work atm. Btw passengers move only in 4 directions. 


### Definition for characters textual map:
1. "." = walkable floor
2. "#" = impassable wall
3. "*" = exit (each passenger will randomly set her destination to one of these randomly)
4. "?" = TODO: a tile that lets me define where passengers will "materialise".





