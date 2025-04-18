from enum import Enum
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import diamond_scraper.utils.stats_util as stats_util

class ValidationLogger:
    def __init__(self, spider, enable_logging=False, pipline_name=None, logging_rules=None, threshold_rules=None,
                 default_rules=None):
        self.spider = spider

        # Determines if the class will handle logging itself
        self.enable_logging = enable_logging
        self.pipline_name = pipline_name

        # Default rules are expected to be defined by the user in dict[str, callable] format
        self.default_rules = default_rules if default_rules is not None else {}

        # Default rules for logging behavior (log level and storage settings)
        DEFAULT_LOGGING_RULES = {
            # Validation Events
            "FIELD_FAILURE": {"log": False, "level": "warning"},  # A field fails validation
            "ITEM_FAILURE": {"log": True, "level": "error"},  # An item fails validation
            "FIELD_FLAGGED": {"log": True, "level": "warning"},  # A field is flagged
            "ITEM_DROPPED": {"log": True, "level": "error"},  # The item is dropped

            # Statistics Events
            "TOTAL_FLAGGED": {"log": True, "level": "info", "store": True},  # Tracks total flagged fields
            "TOTAL_INVALID": {"log": True, "level": "info", "store": True},  # Tracks total invalid items

            # Data Debugging Events
            "ITEM_INPUT": {"log": True, "level": "debug", "store": False},  # Raw item before processing
            "ITEM_OUTPUT": {"log": True, "level": "debug", "store": False},  # Processed item after validation
            "FLAGGED_ITEMS": {"log": True, "level": "debug", "store": True},  # Stores flagged items
            "DROPPED_ITEMS": {"log": True, "level": "debug", "store": True},  # Stores dropped items
        }

        # Defines thresholds for validation failures before item is dropped, set value to None to never drop items
        THRESHOLD_RULES = {
            "FAILURE_THRESHOLD": 0,  # Minimum number of failed fields before dropping item
            "FLAG_THRESHOLD": 3,  # Minimum number of flagged fields before dropping item
        }

        # Merge logging rules with user-defined rules (if enabled)
        self.logging_rules = {} if not enable_logging else {**DEFAULT_LOGGING_RULES, **(logging_rules or {})}

        # Merge threshold rules with user-defined rules
        self.threshold_rules = {**THRESHOLD_RULES, **(threshold_rules or {})}

        # Validate user-defined logging rules
        if logging_rules:
            for key in logging_rules:
                if key not in DEFAULT_LOGGING_RULES:
                    raise KeyError(f"Invalid logging rule: {key}")

        # Validate user-defined threshold rules
        if threshold_rules:
            for key in threshold_rules:
                if key not in THRESHOLD_RULES:
                    raise KeyError(f"Invalid threshold rule: {key}")

    def process_item(self, item: dict, rules: dict[str, callable]) -> dict:
        """
        High-level flow method that:
          1. Validates the item
          2. Logs flagged/invalid values based on settings
          3. Decides whether to drop the item
          4. Returns cleaned item or raises DropItem

        :param item: The scraped item dictionary
        :param rules: Validation rules to apply
        :return: Cleaned item if valid, raises DropItem if not
        """
        item, validation_results = self.validate_item(item, rules)

        self.log_validation_results(validation_results)

        if self.should_drop_item(validation_results):
            raise DropItem(f"Dropping item due to invalid values: {validation_results}")

        return item

    def validate_item(self, item: dict, rules: dict[str, callable], use_universal_default_rules=True) \
            -> (dict, dict[str, dict]):
        """
        Applies field validation rules dynamically and returns a dictionary containing fields that failed validation.

        :param item: dict of items scraped
        :param rules: dict where keys are field names and values are validation callable.
                Callables must return either bool or (bool, new_value)
        :param use_universal_default_rules: If True, applies default rules to all fields.
                If False, applies to fields not in `rules`
        :return: Dict containing failed validations and modified values (if applicable)
        """

        self.log_event("ITEM_INPUT", "Item input before validation: {}", item)

        if self.logging_rules.get("ITEM_INPUT", {}).get("store", False):
            stats_util.append_to_stat(self.spider, "ITEM_INPUT", item)

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
                    self.log_event("FIELD_FLAGGED", "Field {} has been flagged as suspicious", field)
                elif not is_valid:
                    invalid_values[field] = adapter[field]  # Invalid and should be dropped
                    self.log_event("FIELD_FAILURE", "Field {} has failed validation", field)
                else:
                    adapter[field] = new_value  # Valid and can be cleaned
            elif isinstance(result, bool):
                if not result:
                    invalid_values[field] = adapter[field]  # Invalid field
                    self.log_event("FIELD_FAILURE", "Field {} has failed validation", field)
            elif result is None:
                flagged_values[field] = adapter[field]  # Suspicious but not invalid
                self.log_event("FIELD_FLAGGED", "Field {} has been flagged as suspicious", field)
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
                elif not use_universal_default_rules:
                    for function in self.default_rules.values():
                        _process_validation_result(key, function(value))

            except Exception as e:
                self.spider.logger.error(f"Error validating item {key}: {value}, Exception: {e}")
                invalid_values[key] = value  # Treat validation failure as failed if exception occurs

        # Un-adapt the item
        item = dict(adapter)
        self.log_event("ITEM_OUTPUT", "Item output after validation: {}", item)

        if self.logging_rules.get("ITEM_OUTPUT", {}).get("store", False):
            stats_util.append_to_stat(self.spider, "ITEM_OUTPUT", item)

        return item, {"flagged": flagged_values, "invalid": invalid_values}

    def should_drop_item(self, validation_results: dict) -> bool:
        """
        Determines if an item should be dropped based on threshold rules.
        Logs flagged/invalid counts and drops the item if thresholds are exceeded.
        """
        drop = False

        flagged_values = validation_results.get("flagged", {})
        invalid_values = validation_results.get("invalid", {})

        num_flagged_items = len(flagged_values)
        num_invalid_items = len(invalid_values)

        # Check if thresholds for dropping are exceeded
        exceeds_flag_threshold = (0 < self.threshold_rules["FLAG_THRESHOLD"] < num_flagged_items)
        exceeds_failure_threshold = (0 < self.threshold_rules["FAILURE_THRESHOLD"] < num_invalid_items)

        if exceeds_flag_threshold or exceeds_failure_threshold:
            drop = True

            self.log_event(
                "ITEM_DROPPED",
                "Item dropped due to exceeding thresholds - Flagged: {flagged}/{flagged_threshold}, "
                "Invalid: {invalid}/{invalid_threshold}.",
                flagged=num_flagged_items, flagged_threshold=self.threshold_rules["FLAG_THRESHOLD"],
                invalid=num_invalid_items,  invalid_threshold=self.threshold_rules["FAILURE_THRESHOLD"]
            )

        return drop

    def log_validation_results(self, validation_results: dict) -> None:
        """
        Handles logging of the validation results.
        """
        if not self.enable_logging:
            return

        flagged_values = validation_results.get("flagged", {})
        invalid_values = validation_results.get("invalid", {})

        num_flagged_items = len(flagged_values)
        num_invalid_items = len(invalid_values)

        # Log general validation failure
        if num_flagged_items > 0 or num_invalid_items > 0:
            self.log_event(
                "ITEM_FAILURE",
                "Item failed validation with {} flagged fields and {} invalid fields.",
                num_flagged_items, num_invalid_items
            )

        self.log_event("TOTAL_FLAGGED", "Total flagged fields: {}", num_flagged_items)

        self.log_event("TOTAL_INVALID", "Total invalid fields: {}", num_invalid_items)

        self.log_event("FLAGGED_ITEMS", "Flagged values: {}", flagged_values)

        self.log_event("INVALID_ITEMS", "Invalid values: {}", invalid_values)

        if self.logging_rules.get("TOTAL_FLAGGED", {}).get("store", False):
            stats_util.increment_stat(self.spider, StatEnum.TOTAL_FLAGGED.value, num_flagged_items)

        if self.logging_rules.get("TOTAL_INVALID", {}).get("store", False):
            stats_util.increment_stat(self.spider, StatEnum.TOTAL_INVALID.value, num_invalid_items)

        if self.logging_rules.get("FLAGGED_ITEMS", {}).get("store", False):
            stats_util.append_to_stat(self.spider, StatEnum.FLAGGED_ITEMS.value, flagged_values)

        if self.logging_rules.get("INVALID_ITEMS", {}).get("store", False):
            stats_util.append_to_stat(self.spider, StatEnum.INVALID_ITEMS.value, invalid_values)

    def log_event(self, event_name: str, message_template: str, *args, **kwargs):
        """
        General logging method with support for formatted messages.
        :param event_name: The logging rule key.
        :param message_template: A template string for logging.
        :param args: Positional arguments for formatting.
        :param kwargs: Keyword arguments for formatting.
        """

        if not self.enable_logging:
            return

        log_config = self.logging_rules.get(event_name, {"log": False, "level": "info"})

        if log_config.get("log", False):
            log_level = log_config.get("level", "info")

            # Dynamically format message with provided arguments
            formatted_message = message_template.format(*args, **kwargs)

            # Log according to provided specifications
            getattr(self.spider.logger, log_level, self.spider.logger.info)(formatted_message)


def track_db_event(self, event: Enum, message: str = None, level: str = "info"):
    """
    Increments the specified DB event stat and optionally logs a message.

    :param event: logging rule key
    :param message: message to be logged
    :param level: logging level of the event
    :return: None
    """
    stats_util.increment_stat(self.spider, event.value, 1)

    if message and self.enable_logging:
        # Use self.spider.logger if available
        if hasattr(self.spider, 'logger'):
            getattr(self.spider.logger, level.lower())(f"[DB_EVENT] {message}")
        else:
            print(f"[DB_EVENT] {message}")


def log_general_message(self, message: str, level: str = "info"):
    """
    Logs a custom message at the given level.
    This is outside the normal validation flow, for custom usage.
    """
    if not self.enable_logging:
        return

    if hasattr(self.spider, 'logger'):
        getattr(self.spider.logger, level.lower())(f"[GENERAL] {message}")
    else:
        print(f"[GENERAL] {message}")


class StatEnum(Enum):
    ITEMS_PROCESSED = "custom/items_processed"
    ITEMS_DROPPED = "custom/items_dropped"

    # Validation stats
    TOTAL_FLAGGED = "custom/total_flagged"
    TOTAL_INVALID = "custom/total_invalid"

    # Field-level tracking
    FLAGGED_FIELDS = "custom/flagged_fields"
    INVALID_FIELDS = "custom/invalid_fields"

    # Debugging and Item Flow Tracking
    ITEM_INPUT = "custom/item_input"
    ITEM_OUTPUT = "custom/item_output"
    FLAGGED_ITEMS = "custom/flagged_items"
    INVALID_ITEMS = "custom/invalid_items"
    DROPPED_ITEMS = "custom/dropped_items"

    # Database tracking
    DB_TABLE_CREATED = "custom/db_table_created"
    DB_TABLE_CREATE_FAILED = "custom/db_table_create_failed"
    DB_INSERT_SUCCESS = "custom/db_insert_success"
    DB_INSERT_FAILED = "custom/db_insert_failed"
