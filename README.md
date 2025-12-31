# CHAMP - Chores And Motivation Package
## Home Assistant Custom Component

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/vmerz/ha-champ)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)]()
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2024.12+-blue.svg)]()

**Turn chores into achievements, make every kid a CHAMP!** 🏆

---

## What is CHAMP?

CHAMP gamifies household chores and learning tasks for children through Home Assistant. Kids earn points for completing tasks, level up, and parents get an overview of all progress.

### Features

✅ **Points & Levels** - Earn points, gain levels  
✅ **Multiple Children** - Support for 1-8+ kids  
✅ **Custom Tasks** - Any task, any point value  
✅ **UI Configuration** - No YAML needed  
✅ **Auto Notifications** - Celebrate achievements  
✅ **Multi-Language** - English & German  

---

## Quick Start

### For Users (Installation)

```bash
# 1. Copy component to Home Assistant
cp -r custom_components/champ /config/custom_components/

# 2. Restart Home Assistant
# 3. Add via UI: Settings → Devices & Services → CHAMP
```

📚 **Full installation guide**: [docs/INSTALL.md](docs/INSTALL.md)

### For Developers (Contributing)

```bash
# 1. Setup
./setup.sh

# 2. Test
make test

# 3. Develop!
```

📚 **Contributing guide**: [CONTRIBUTING.md](CONTRIBUTING.md)

---

## How It Works

### 1. Setup (via UI)
```
Settings → Devices & Services → Add Integration → CHAMP
  → Add child: "John"
  → Add task: "Empty Dishwasher" (5 points)
  → Set levels: 50 points = 1 level
```

### 2. Entities Created
```
sensor.champ_john_points                # Current points
sensor.champ_john_level                 # Current level  
sensor.champ_john_points_to_next_level  # Progress
switch.champ_john_dishwasher            # Task toggle
```

### 3. Complete Tasks
```
Toggle switch ON → Points awarded → Notification → Switch auto OFF
```

---

## Development Commands

| Command | Description |
|---------|-------------|
| `./setup.sh` | Initial environment setup |
| `make test` | Run tests with coverage |
| `make format` | Format code (Black, isort) |
| `make lint` | Lint code (Ruff) |
| `make type-check` | Type check (MyPy) |
| `make all` | Run all checks |
| `make validate` | Validate component structure |

---

## Documentation

| Document | Purpose |
|----------|---------|
| [CONTRIBUTING.md](CONTRIBUTING.md) | Development setup & workflow |
| [docs/INSTALL.md](docs/INSTALL.md) | User installation guide |
| [docs/QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md) | Developer cheat sheet |
| [CHANGELOG.md](CHANGELOG.md) | Version history |

---

## Project Structure

```
ha-champ-project/
├── custom_components/champ/   # The integration
│   ├── __init__.py            # Setup
│   ├── config_flow.py         # UI wizard
│   ├── sensor.py              # Points/level sensors
│   └── switch.py              # Task switches
├── tests/                     # Test suite
├── docs/                      # Documentation
└── Makefile                   # Common commands
```

---

## Technology Stack

- **Python 3.11+** with type hints
- **Home Assistant 2024.12+**
- **pytest** for testing
- **Black, Ruff, MyPy** for code quality

---

## Development Status

**Current:** v0.1.0 - Phase 1 Complete ✅

### Phase 1 ✅
- Config flow UI
- Points & level system
- Multi-child support
- Task switches
- Notifications

### Phase 2 🚧
- Dashboard generation
- Rewards system
- Kid-friendly cards

### Phase 3 📅
- Recurring tasks
- Streak tracking
- Statistics

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup
- Code standards
- Pull request process

---

## Support

- **Issues**: [GitHub Issues](https://github.com/vmerz/ha-champ/issues)
- **Docs**: See `docs/` folder
- **Community**: [Home Assistant Forum](https://community.home-assistant.io/)

---

## License

MIT License - see [LICENSE](LICENSE)

---

**🏆 CHAMP - Because every kid deserves to feel like a champion!**

*Project Status: Phase 1 Complete - Ready for Development & Testing*
