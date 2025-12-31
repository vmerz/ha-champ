# CHAMP Quick Reference Card

## Installation
```bash
# Copy to Home Assistant
cp -r custom_components/champ /config/custom_components/
# Restart Home Assistant
# Add via UI: Settings → Devices & Services → Add Integration → CHAMP
```

## Entity Naming Pattern

### Sensors (per child)
```
sensor.champ_{child_id}_points               # Current points
sensor.champ_{child_id}_level                # Current level  
sensor.champ_{child_id}_points_to_next_level # Progress
```

### Switches (per child per task)
```
switch.champ_{child_id}_{task_id}            # Task switch
```

## Configuration Flow Steps

1. **User** - Welcome screen
2. **Add Child** - Name, age, icon
3. **Add Another Child?** - Yes/No
4. **Add Task** - Name, points, icon, category
5. **Add Another Task?** - Yes/No
6. **Level Config** - Points per level (default: 50)
7. **Finish** - Creates integration

## Example Entities

Child: "John", Task: "Dishwasher" (5 points)

```
sensor.champ_john_points                     # 0 → 5 → 10...
sensor.champ_john_level                      # 0 → 1 (at 50 pts)
sensor.champ_john_points_to_next_level       # 50 → 45 → 40...
switch.champ_john_dishwasher                 # Toggle to award 5 pts
```

## Task Completion Flow

1. User toggles `switch.champ_{child}_{task}` **ON**
2. Switch turns **ON**
3. Points awarded to child
4. Notification sent: "🎉 {Child} hat {points} Punkte verdient!"
5. Switch auto turns **OFF** after 2 seconds
6. Sensors update

## Key Files

```
custom_components/champ/
├── __init__.py          # Setup entry point
├── manifest.json        # Integration metadata
├── config_flow.py       # UI wizard
├── const.py            # Constants
├── coordinator.py      # Data management
├── sensor.py           # Point/level sensors
├── switch.py           # Task switches
└── translations/
    ├── en.json         # English
    └── de.json         # German
```

## Debugging

```yaml
# configuration.yaml
logger:
  logs:
    custom_components.champ: debug
```

```bash
# View logs
tail -f /config/home-assistant.log | grep champ
```

## Common Operations

### Reload Integration
Settings → Devices & Services → CHAMP → ⋮ → Reload

### Remove Integration
Settings → Devices & Services → CHAMP → ⋮ → Delete

### View All Entities
Developer Tools → States → Filter: "champ"

### Manual Point Award (via coordinator)
```python
await coordinator.award_points(child_id, points)
```

### Reset Points (via coordinator)
```python
await coordinator.reset_points(child_id)
```

## Default Values

```python
DEFAULT_POINTS_PER_LEVEL = 50
DEFAULT_TASK_ICON = "mdi:checkbox-marked-circle"
DEFAULT_CHILD_ICON = "mdi:account-child"
UPDATE_INTERVAL = 30  # seconds
```

## Task Categories

- `chores` - Household tasks
- `learning` - Educational activities
- `health` - Exercise, eating well
- `other` - Everything else

## Level Calculation

```python
level = points // points_per_level
points_to_next = points_per_level - (points % points_per_level)
```

Example: 50 points per level
- 0-49 points = Level 0
- 50-99 points = Level 1
- 100-149 points = Level 2

## Notifications

Format:
```
Title: 🎉 Punkte verdient!
Message: {Child} hat {points} Punkte für {task} verdient! 
         Gesamt: {total_points} Punkte (Level {level})
```

## YAML Dashboard Example

```yaml
type: entities
title: John's Progress
entities:
  - sensor.champ_john_points
  - sensor.champ_john_level
  - sensor.champ_john_points_to_next_level
  - switch.champ_john_dishwasher
  - switch.champ_john_table
```

## Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| Integration not found | Check files in `/config/custom_components/champ` |
| Setup fails | Check HA logs, verify names not empty |
| Entities not created | Reload integration or check coordinator |
| Points not updating | Check switch ON→OFF cycle works |
| No notification | Verify `persistent_notification` service |

## Version Info

**Current Version:** 0.1.0 (Phase 1)  
**Home Assistant:** 2024.12+  
**Python:** 3.11+  

---

**Keep this card handy during development and testing!**
