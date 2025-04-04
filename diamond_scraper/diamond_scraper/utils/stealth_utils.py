import random

def get_weighted_choice(population, weights, k):
    return random.choices(population, weights=weights, k=k)

def get_random_user_agent() -> str:
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64)",
    ]
    return random.choice(user_agents)

def get_random_accept_language(skew = True) -> str:
    accept_languages = [
        "en-US",
        ""
    ]


# Todo check if dnt is a string
def get_random_DNT(skew = True) -> str:
    """
        Returns a random DNT value
        Skew controls the probability of certain DNT values, by default it is set to better mimic real DNT values
    """
    DNT_vals = {
        "1" : 8,
        "0" : 1,
        "null" : 1
    }
    if not skew:
        return random.choice(list(DNT_vals.keys()))

    return get_weighted_choice(list(DNT_vals.keys()),list(DNT_vals.values()),1)


def get_random_headers() -> dict:
    """
        Returns a dictionary of basic randomized headers:
        - User-Agent
        - Accept-Language
        - DNT (Do Not Track)
    """
    headers = {
        "User-Agent": get_random_user_agent(),
        "Accept-Language": get_random_accept_language(),
        "DNT": get_random_DNT(),
    }
    pass

def get_random_wait_time(min_ms=1500, max_ms=4500) -> int:
    return random.randint(min_ms, max_ms)