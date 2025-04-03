import random
def get_random_user_agent() -> str:
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64)",
    ]
    return random.choice(user_agents)

def get_random_headers() -> dict:
    pass

def get_random_wait_time(min_ms=1500, max_ms=4500) -> int:
    pass