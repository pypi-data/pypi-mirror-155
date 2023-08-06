# Cell Machine Levels

A library for manipulating modded cell machine level codes.

To install do:

```bash
pip3 install cell_machine_levels
```

Or just `pip` on some OSes

## Level class

Currently supports only V1 and V2, support is going to be added for much more than just these

Level creation example:

```py
from cell_machine_levels import level
test = level.Level(10, 10, "test", level.WallEffect.wrap)
print(test.save("V1"))
```

Level importing example:

```py
from cell_machine_levels import level
test = level.open("V1;10;10;;;test;2")
print(f"{test.name}: {test.size}, {test.wall_effect}")
```
