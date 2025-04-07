import random
from scrapy import signals
from collections import defaultdict
import diamond_scraper.utils.stats_util as stats_util

class ProxyRotationMiddleware:
    """
    Middleware to rotate proxies and track failures across sessions.
    """

    def __init__(self, proxy_list, fallback_proxy, failure_check_enabled, failure_threshold):
        self.proxy_list = proxy_list
        self.fallback_proxy = fallback_proxy
        self.failure_check_enabled = failure_check_enabled
        self.failure_threshold = failure_threshold
        self.proxy_failures = defaultdict(int)  # Tracks failures per proxy
        self.proxy_uses = defaultdict(int)  # Tracks usage of each proxy

    @classmethod
    def from_crawler(cls, crawler):
        """
        :param crawler: crawler instance
        :return: middleware instance
        """
        proxy_list = crawler.settings.get('PROXY_LIST', [])
        fallback_proxy = crawler.settings.get("FALLBACK_PROXY", None)
        failure_check_enabled = crawler.settings.get("PROXY_FAILURE_CHECK_ENABLED", False)
        failure_threshold = crawler.settings.get("FAILURE_THRESHOLD", None)
        middleware = cls(proxy_list, fallback_proxy, failure_check_enabled, failure_threshold)
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    def process_request(self, request, spider):
        """
        :param request: outgoing request
        :param spider: spider instance
        """

        proxy = None

        # TODO dynamically assign proxies, and adjust util usage based on responses
        if self.failure_check_enabled:
            viable_proxies = [p for p in self.proxy_list if self.proxy_failures[p] < self.failure_threshold]
        else:
            viable_proxies = self.proxy_list

        if viable_proxies:
            proxy = random.choice(viable_proxies)
        elif self.fallback_proxy:
            proxy = self.fallback_proxy
        else:
            spider.logger.warning("No viable proxies provided. Request will not use a proxy.")

        if proxy:
            spider.logger.info(f"Using proxy: {proxy}")
            self.proxy_uses[proxy] += 1
            request.meta['proxy'] = proxy

    def process_exception(self, request, exception, spider):
        """
        Increments failure count if a proxy is used and the request fails.
        """
        proxy = request.meta.get('proxy')
        if proxy and self.failure_check_enabled:
            self.proxy_failures[proxy] += 1

    def spider_closed(self, spider):
        stats_util.append_to_stat(spider, "PROXY_FAILURES", self.proxy_failures)
        stats_util.append_to_stat(spider, "PROXY_USES", self.proxy_uses)
        spider.logger.info(f"Proxy middleware shut down. Total proxies used: {len(self.proxy_list)}")
