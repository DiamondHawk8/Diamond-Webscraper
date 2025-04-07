import random
from scrapy import signals
class ProxyRotationMiddleware:
    """
    Middleware for rotating proxies between requests.
        - Assigns a random proxy to each request
        - Pulls proxies from settings from  PROXY_LIST
    """

    def __init__(self, proxy_list):
        self.proxy_list = proxy_list

    @classmethod
    def from_crawler(cls, crawler):
        """

        :param crawler: crawler instance
        :return: middleware instance
        """
        middleware = cls(crawler.settings.get('PROXY_LIST', []))
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    def process_request(self, request, spider):
        """

        :param request: outgoing request
        """
        # TODO dynamically assign proxies based on responses
        if self.proxy_list:
            request.meta['proxy'] = random.choice(self.proxy_list)
        else:
            spider.logger.warning("Proxy list is empty. Request will not use a proxy.")

    def spider_closed(self, spider):
        spider.logger.info(f"Proxy middleware shut down. Total proxies used: {len(self.proxy_list)}")