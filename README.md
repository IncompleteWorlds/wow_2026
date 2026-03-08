# Introduction

# Installation

Create a new virtual Python environment
```sh
$ python3 -m venv env
```

Activate the new environment:
```sh
$ source env/bin/activate
```

Install the *pygame* library
```sh
$ pip install pygame
Collecting pygame
  Downloading pygame-2.6.1-cp312-cp312-macosx_11_0_arm64.whl.metadata (12 kB)
Downloading pygame-2.6.1-cp312-cp312-macosx_11_0_arm64.whl (12.4 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 12.4/12.4 MB 35.5 MB/s eta 0:00:00
Installing collected packages: pygame
Successfully installed pygame-2.6.1

[notice] A new release of pip is available: 24.0 -> 26.0.1
[notice] To update, run: pip install --upgrade pip
```

# Notes

Room data are defined in a JSON file, located in 'assets/rooms/'
A room is composed of exits and a graph. A graph includes a list of nodes and
a list of edges.

Map is defined in the 'assets/map_data.json' file
It contains among other things a graph; list of nodes and edges 

Some debug info:
- In a room; press 'g' to show the graph
             press 'd' for showing some debug info

- In the map; press 'g' to show the graph
              press 'd' for showing some debug info
