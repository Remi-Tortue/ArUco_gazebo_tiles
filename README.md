# ArUco_gazebo_tiles
Generate gazebo models of aruco markers + aruco detection
![Example ArUco Marker Tile](doc/screenshot_gazebo_tile_7x7_0_0_1.png)

## Install

```bash
cd ArUco_gazebo_tiles
pip install -e .
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:$(pwd)/models # If you’re using Gazebo Classic
export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:$(pwd)/models # If you’re using Ignition / Gazebo Sim (Fortress, Garden, Harmonic)
```

## How it works

Generate the tile model :
```bash
python3 generate_gazebo_tiles.py <DICT> <ID> <SIZE_IN_M>
# python3 generate_gazebo_tiles.py 7x7 0 0.1
```

Visualize the marker tile via :
```bash
gazebo
# or
gz
```
Then insert the marker model.



## Overview


## ToDo / new features
- aruco marker detection python lib.
- Ros2 node publisher or service to get the aruco marker transform.

## Contributors
- **Rémi Porée**