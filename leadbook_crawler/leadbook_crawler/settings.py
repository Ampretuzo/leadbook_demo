# -*- coding: utf-8 -*-

# Scrapy settings for leadbook_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import os
import string

BOT_NAME = "leadbook_crawler"

SPIDER_MODULES = ["leadbook_crawler.spiders"]
NEWSPIDER_MODULE = "leadbook_crawler.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'leadbook_crawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'leadbook_crawler.middlewares.LeadbookCrawlerSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'leadbook_crawler.middlewares.LeadbookCrawlerDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "leadbook_crawler.pipelines.LeadbookCompanyProfileCrawlerPipeline": 300
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Splash setup from https://blog.scrapinghub.com/2015/03/02/handling-javascript-in-scrapy-with-splash

DOWNLOADER_MIDDLEWARES = {
    "scrapy_splash.SplashCookiesMiddleware": 723,
    "scrapy_splash.SplashMiddleware": 725,
    "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 810,
}

_SPLASH_HOST = os.environ.get("LEADBOOK_SPLASH_HOST")
_SPLASH_PORT = os.environ.get("LEADBOOK_SPLASH_PORT")
SPLASH_URL = string.Template("http://$splash_host:$splash_port/").substitute(
    splash_host=_SPLASH_HOST, splash_port=_SPLASH_PORT
)

SPIDER_MIDDLEWARES = {"scrapy_splash.SplashDeduplicateArgsMiddleware": 100}

DUPEFILTER_CLASS = "scrapy_splash.SplashAwareDupeFilter"
HTTPCACHE_STORAGE = "scrapy_splash.SplashAwareFSCacheStorage"

# Custom settings

SGMARITIME_COMPANY_LUA_PATH = "splash_scripts/sgmaritime_company.lua"

_RABBIT_UNAME = os.environ.get("LEADBOOK_RABBIT_UNAME")
_RABBIT_PWD = os.environ.get("LEADBOOK_RABBIT_PWD")
_RABBIT_ADDRESS = os.environ.get("LEADBOOK_RABBIT_ADDRESS")
BROKER_URI = string.Template(
    "amqp://$broker_uname:$broker_pwd@$broker_address"
).substitute(
    broker_uname=_RABBIT_UNAME, broker_pwd=_RABBIT_PWD, broker_address=_RABBIT_ADDRESS
)
