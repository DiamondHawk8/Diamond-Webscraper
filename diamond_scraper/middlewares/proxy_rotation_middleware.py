import random
from scrapy import signals
from collections import defaultdict


class ProxyRotationMiddleware:
    """
    Middleware to rotate proxies and track failures across sessions.
    """

    def __init__(self, proxy_list, fallback_proxy):
        self.proxy_list = proxy_list
        self.fallback_proxy = fallback_proxy
        self.proxy_failures = defaultdict(int)  # Tracks failures per proxy

    @classmethod
    def from_crawler(cls, crawler):
        """
        :param crawler: crawler instance
        :return: middleware instance
        """
        fallback_proxy = crawler.settings.get("FALLBACK_PROXY")
        middleware = cls(crawler.settings.get('PROXY_LIST', []), fallback_proxy)
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    def process_request(self, request, spider, failure_check=True, enable_fallback_proxy=True):
        """
        :param request: outgoing request
        :param spider: spider instance
        :param failure_check:
        :param enable_fallback_proxy: enable fallback proxy
        """

        proxy = None

        # TODO dynamically assign proxies, and adjust util usage based on responses
        if failure_check:
            viable_proxies = [p for p in self.proxy_list if self.proxy_failures[p] < 3]
        else:
            viable_proxies = self.proxy_list

        if viable_proxies:
            proxy = random.choice(viable_proxies)
        elif enable_fallback_proxy and self.fallback_proxy:
            proxy = self.fallback_proxy
        else:
            spider.logger.warning("No viable proxies provided. Request will not use a proxy.")

        if proxy:
            request.meta['proxy'] = proxy

    def spider_closed(self, spider):
        spider.logger.info(f"Proxy middleware shut down. Total proxies used: {len(self.proxy_list)}")
