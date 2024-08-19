import pytest
from django.test import override_settings


@pytest.mark.django_db
def test_e2e(client):
    resp = client.get("/metrics")
    assert (
        resp.content.decode()
        == """# HELP books_count Total number of books
# TYPE books_count counter
books_count 0
# HELP universes_count Total number of universes
# TYPE universes_count counter
universes_count 1
"""
    )

@override_settings(AETOS_ENABLE_IP_ALLOWLIST=True, AETOS_IP_ALLOWLIST=["127.0.0.1"], AETOS_ENABLE_AUTH=True, AETOS_AUTH_TOKENLIST=["AhGei6ohghooDae"])
def test_settings():
    from django_aetos import app_settings
    assert app_settings.ENABLE_IP_ALLOWLIST == True
    assert app_settings.IP_ALLOWLIST == ["127.0.0.1"]
    assert app_settings.ENABLE_AUTH == True
    assert app_settings.AUTH_TOKENLIST == ["AhGei6ohghooDae"]
    
def test_settings_defaults():
    from django_aetos import app_settings
    assert app_settings.ENABLE_IP_ALLOWLIST == False
    assert app_settings.IP_ALLOWLIST == []
    assert app_settings.ENABLE_AUTH == False
    assert app_settings.AUTH_TOKENLIST == []