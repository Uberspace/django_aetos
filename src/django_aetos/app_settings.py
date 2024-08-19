from django.conf import settings

ENABLE_IP_ALLOWLIST = getattr(settings, "AETOS_ENABLE_IP_ALLOWLIST", False)
IP_ALLOWLIST = getattr(settings, "AETOS_IP_ALLOWLIST", [])
ENABLE_AUTH = getattr(settings, "AETOS_ENABLE_AUTH", False)
AUTH_TOKENLIST = getattr(settings, "AETOS_AUTH_TOKENLIST", [])