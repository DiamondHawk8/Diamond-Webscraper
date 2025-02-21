from enum import Enum


class StatTracker:
    def __init__(self, spider, enable_logging=False, pipline_name=None, logging_rules=None):
        self.spider = spider

        # Determines if the class will handle logging itself
        self.enable_logging = enable_logging
        self.pipline_name = pipline_name

        default_logging_rules = {}
        if logging_rules:
            # TODO allow for partially filled provided rules that are substituted with default where blank
            self.logging_rules = logging_rules

    # Method for incrementing stat by given amount
    def increment_stat(self, stat_name: str, value: int = 1):
        pass

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
