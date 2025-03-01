# Validation and Logging Utility for Scrapy Pipelines

## Overview

This utility class is designed to assist with:

- **Data Cleaning** (optional, can be done in rules)
  - Cleaning can be done inside validation rules using `(True, new_value)`.
- **Validation & Flagging** of item fields
- **Logging & Statistics Collection** for pipeline processing

## Usage

### 1. Instantiate the Utility Class

In a Scrapy pipeline, create an instance of the class:

```python
tracker = ValidationLogger(spider)
```

### 2. Define Validation Rules

Validation rules can:

### 2. Define Validation Rules
Validation rules can:
- **Return `True`** → The value is valid.
- **Return `False`** → The value is invalid and will be logged as an error.
- **Return `None`** → The value is suspicious and will be logged but kept.
- **Return `(True, new_value)`** → The value is valid and replaced with `new_value`.
- **Return `(False, new_value)`** → The value is invalid, replaced, and marked for dropping.
- **Return `(None, new_value)`** → The value is suspicious, replaced, and logged but kept.

#### Example Rule Set:

```python
rules = {
    "tickerSymbol": lambda x: (True, x.upper().replace(" ", "")),  # Cleaning rule
    "price": lambda x: (None if x < 1 else True, x),  # Suspicious if price < 1
    "volume": lambda x: (x >= 0, x),  # Invalid if volume is negative
}
```

### 3. Validate an Item

Pass an **item dictionary** and the **rules** into `validate_item()`:

```python
item = {"tickerSymbol": " msft ", "price": 0.5, "volume": -100}

item, validation_results = tracker.validate_item(item, rules)

print(validation_results)
```

#### Example Output:

```python
{
    "flagged": {"price": 0.5},  # Suspicious value but still valid
    "invalid": {"volume": -100}  # Invalid field, item should be dropped
}
```

### 4. Log Validation Results

```python
tracker.log_validation_results(validation_results)
```

### 5. Decide Whether to Drop the Item

```python
should_drop = tracker.should_drop_item(validation_results)

if should_drop:
    raise DropItem(f"Dropping item due to invalid values: {validation_results['invalid']}")
```

### 6. Process an Item in One Step

If you want to **run validation, logging, and dropping in a single step**, use `process_item()`:

```python
cleaned_item = tracker.process_item(item, rules)
```

This method:

1. Validates the item.
2. Logs flagged/invalid values.
3. Drops the item if necessary.
4. Returns the cleaned item if valid.

