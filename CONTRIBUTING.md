# Contributing to CHAMP

Thanks for your interest in contributing! This guide will help you get set up for development.

---

## Quick Start (5 Minutes)

```bash
# 1. Clone the repository
git clone https://github.com/vmerz/ha-champ.git
cd ha-champ-project

# 2. Run setup
./setup.sh

# 3. Activate environment
source venv/bin/activate

# 4. Verify setup
make test

# ✅ Ready to develop!
```

---

## Prerequisites

- **Python 3.12** (Python 3.11 also supported)
- **Git**
- **PyCharm Professional** (recommended) or any Python IDE
- **Home Assistant** instance for testing (optional)

---

## Development Setup

### 1. Environment Setup

The `setup.sh` script does everything:

```bash
./setup.sh
```

**What it does:**
- Creates virtual environment (`venv/`)
- Installs all dependencies
- Sets up pre-commit hooks

### 2. PyCharm Configuration (Recommended)

#### Open Project
1. **File** → **Open** → Select `ha-champ-project` folder

#### Set Interpreter
1. **Settings** → **Project** → **Python Interpreter**
2. Click ⚙️ → **Add Interpreter** → **Existing**
3. Select: `venv/bin/python`
4. Click **OK**

#### Configure Test Runner
1. **Settings** → **Tools** → **Python Integrated Tools**
2. Set **Default test runner** to `pytest`

#### Mark Directories
1. **File** → **Project Structure**
2. Mark `custom_components` as **Sources**
3. Mark `tests` as **Tests**

**That's it!** PyCharm is configured.

### 3. Verify Setup

```bash
# Run validation
make validate

# Run tests
make test

# Run all checks
make all
```

All checks should pass ✅

---

## Development Workflow

### Daily Workflow

1. **Activate environment** (automatic in PyCharm)
   ```bash
   source venv/bin/activate
   ```

2. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature
   ```

3. **Make changes** to code

4. **Run tests** as you develop
   ```bash
   make test
   ```

5. **Before committing**
   ```bash
   make all  # Runs format, lint, type-check, test
   ```

6. **Commit** (pre-commit hooks run automatically)
   ```bash
   git add .
   git commit -m "Add amazing feature"
   ```

7. **Push and create PR**
   ```bash
   git push origin feature/your-feature
   ```

### Development Commands

| Command | What It Does |
|---------|--------------|
| `make test` | Run pytest with coverage |
| `make format` | Auto-format with Black & isort |
| `make lint` | Check code quality with Ruff |
| `make type-check` | Type check with MyPy |
| `make validate` | Validate component structure |
| `make all` | Run all checks (use before commit) |
| `make clean` | Remove build artifacts |
| `make help` | Show all commands |

---

## Testing Your Changes

### Unit Tests

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_init.py

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=custom_components/champ --cov-report=html
```

### Testing in Home Assistant

#### Option 1: Copy to HA Instance
```bash
# Copy component
cp -r custom_components/champ /config/custom_components/

# Restart Home Assistant
# Or reload: Settings → Devices & Services → CHAMP → ⋮ → Reload
```

#### Option 2: Development Instance
```bash
# Set up separate HA dev instance
cd ~/homeassistant-dev
python3.12 -m venv venv
source venv/bin/activate
pip install homeassistant

# Link your component
ln -s ~/path/to/ha-champ-project/custom_components/champ \
      ~/homeassistant-dev/config/custom_components/champ

# Run HA
hass -c ~/homeassistant-dev/config
```

### Debugging in PyCharm

1. Create debug configuration:
   - **Run** → **Edit Configurations**
   - **Script path**: `/path/to/homeassistant-dev/venv/bin/hass`
   - **Parameters**: `-c /path/to/homeassistant-dev/config`

2. Set breakpoints in code

3. Click **Debug** button

4. HA starts and pauses at breakpoints! 🎯

---

## Code Standards

### Style Guide

- **Line length**: 88 characters (Black default)
- **Imports**: Sorted with isort
- **Type hints**: Required on all functions
- **Docstrings**: Google style for public APIs
- **Naming**: snake_case for functions/variables

### Before Committing

**Always run:**
```bash
make all
```

This ensures:
- ✅ Code is formatted (Black, isort)
- ✅ No linting errors (Ruff)
- ✅ Type hints are correct (MyPy)
- ✅ All tests pass (pytest)

### Pre-commit Hooks

Hooks run automatically on `git commit`:
- Black formatting
- Ruff linting
- Trailing whitespace removal
- YAML validation

**If hooks fail:**
```bash
# Fix issues
make format

# Try commit again
git commit -m "Your message"
```

---

## Pull Request Process

### 1. Create Feature Branch
```bash
git checkout -b feature/amazing-feature
```

### 2. Make Changes
- Write code
- Add tests
- Update docs if needed

### 3. Test Locally
```bash
make all  # Must pass!
```

### 4. Commit
```bash
git add .
git commit -m "Add amazing feature"
```

### 5. Push
```bash
git push origin feature/amazing-feature
```

### 6. Create Pull Request

On GitHub:
1. Click **Pull Request**
2. Fill out the template
3. Wait for CI checks to pass
4. Request review

### PR Checklist

- [ ] Code follows style guide
- [ ] All tests pass (`make all`)
- [ ] New features have tests
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] PR description is clear

---

## CI/CD

### GitHub Actions

Every push and PR triggers:
- ✅ **Validation** - Component structure check
- ✅ **Linting** - Black, isort, Ruff
- ✅ **Type Check** - MyPy
- ✅ **Tests** - pytest on Python 3.11 & 3.12
- ✅ **Hassfest** - Home Assistant validation
- ✅ **HACS** - HACS compatibility

**All checks must pass** before merging.

### Dependabot

Automatically:
- Checks for dependency updates weekly
- Creates PRs for updates
- Runs CI on update PRs

---

## Project Structure

```
ha-champ-project/
├── custom_components/champ/   # Integration code
│   ├── __init__.py            # Component setup
│   ├── manifest.json          # Metadata
│   ├── config_flow.py         # UI wizard
│   ├── const.py              # Constants
│   ├── coordinator.py        # Data management
│   ├── sensor.py             # Point/level sensors
│   ├── switch.py             # Task switches
│   └── translations/         # i18n
├── tests/                    # Test suite
│   ├── conftest.py          # Test fixtures
│   └── test_init.py         # Tests
├── docs/                    # Documentation
├── .github/                 # CI/CD workflows
├── pyproject.toml          # Project config
├── requirements-dev.txt    # Dev dependencies
├── Makefile               # Dev commands
└── setup.sh              # Setup script
```

### Key Files

| File | Purpose |
|------|---------|
| `__init__.py` | Component entry point |
| `config_flow.py` | Setup wizard UI |
| `coordinator.py` | Data & state management |
| `sensor.py` | Points/level sensors |
| `switch.py` | Task switches (point awarding) |
| `const.py` | Constants & defaults |

---

## Adding New Features

### Example: Add New Sensor

1. **Update `sensor.py`**
   ```python
   class NewSensor(ChampSensor):
       """New sensor implementation."""
       
       @property
       def native_value(self):
           return self.coordinator.get_value()
   ```

2. **Add tests in `tests/test_sensor.py`**
   ```python
   async def test_new_sensor(hass, setup_integration):
       """Test new sensor."""
       state = hass.states.get("sensor.champ_child_new")
       assert state is not None
   ```

3. **Update translations**
   - Add to `translations/en.json`
   - Add to `translations/de.json`

4. **Test**
   ```bash
   make all
   ```

5. **Commit**
   ```bash
   git commit -m "Add new sensor for XYZ"
   ```

---

## Common Issues

### "Module not found" errors
```bash
pip install -r requirements-dev.txt
```

### Tests fail locally but pass on GitHub
```bash
# Test with both Python versions
python3.11 -m pytest
python3.12 -m pytest
```

### Pre-commit hooks fail
```bash
# Auto-fix most issues
make format

# Try commit again
git commit -m "Your message"
```

### Type checking errors
```bash
# Check specific file
mypy custom_components/champ/sensor.py

# Add type ignore if needed
result: Any = function()  # type: ignore[annotation-issue]
```

---

## Getting Help

- **Questions**: Create a [Discussion](https://github.com/vmerz/ha-champ/discussions)
- **Bugs**: Create an [Issue](https://github.com/vmerz/ha-champ/issues)
- **Documentation**: Check `docs/` folder
- **Quick Reference**: See [docs/QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md)

---

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards others

---

## Recognition

Contributors are:
- Listed in release notes
- Credited in CHANGELOG.md
- Acknowledged in README.md

---

**Thank you for contributing to CHAMP!** 🏆

*Let's make household chores fun for families everywhere!*
