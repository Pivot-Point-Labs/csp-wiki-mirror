# Node Adjustments

Could be used to activate or deactivate nodes (think of them as parents to meshes and other nodes) or move them somewhere else. For example, one good use is to move to COCKPIT_HR some interior mesh which was accidentally left “outside”.

### Syntax

```ini
[NODE_ADJUSTMENT_...]
NODES = list, of, nodes, and?or, f?lters
MOVE_TO = node_to_move_to  ; optional, could be filter or several entries
                           ; if several were found, first one will be used
IS_ACTIVE = 1              ; optional, switches whole node on and off
```
