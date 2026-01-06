# Changelog

All notable changes to CHAMP will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned for Phase 2
- Dashboard generation service
- Kid-friendly Lovelace card templates
- Rewards system (spend points)
- Enhanced notifications (TTS, mobile app)
- Visual improvements

### Planned for Phase 3
- Recurring tasks (daily/weekly reset)
- Streak tracking
- Statistics and history views
- Parent approval workflow
- Task scheduling

## [0.2.0] - 2025-01-07

### Breaking Changes
- Renamed "children" to "members" throughout the integration
- Entity IDs changed: `champ_{child}_*` → `champ_{member}_*`
- Changed "age" field to "birthdate" (YYYY-MM-DD date format)
- Existing users must remove and re-add the integration

### Added
- Date selector for member birthdate (optional)
- Automatic age calculation from birthdate
- Icon selector (visual picker) for member and task icons
- Translated category selector for tasks
- Integration icon in Home Assistant UI
- Birthdate validation (no future dates, reasonable range)
- Age display in entity attributes
- Python 3.13 support

### Changed
- Generalized terminology: "children" → "members" (works for all ages)
- Improved UI selectors for better user experience
- Enhanced translations (English and German)
- Updated documentation for terminology changes

### Fixed
- Config flow validation logic
- Test suite with proper pytest fixtures
- CI configuration for Python 3.13
- Import formatting conflicts between Black and isort

### Documentation
- Added CREDITS.md for icon attribution
- Updated README with credits section
- Consolidated documentation structure
- 
## [0.1.0] - 2025-12-28

### Added - Phase 1 Complete ✅
- Initial release of CHAMP integration
- UI-based configuration flow (no YAML needed)
- Multi-step setup wizard for members and tasks
- Support for multiple members (1-8+)
- Dynamic entity creation based on configuration
- Sensor entities:
  - Points tracking per member
  - Level calculation per member
  - Progress to next level per member
- Switch entities for tasks:
  - Auto-award points on toggle
  - Auto-turn off after 2 seconds (visual feedback)
  - Persistent notifications on completion
- Level system (configurable points per level, default: 50)
- Multi-language support:
  - English (en)
  - German (de)
- Data coordinator for efficient state management
- Device grouping (all member entities grouped together)
- Proper entity registry integration
- State persistence across restarts
- Reload support without restart
- Comprehensive documentation:
  - Installation guide
  - Quick reference card
  - Technical documentation
  - PyCharm setup guide
- Development tools:
  - pytest test suite
  - Black code formatting
  - Ruff linting
  - MyPy type checking
  - Pre-commit hooks
  - Validation script

### Technical Details
- Python 3.11+ with full type hints
- Async/await patterns throughout
- Home Assistant 2024.12+ compatible
- DataUpdateCoordinator architecture
- Config flow implementation
- Proper error handling and logging

## [0.0.1] - 2025-12-26

### Initial Development
- Proof of concept YAML package
- Basic point system for 2 members
- 7 task types with fixed point values
- Manual YAML configuration
- Input number and boolean entities
- Home Assistant automations for point awarding

---

## Version Numbering

CHAMP follows [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality (backward compatible)
- **PATCH** version for bug fixes (backward compatible)

Current version: **0.1.0** (Phase 1 - Core Component Complete)

---

## Migration Guides

### From YAML Package to v0.1.0

The new component completely replaces the YAML package. To migrate:

1. **Backup your YAML configuration**
   ```bash
   cp /config/packages/gamified_tasks.yaml /config/gamified_tasks.yaml.backup
   ```

2. **Remove the YAML package**
   ```bash
   rm /config/packages/gamified_tasks.yaml
   ```

3. **Install the custom component**
   ```bash
   cp -r custom_components/champ /config/custom_components/
   ```

4. **Restart Home Assistant**

5. **Add integration via UI**
   - Settings → Devices & Services → Add Integration → CHAMP
   - Follow the setup wizard

6. **Recreate your members and tasks** in the UI wizard

7. **Note:** Entity IDs will change:
   - Old: `input_number.john_points`
   - New: `sensor.champ_john_points`
   
   Update any automations or dashboards that reference the old entities.

---

## Breaking Changes

### v0.1.0
- Complete rewrite from YAML package to custom component
- Entity naming changed from `input_*` to `sensor.*` and `switch.*`
- Manual YAML configuration no longer supported
- All configuration now via UI

---

## Deprecations

None yet.

---

## Security

If you discover a security vulnerability, please email [your-email@example.com].
Do not create a public issue.

---

[Unreleased]: https://github.com/vmerz/ha-champ/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/vmerz/ha-champ/releases/tag/v0.1.0
[0.0.1]: https://github.com/vmerz/ha-champ/releases/tag/v0.0.1
