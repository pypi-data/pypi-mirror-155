"""Configuration."""
import os

CLI_ENV = os.getenv("CLI_ENV", "prod")

DEFAULT_SHOP = ""
AUTH_TIMEOUT = 120
CLIENT_ID = "5f0ef15fa8037afc5992380960561151"

# product environment, use .com domain
if CLI_ENV == "prod":
    ACCOUNT_API_URL = "https://accounts.funpinpin.cn/api"
    PARTNER_API_URL = "https://partners.funpinpin.com/api"
    DOMAIN_SUFFIX = "com"
else:
    ACCOUNT_API_URL = "https://accounts.funpinpin.top/api"
    PARTNER_API_URL = "https://partners.funpinpin.top/api"
    DOMAIN_SUFFIX = "top"

REDIRECT_URI = "http://127.0.0.1:3456"
