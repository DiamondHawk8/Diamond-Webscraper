def get_stat(spider, stat_name: str, default=None):
    """
    Fetches the current value of a tracked statistic.
    """
    return spider.crawler.stats.get_value(stat_name, default)


def increment_stat(spider, stat_name: str, value: int = 1):
    """
    Increments a numeric statistic counter by the specified value.
    """
    spider.crawler.stats.inc_value(stat_name, count=value)


def append_to_stat(spider, stat_name: str, data: dict):
    """
    Appends a dictionary to a list-based statistic.
    Ensures stats are stored as lists and retains previous entries.
    """
    current = get_stat(spider, stat_name, default=[])
    if not isinstance(current, list):
        current = [current]

    current.append(data)
    spider.crawler.stats.set_value(stat_name, current)
