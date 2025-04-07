class ProxyRotationMiddleware:
    """
    Middleware for rotating proxies between requests.

    Responsibilities:
    - Assigns a new proxy from a list to each request.
    - Ensures proxy usage is randomized and optionally avoids reuse.
    - Integrates with Playwright-enabled requests if needed.
    """

    def __init__(self, proxy_list):

        pass  # Store the proxy list internally

    @classmethod
    def from_crawler(cls, crawler):
        """
        Loads proxy list from Scrapy settings and returns an instance.

        Args:
            crawler: The Scrapy crawler instance.

        Returns:
            ProxyRotationMiddleware: Configured middleware instance.
        """
        pass  # Extract setting like 'PROXY_LIST' from crawler.settings

    def process_request(self, request, spider):
        """
        Attaches a proxy to the request.

        Args:
            request (scrapy.Request): The outgoing request.
            spider (scrapy.Spider): The active spider instance.
        """
        pass  # Randomly assign a proxy to request.meta['proxy']
