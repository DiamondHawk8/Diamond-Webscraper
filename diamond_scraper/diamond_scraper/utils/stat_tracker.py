from enum import Enum


class StatTracker:
    def __init__(self, spider, enable_logging=False, pipline_name=None, logging_rules=None):
        self.spider = spider

        # Determines if the class will handle logging itself
        self.enable_logging = enable_logging
        self.pipline_name = pipline_name
        
        
        DEFAULT_LOGGING_RULES = {
            # Validation
            "FIELD_FAILURE": {"log": False, "level": "warning", "store": False},  # Field validation failure
            "ITEM_FAILURE": {"log": True, "level": "error", "store": True},  # Entire item validation failure
            "FIELD_FLAGGED": {"log": True, "level": "warning", "store": True},  # Field flagged
            "ITEM_DROPPED": {"log": True, "level": "error", "store": True},  # Item dropped

            # Statistics
            "TOTAL_FLAGGED": {"log": True, "level": "info", "store": True},  # Total flagged fields
            "TOTAL_DROPPED": {"log": True, "level": "info", "store": True},  # Total dropped items

            # Data Debugging
            "ITEM_INPUT": {"log": True, "level": "debug", "store": False},  # Raw item input
            "ITEM_OUTPUT": {"log": True, "level": "debug", "store": False},  # Processed item output
            "FLAGGED_ITEMS": {"log": True, "level": "debug", "store": True},  # Track flagged items
            "DROPPED_ITEMS": {"log": Txrue, "level": "debug", "store": True},  # Track dropped items
        }

        THRESHOLD_RULES = {
            # How many fields of an item need to fail validation before the entire item is dropped
            "FAILURE_THRESHOLD": 0,

            # How many fields of an item need to be flagged before the entire item is dropped
            "FLAG_THRESHOLD": 3,

        }


        if self.enable_logging:
            if logging_rules:
                # Validate keys before applying custom rules
                for key in logging_rules:
                    if key not in DEFAULT_LOGGING_RULES:
                        raise KeyError(f"Invalid logging rule: {key}")

                # Merge default rules with custom rules
                self.logging_rules = {**DEFAULT_LOGGING_RULES, **logging_rules}
            else:
                self.logging_rules = DEFAULT_LOGGING_RULES
        else:
            self.logging_rules = None

    # Method for incrementing stat by given amount
    def increment_stat(self, stat_name: str, value: int = 1):
        self.spider.crawler.stats.inc_value("custom/items_flagged", count=value)

    # Method for appending to a given stat
    def append_to_stat(self, stat_name: str, data: dict | list):
        pass

    # Method for getting a stat
    def get_stat(self, stat_name: str, default=None):
        # Assuming this method is being used, the statistics being tracked are most likely user defined

        pass

    # Determines whether an item should be dropped based on failed rules.
    def should_drop_item(self, failed_validations: dict) -> bool:
        # TODO allow for thresholds
        pass

    def log_validation_results(self, failed_validations: dict, logging_rules=None):
        # TODO, allow finer control over logging levels based upon
        pass

    # returns a dict of item components that failed validations
    def validate_item(self, item: dict, rules: dict[str, callable]) -> dict:
        # TODO, allow for universal rules to be defined and rules that apply to specific keys
        pass

    # method for implementing custom logging logic
    def log_event(self, event, message):
        rule = self.logging_rules.get(event, {"enabled": False, "level": "info", "store": False})

        if rule["enabled"]:
            getattr(self.spider.logger, rule["level"])(message)

        if rule["store"]:
            self.spider.crawler.stats.inc_value(f"custom/{event.lower()}")


class StatEnum(Enum):
    """Enum for standardized Scrapy stats tracking."""

    # General item processing stats
    ITEMS_PROCESSED = "custom/items_processed"
    ITEMS_DROPPED = "custom/items_dropped"
    ITEMS_FLAGGED = "custom/items_flagged"

    # Validation stats
    FLAGGED_FIELDS = "custom/flagged_fields"
    DROPPED_FIELDS = "custom/dropped_fields"

    # Placeholder for custom user-defined stats
    CUSTOM = "custom/user_defined"


class LoggingEnum(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    DEBUG = "debug"



