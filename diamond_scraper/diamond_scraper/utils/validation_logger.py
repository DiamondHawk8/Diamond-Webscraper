from enum import Enum
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class ValidationLogger:
    def __init__(self, spider, enable_logging=False, pipline_name=None, logging_rules=None, default_rules=None):
        self.spider = spider

        # Determines if the class will handle logging itself
        self.enable_logging = enable_logging
        self.pipline_name = pipline_name


        # Would it be better to enable the default rules automatically, or have that be something users opt into?
        # I can see situations where it would be annoying to have to turn of my custom rules every time
        # TODO create default rules
        DEFAULT_RULES = {

        }
        if not default_rules:
            self.default_rules = DEFAULT_RULES

        # Default rules for logging behavior (log level and storage settings)
        DEFAULT_LOGGING_RULES = {
            # Validation Events
            "FIELD_FAILURE": {"log": False, "level": "warning", "store": False},  # A field fails validation
            "ITEM_FAILURE": {"log": True, "level": "error", "store": True},  # An entire item fails validation
            "FIELD_FLAGGED": {"log": True, "level": "warning", "store": True},  # A field is flagged
            "ITEM_DROPPED": {"log": True, "level": "error", "store": True},  # The item is dropped

            # Statistics Events
            "TOTAL_FLAGGED": {"log": True, "level": "info", "store": True},  # Tracks total flagged fields
            "TOTAL_DROPPED": {"log": True, "level": "info", "store": True},  # Tracks total dropped items

            # Data Debugging Events
            "ITEM_INPUT": {"log": True, "level": "debug", "store": False},  # Raw item before processing
            "ITEM_OUTPUT": {"log": True, "level": "debug", "store": False},  # Processed item after validation
            "FLAGGED_ITEMS": {"log": True, "level": "debug", "store": True},  # Stores flagged items
            "DROPPED_ITEMS": {"log": True, "level": "debug", "store": True},  # Stores dropped items
        }

        # Defines thresholds for validation failures before item is dropped
        THRESHOLD_RULES = {
            "FAILURE_THRESHOLD": 0,  # Minimum number of failed fields before dropping item
            "FLAG_THRESHOLD": 3,  # Minimum number of flagged fields before dropping item
        }

        if self.enable_logging:
            if logging_rules:
                # Validate custom rules to ensure only allowed keys are overridden
                for key in logging_rules:
                    if key not in DEFAULT_LOGGING_RULES:
                        raise KeyError(f"Invalid logging rule: {key}")

                # Merge default logging rules with user-defined rules
                self.logging_rules = {**DEFAULT_LOGGING_RULES, **logging_rules}
            else:
                self.logging_rules = DEFAULT_LOGGING_RULES
        else:
            self.logging_rules = None

    # Increments a Scrapy stat by a given amount
    def increment_stat(self, stat_name: str, value: int = 1):
        self.spider.crawler.stats.inc_value(stat_name, count=value)

    # Method for appending to a given stat
    def append_to_stat(self, stat_name: str, data: dict | list):
        """
        Stores non-integer statistics such as flagged/dropped items.
        Ensures previous values are retained instead of overwritten.
        """
        pass  # TODO: Retrieve existing data, append new entry, and store it back

    # Method for getting a stat
    def get_stat(self, stat_name: str, default=None):
        """
        Fetches the current value of a tracked statistic.
        Used to retrieve statistics stored across different pipelines.
        """
        pass  # TODO: Implement retrieval of stored statistics

    # Determines whether an item should be dropped based on failed rules.
    def should_drop_item(self, failed_validations: dict) -> bool:
        """
        Determines if an item should be dropped based on threshold rules.
        Checks both failure and flag count thresholds.
        """
        pass  # TODO: Count the number of failed and flagged fields, compare to thresholds

    def log_validation_results(self, failed_validations: dict, logging_rules=None):
        """
        Logs failed validations according to predefined logging behavior.
        Uses logging level rules to distinguish between warnings and errors.
        """
        pass  # TODO: Iterate through failed fields, determine log levels, log appropriately

    def validate_item(self, item: dict, rules: dict[str, callable], use_universal_default_rules=True,
                      ignore_defaults=False) -> dict:
        """
        Applies field validation rules dynamically and returns a dictionary
        containing fields that failed validation.

        :param item: dict of items scraped
        :param rules: dict where keys are field names and values are validation callables
                Callables must return either bool or (bool, new_value)
        :param use_universal_default_rules: If True, applies default rules to all fields
                If False, applies to fields not in `rules`
        :param ignore_defaults: If True, skips default rules entirely
        :return: Dict containing failed validations and modified values (if applicable)
        """
        adapter = ItemAdapter(item)
        flagged_values = {}
        invalid_values = {}

        # Helper function to process validation results
        def _process_validation_result(field, result):
            """
            Determines whether a field is clean, suspicious, or invalid.
            - result must be either (is_valid, new_value) or just a boolean.
            """
            if isinstance(result, tuple):
                is_valid, new_value = result
                if is_valid is None:
                    flagged_values[field] = adapter[field]  # Suspicious but not invalid
                elif not is_valid:
                    invalid_values[field] = adapter[field]  # Invalid and should be dropped
                else:
                    adapter[field] = new_value  # Valid and can be cleaned
            elif isinstance(result, bool):
                if not result:
                    invalid_values[field] = adapter[field]  # Invalid field
            else:
                raise ValueError(f"Invalid return type from validation rule for {field}")

        # Apply validation rules to each field
        for key, value in adapter.items():
            try:
                if key in rules:
                    # Apply default rules if enabled
                    if use_universal_default_rules:
                        for function in self.default_rules.values():
                            _process_validation_result(key, function(value))

                    _process_validation_result(key, rules[key](value))

                # Apply default rules if they are not ignored and no custom rule exists
                elif not use_universal_default_rules and not ignore_defaults:
                    for function in self.default_rules.values():
                        _process_validation_result(key, function(value))

            except Exception as e:
                self.spider.logger.error(f"Error validating item {key}: {value}, Exception: {e}")
                invalid_values[key] = value  # Treat validation failure as failed if exception occurs

        return {"flagged": flagged_values, "invalid": invalid_values}




    """
    Logs an event based on the logging rules configuration.
    Also determines whether the event should be stored in Scrapy stats based upon the "store" key.
    """
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
