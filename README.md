# tcheckerpy

**tcheckerpy** is a Python interface to the [TChecker](https://github.com/Echtzeitsysteme/tchecker/) model checker, allowing you to analyze and compare timed automata models directly from Python.  
It provides access to the following TChecker tools:

- tck-compare
- tck-liveness
- tck-reach
- tck-simulate
- tck-syntax

For detailed documentation, refer to the [TChecker Wiki](https://github.com/ticktac-project/tchecker/wiki/Using-TChecker).

## Installation

You can install `tcheckerpy` via PyPI:

```bash
pip install tcheckerpy
```

## Usage

To use any of the supported tools, import the corresponding router and call the associated function.
Each function expects the system declaration of your timed automata network(s) as a string input.
You may also provide additional arguments by creating a parameter object specific to the selected tool.
Return values are in the form of either a string, a dict of strings, or a Response object.  
Most tools (except tck-syntax) require the use of Python's asyncio to run the functions asynchronously.

## Example

```python

# import required routers
from tcheckerpy.routers import tck_reach, tck_syntax
import asyncio

# read declaration of timed automata network from .txt or .tck file into string
with open(system_declaration_path) as file:
        system = file.read()

# check syntax
syntax_check = tck_syntax.check(system)["status"] == "success" # convert to bool

# define reachability analysis parameters
reach_body = tck_reach.TckReachBody(
    sysdecl=system, 
    labels="", 
    algorithm=0,
    search_order="bfs",
    certificate=0
)

# perform reachability analysis if syntax is valid
if(syntax_check):
    reachability_result = asyncio.run(tck_reach.reach(reach_body))
    print(reachability_result["stats"])
    print(reachability_result["certificate"])

```

Example output (based on [ad94.txt](https://github.com/Echtzeitsysteme/tchecker/blob/master/examples/ad94.txt)):

```
MEMORY_MAX_RSS 41116
REACHABLE false
RUNNING_TIME_SECONDS 6.1474e-05
VISITED_STATES 7
VISITED_TRANSITIONS 8

digraph ad94_fig10 {
  0 [initial="true", intval="", labels="", vloc="<l0>", zone="(0<=x && 0<=y)"]
  1 [intval="", labels="", vloc="<l1>", zone="(1<x && 0<=y && 1<x-y)"]
  2 [intval="", labels="", vloc="<l1>", zone="(0<=x && 0<=y && 0<=x-y)"]
  3 [intval="", labels="", vloc="<l2>", zone="(1<x && 1<=y)"]
  4 [intval="", labels="", vloc="<l2>", zone="(1<=x && 1<=y)"]
  5 [intval="", labels="green", vloc="<l3>", zone="(1<x && 0<y && x-y<1)"]
  6 [intval="", labels="green", vloc="<l3>", zone="(0<=x && 0<=y && x-y<1)"]
  0 -> 2 [vedge="<P@a>"]
  1 -> 3 [vedge="<P@b>"]
  2 -> 4 [vedge="<P@b>"]
  2 -> 6 [vedge="<P@c>"]
  5 -> 1 [vedge="<P@a>"]
  5 -> 5 [vedge="<P@d>"]
  6 -> 2 [vedge="<P@a>"]
  6 -> 5 [vedge="<P@d>"]
}

```
