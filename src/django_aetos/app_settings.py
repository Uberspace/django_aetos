
class AppSettings:
    def __init__(self, prefix):
        self.prefix = prefix
    
    def _setting(self, name, dflt):
        from django.conf import settings
        
        return getattr(settings, self.prefix + name, dflt)
    
    @property
    def ENABLE_IP_ALLOWLIST(self):
        return self._setting("ENABLE_IP_ALLOWLIST", False)

    @property
    def IP_ALLOWLIST(self):
        return self._setting("IP_ALLOWLIST", [])
    
    @property
    def ENABLE_AUTH(self):
        return self._setting("ENABLE_AUTH", False)
    
    @property
    def AUTH_TOKENLIST(self):
        return self._setting("AUTH_TOKENLIST", [])

_app_settings = AppSettings("AETOS_")

def __getattr__(name):
    # See https://peps.python.org/pep-0562/
    return getattr(_app_settings, name)