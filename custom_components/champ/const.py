"""Constants for the CHAMP integration."""

# Domain
DOMAIN = "champ"

# Configuration and options
CONF_TASKS = "tasks"
CONF_LEVEL_CONFIG = "level_config"
CONF_REWARDS = "rewards"

# Member configuration
CONF_MEMBERS = "members"
CONF_MEMBER_NAME = "member_name"
CONF_MEMBER_ID = "member_id"
CONF_MEMBER_BIRTHDATE = "member_birthdate"
CONF_MEMBER_ICON = "member_icon"

# Task configuration
CONF_TASK_ID = "id"
CONF_TASK_NAME = "name"
CONF_TASK_ICON = "icon"
CONF_TASK_POINTS = "points"
CONF_TASK_CATEGORY = "category"
CONF_TASK_ASSIGNED_TO = "assigned_to"

# Level configuration
CONF_POINTS_PER_LEVEL = "points_per_level"
CONF_MAX_LEVEL = "max_level"

# Reward configuration
CONF_REWARD_ID = "id"
CONF_REWARD_DESCRIPTION = "description"
CONF_REWARD_COST = "cost"
CONF_REWARD_APPROVAL_REQUIRED = "approval_required"

# Defaults
DEFAULT_POINTS_PER_LEVEL = 50
DEFAULT_TASK_ICON = "mdi:checkbox-marked-circle"
DEFAULT_MEMBER_ICON = "mdi:account-member"

# Task categories
TASK_CATEGORY_CHORES = "chores"
TASK_CATEGORY_LEARNING = "learning"
TASK_CATEGORY_HEALTH = "health"
TASK_CATEGORY_OTHER = "other"

TASK_CATEGORIES = [
    TASK_CATEGORY_CHORES,
    TASK_CATEGORY_LEARNING,
    TASK_CATEGORY_HEALTH,
    TASK_CATEGORY_OTHER,
]

# Services
SERVICE_AWARD_POINTS = "award_points"
SERVICE_RESET_POINTS = "reset_points"
SERVICE_COMPLETE_TASK = "complete_task"
SERVICE_GENERATE_DASHBOARD = "generate_dashboard"

# Attributes
ATTR_MEMBER_ID = "member_id"
ATTR_POINTS = "points"
ATTR_TASK_ID = "task_id"
ATTR_DASHBOARD_TYPE = "dashboard_type"

# Entity ID formats
SENSOR_POINTS = "{domain}_{member_id}_points"
SENSOR_LEVEL = "{domain}_{member_id}_level"
SENSOR_POINTS_TO_NEXT = "{domain}_{member_id}_points_to_next_level"
SWITCH_TASK = "{domain}_{member_id}_{task_id}"

# Update interval (in seconds)
UPDATE_INTERVAL = 30
