import random


def get_weighted_choice(population, weights, k=1):
    """
    Selects k elements from a weighted population using random.choices
    Expects population and weights to be equal-length lists
    Returns a single item if k=1, otherwise a list of items
    """
    if not k == 1:
        return random.choices(population, weights=weights, k=k)
    else:
        return random.choices(population, weights=weights, k=k)[0]



def get_random_user_agent(skew=True) -> str:
    # TODO, customize user agents like accept languages
    user_agents = {
        # Windows + Chrome
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36": 10.0,

        # macOS + Safari
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15": 3.5,

        # Linux + Firefox
        "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0": 2.0,

        # Windows + Firefox
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0": 1.5,

        # macOS + Chrome
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36": 1.0,

        # Linux + Chrome
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36": 0.7
    }

    if not skew:
        return random.choice(list(user_agents.keys()))

    return get_weighted_choice(list(user_agents.keys()), list(user_agents.values()), 1)


def get_random_accept_language(skew=True, language="en", randomize_primary=False, append_alternates=False,
                               alternate_count=1) -> str:
    # TODO make docstrings better
    """
    :param skew: Boolean, whether or not headers should be weighted
    :param language: Which language will be generated as the primary
    :param randomize_primary: Boolean, whether or not to allow foreign lanuage as primary choice
    :param append_alternates: Boolean, whether or not to attempt random language alternates
    :param alternate_count: Number of alternates to generate
    :return:
    """
    language_prefix = {
        "en": 10.0,  # English (most dominant on the web)
        "es": 5.5,  # Spanish (Spain + Latin America + US)
        "fr": 4.0,  # French (France, Canada, parts of Africa)
        "zh": 3.5,  # Chinese (Simplified & Traditional)
        "de": 3.0,  # German (Germany, Austria, Switzerland)
        "pt": 2.5,  # Portuguese (Brazil, Portugal, Angola)
        "ru": 2.2,  # Russian (Russia, Ukraine, CIS countries)
        "ar": 2.0  # Arabic (Middle East, North Africa)
    }

    # If randomize is active then pick randomly from this list
    if randomize_primary:
        if skew:
            prefix = get_weighted_choice(list(language_prefix.keys()), list(language_prefix.values()))
        else:
            prefix = random.choice(list(language_prefix.keys()))
    elif language in language_prefix:
        prefix = language_prefix[language]
    # Default to english
    else:
        prefix = "en"

    en_suffix = {
        "US": 10.0,
        "GB": 3.5,
        "CA": 2.5,
        "AU": 2.0,
        "IN": 1.6,
        "IE": 1.2,
        "NZ": 1.0,
        "ZA": 0.8,
        "SG": 0.7,
        "PH": 0.6,
        "NG": 0.5,
        "HK": 0.5,
        "PK": 0.4,
        "KE": 0.3,
        "GH": 0.3,
        "MY": 0.2,
        "TT": 0.2,
        "IL": 0.2,
        "BZ": 0.1,
        "MT": 0.1,
        "UG": 0.1,
        None: 2.0
    }
    fr_suffix = {
        "FR": 10.0,
        "CA": 3.0,
        "BE": 1.5,
        "CH": 1.0,
        "LU": 0.5,
        "CI": 0.4,
        "SN": 0.3,
        "MA": 0.3,
        "TN": 0.2,
        None: 1.5
    }
    es_suffix = {
        "ES": 10.0,
        "MX": 6.0,
        "AR": 3.0,
        "CO": 2.5,
        "CL": 2.0,
        "PE": 1.8,
        "VE": 1.5,
        "US": 1.2,
        "EC": 1.0,
        "GT": 0.8,
        None: 1.0
    }
    de_suffix = {
        "DE": 10.0,
        "AT": 2.5,
        "CH": 2.0,
        "LU": 0.5,
        "BE": 0.3,
        None: 1.0
    }
    zh_suffix = {
        "CN": 10.0,
        "SG": 2.5,
        "TW": 2.0,
        "HK": 1.8,
        "MO": 0.5,
        None: 1.5
    }
    ru_suffix = {
        "RU": 10.0,
        "UA": 3.0,
        "BY": 2.5,
        "KZ": 1.0,
        "KG": 0.5,
        "UZ": 0.4,
        None: 1.2
    }
    pt_suffix = {
        "BR": 10.0,
        "PT": 4.0,
        "AO": 1.0,
        "MZ": 0.5,
        None: 0.8
    }
    ar_suffix = {
        "SA": 10.0,
        "EG": 4.0,
        "AE": 3.5,
        "MA": 2.0,
        "DZ": 1.8,
        "IQ": 1.5,
        "TN": 1.0,
        "JO": 0.8,
        "LB": 0.6,
        None: 1.0
    }
    language_suffixes = {
        "en": en_suffix,
        "fr": fr_suffix,
        "es": es_suffix,
        "de": de_suffix,
        "zh": zh_suffix,
        "ru": ru_suffix,
        "pt": pt_suffix,
        "ar": ar_suffix
    }

    # TODO, more advanced logic for determining the appropriate alternate based off preceding languages, currently is random
    # would involve increasing the likelihood of the same language following itself, especially no preference suffixes

    suffix_dict = language_suffixes.get(prefix)
    if not suffix_dict:
        raise ValueError(f"Unknown language prefix: {prefix}")

    if skew:
        suffix = get_weighted_choice(list(suffix_dict.keys()), list(suffix_dict.values()))
    else:
        suffix = random.choice(list(suffix_dict.keys()))

    # Account for no preference
    if suffix:
        argument = f"{prefix}-{suffix}"
    else:
        argument = f"{prefix}"

    if append_alternates:
        for i in range(alternate_count):
            argument += ","
            if skew:
                prefix = get_weighted_choice(list(language_prefix.keys()), list(language_prefix.values()))
            else:
                prefix = random.choice(list(language_prefix.keys()))
            suffix_dict = language_suffixes.get(prefix)
            if skew:
                suffix = get_weighted_choice(list(suffix_dict.keys()), list(suffix_dict.values()))
            else:
                suffix = random.choice(list(suffix_dict.keys()))

            if suffix:
                argument += f"{prefix}-{suffix};"
            else:
                argument += f"{prefix};"

            # Append relative priority
            argument += f"q={0.9 - i * 0.1}"

    return argument


def get_random_DNT(skew=True) -> str:
    """
        Returns a random DNT value
        Skew controls the probability of certain DNT values, by default it is set to better mimic real DNT values
    """
    # TODO, check if these are realistic skews
    DNT_vals = {
        "1": 2,
        "0": 1,
        None: 7
    }
    if not skew:
        return random.choice(list(DNT_vals.keys()))

    return get_weighted_choice(list(DNT_vals.keys()), list(DNT_vals.values()), 1)


def get_random_headers(replacements=None) -> dict:
    # TODO, generate more headers
    """
    Returns a random headers dictionary
    :param replacements:
    :return:
    """
    headers = {
        "User-Agent": get_random_user_agent(),
        "Accept-Language": get_random_accept_language(),
        "DNT": get_random_DNT(),
    }

    headers = {
        k: v for k, v in headers.items() if v is not None
    }

    if replacements:
        headers.update(replacements)
    return headers


def get_random_wait_time(min_ms=1500, max_ms=4500) -> int:
    return random.randint(min_ms, max_ms)
