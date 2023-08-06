# Cell Machine Levels

A library for manipulating modded cell machine level codes.

To install do:

```bash
pip3 install cell_machine_levels
```

Or just `pip` on some OSes

## Level class

Currently supports the main 3 types (V1, V2, V3), support is going to be added for more than just these

Level creation example:

```py
from cell_machine_levels import level
test = level.Level(10, 10, "test", level.WallEffect.wrap)
print(test.save("V3"))
```

Level importing example:

```py
from cell_machine_levels import level
test = level.open("V3;a;a;;;test;2")
print(f"{test.name}: {test.size}, {test.wall_effect}")
```
