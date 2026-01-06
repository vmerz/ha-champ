# CHAMP Installation Guide

Complete installation instructions for Home Assistant users.

---

## Installation Steps

### Step 1: Copy Files

1. **Download/clone** the repository or get the component files

2. **Copy to Home Assistant**
   ```bash
   cp -r custom_components/champ /config/custom_components/
   ```

3. **Verify structure**
   ```
   /config/custom_components/champ/
   ├── __init__.py
   ├── manifest.json
   ├── config_flow.py
   ├── coordinator.py
   ├── sensor.py
   ├── switch.py
   └── translations/
       ├── en.json
       └── de.json
   ```

### Step 2: Restart Home Assistant

**Settings** → **System** → **Restart**

Wait for Home Assistant to come back online.

### Step 3: Add Integration

1. **Settings** → **Devices & Services**
2. Click **+ Add Integration** (bottom right)
3. Search for **"CHAMP"**
4. Click **CHAMP - Chores And Motivation Package**

### Step 4: Setup Wizard

Follow the prompts:

#### Add members
- Enter member's name
- Optionally add birthdate
- Choose icon (default: `mdi:account-member`)
- Click **Submit**
- Add more members or click **Done**

#### Add Tasks
- Task name (e.g., "Empty Dishwasher")
- Point value (e.g., 5)
- Icon (e.g., `mdi:dishwasher`)
- Category (chores, learning, health, other)
- Click **Submit**
- Add more tasks or click **Done**

#### Configure Levels
- Points per level (default: 50)
- Click **Submit**

### Step 5: Complete!

CHAMP creates entities for each member:
- `sensor.champ_{member}_points`
- `sensor.champ_{member}_level`
- `sensor.champ_{member}_points_to_next_level`
- `switch.champ_{member}_{task}` (for each task)

---

## Using CHAMP

### Completing Tasks

**Method 1: Via Dashboard**
1. Add switch to dashboard
2. Toggle switch ON when task complete
3. Points awarded automatically
4. Switch turns OFF after 2 seconds

**Method 2: Via Devices & Services**
1. **Settings** → **Devices & Services** → **CHAMP**
2. Click on member's device
3. Toggle task switches

### Viewing Progress

Add sensors to your dashboard:

```yaml
type: entities
title: John's Progress
entities:
  - sensor.champ_john_points
  - sensor.champ_john_level
  - sensor.champ_john_points_to_next_level
```

---

## Troubleshooting

### Integration Not Found

**Problem**: CHAMP doesn't appear in integration search

**Solutions**:
1. Verify files are in `/config/custom_components/champ/`
2. Check file permissions (readable by HA)
3. Restart Home Assistant again
4. Clear browser cache and reload page
5. Check logs: **Settings** → **System** → **Logs**

**Check logs for errors:**
```
Settings → System → Logs → Filter: "champ"
```

### Setup Wizard Fails

**Problem**: Error during configuration

**Solutions**:
1. Ensure member name is not empty
2. Ensure task name is not empty
3. Verify point values are positive numbers
4. Check Home Assistant logs for details
5. Try with simple names (avoid special characters)

### Entities Not Created

**Problem**: No entities appear after setup

**Solutions**:
1. Go to **Developer Tools** → **States**
2. Filter by "champ"
3. Check if entities exist but are hidden
4. Try reloading integration:
   - **Settings** → **Devices & Services** → **CHAMP** → **⋮** → **Reload**
5. Check coordinator logs for errors

### Points Not Updating

**Problem**: Toggling switch doesn't award points

**Solutions**:
1. Verify switch turns ON then OFF (within 2 seconds)
2. Check notification appears
3. Manually check sensor value in Developer Tools
4. Review Home Assistant logs
5. Reload integration

### No Notifications

**Problem**: No notification when task completed

**Solutions**:
1. Check notification panel (bell icon, top right)
2. Verify browser notification permissions
3. Check Home Assistant notification settings
4. Test with manual notification:
   ```yaml
   service: persistent_notification.create
   data:
     title: Test
     message: Testing notifications
   ```

---

## Enable Debug Logging

Add to `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.champ: debug
```

Then restart Home Assistant and check logs for detailed information.

---

## Updating CHAMP

### Manual Update

1. **Backup** current configuration (optional)
2. **Download** new version
3. **Replace** files in `/config/custom_components/champ/`
4. **Restart** Home Assistant
5. **Reload** integration if needed

### Configuration Preservation

Your configuration (members, tasks, points) is stored in Home Assistant's database and survives updates.

---

## Uninstalling

1. **Settings** → **Devices & Services**
2. Find **CHAMP**
3. Click **⋮** → **Delete**
4. Confirm deletion
5. (Optional) Remove files:
   ```bash
   rm -rf /config/custom_components/champ/
   ```
6. Restart Home Assistant

**Note**: Deleting removes all points and configuration.

---

## Getting Help

### Check Logs First

**Settings** → **System** → **Logs** → Filter: "champ"

### Create Issue

If problems persist, create an issue with:
- Home Assistant version
- CHAMP version
- Steps to reproduce
- Relevant log entries
- Screenshots (if applicable)

**GitHub Issues**: https://github.com/vmerz/ha-champ/issues

---

## Next Steps

- **Create dashboards** for your members
- **Customize notifications** (coming in Phase 2)
- **Set up rewards** (coming in Phase 2)
- **Track progress** over time

---

**Happy gamifying!** 🏆

*For development and contributing, see [CONTRIBUTING.md](../CONTRIBUTING.md)*
