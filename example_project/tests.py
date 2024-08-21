import pytest
from django.test import override_settings

expected_output = """# HELP books_count Total number of books
# TYPE books_count counter
books_count 0
# HELP universes_count Total number of universes
# TYPE universes_count counter
universes_count 1
"""


@pytest.mark.django_db
def test_e2e(client):
    resp = client.get("/metrics")
    assert resp.content.decode() == expected_output


@override_settings(
    AETOS_ENABLE_IP_ALLOWLIST=True,
    AETOS_IP_ALLOWLIST=["127.0.0.1"],
    AETOS_ENABLE_AUTH=True,
    AETOS_AUTH_TOKENLIST=["AhGei6ohghooDae"],
)
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


@pytest.mark.django_db
@override_settings(AETOS_ENABLE_IP_ALLOWLIST=True, AETOS_IP_ALLOWLIST=["127.0.0.1"])
def test_enable_allowed_ips(client):
    resp = client.get("/metrics")
    assert resp.content.decode() == expected_output


@pytest.mark.django_db
@override_settings(AETOS_ENABLE_IP_ALLOWLIST=True, AETOS_IP_ALLOWLIST=["255.0.0.1"])
def test_enable_allowed_ips_not_allowed(client):
    resp = client.get("/metrics")
    assert resp.status_code == 401


@pytest.mark.django_db
@override_settings(AETOS_ENABLE_AUTH=True, AETOS_AUTH_TOKENLIST=["aquee4ro4Theeth"])
def test_enable_auth(client):
    resp = client.get("/metrics", headers={"Authorization": "Bearer aquee4ro4Theeth"})
    assert resp.content.decode() == expected_output


@pytest.mark.django_db
@override_settings(AETOS_ENABLE_AUTH=True, AETOS_AUTH_TOKENLIST=["aquee4ro4Theeth"])
def test_enable_auth_token_not_allowed(client):
    resp = client.get("/metrics", headers={"Authorization": "Bearer wr0ngt0kenf"})
    assert resp.status_code == 401


@pytest.mark.django_db
@override_settings(
    AETOS_ENABLE_IP_ALLOWLIST=True,
    AETOS_IP_ALLOWLIST=["127.0.0.1"],
    AETOS_ENABLE_AUTH=True,
    AETOS_AUTH_TOKENLIST=["aquee4ro4Theeth"],
)
def test_enable_all(client):
    resp = client.get("/metrics", headers={"Authorization": "Bearer aquee4ro4Theeth"})
    assert resp.content.decode() == expected_output


@pytest.mark.django_db
@override_settings(
    AETOS_ENABLE_IP_ALLOWLIST=True,
    AETOS_IP_ALLOWLIST=["255.0.0.1"],
    AETOS_ENABLE_AUTH=True,
    AETOS_AUTH_TOKENLIST=["aquee4ro4Theeth"],
)
def test_enable_all_wrong_ip(client):
    resp = client.get("/metrics", headers={"Authorization": "Bearer aquee4ro4Theeth"})
    assert resp.status_code == 401


@pytest.mark.django_db
@override_settings(
    AETOS_ENABLE_IP_ALLOWLIST=True,
    AETOS_IP_ALLOWLIST=["127.0.0.1"],
    AETOS_ENABLE_AUTH=True,
    AETOS_AUTH_TOKENLIST=["aquee4ro4Theeth"],
)
def test_enable_all_wrong_token(client):
    resp = client.get("/metrics", headers={"Authorization": "Bearer wr0ngt0ken"})
    assert resp.status_code == 401


@pytest.mark.django_db
@override_settings(
    AETOS_ENABLE_IP_ALLOWLIST=True,
    AETOS_IP_ALLOWLIST=["255.0.0.1"],
    AETOS_ENABLE_AUTH=True,
    AETOS_AUTH_TOKENLIST=["aquee4ro4Theeth"],
)
def test_enable_all_wrong_token_ip(client):
    resp = client.get("/metrics", headers={"Authorization": "Bearer wr0ngt0ken"})
    assert resp.status_code == 401


@pytest.mark.django_db
@override_settings(
    AETOS_ENABLE_IP_ALLOWLIST=True, AETOS_ENABLE_AUTH=True, AETOS_AUTH_TOKENLIST=["aquee4ro4Theeth"]
)
def test_enable_all_empty_ip(client):
    resp = client.get("/metrics", headers={"Authorization": "Bearer aquee4ro4Theeth"})
    assert resp.status_code == 401


@pytest.mark.django_db
@override_settings(
    AETOS_ENABLE_IP_ALLOWLIST=True, AETOS_IP_ALLOWLIST=["127.0.0.1"], AETOS_ENABLE_AUTH=True
)
def test_enable_all_empty_token(client):
    resp = client.get("/metrics", headers={"Authorization": "Bearer aquee4ro4Theeth"})
    assert resp.status_code == 401


@pytest.mark.django_db
@override_settings(AETOS_ENABLE_IP_ALLOWLIST=True, AETOS_ENABLE_AUTH=True)
def test_enable_all_empty_token_ip(client):
    resp = client.get("/metrics", headers={"Authorization": "Bearer aquee4ro4Theeth"})
    assert resp.status_code == 401


@pytest.mark.django_db
@override_settings(
    AETOS_ENABLE_IP_ALLOWLIST=True,
    AETOS_IP_ALLOWLIST=["127.0.0.1"],
    AETOS_ENABLE_AUTH=True,
    AETOS_AUTH_TOKENLIST=["aquee4ro4Theeth"],
)
def test_enable_all_wrong_auth_header(client):
    resp = client.get("/metrics", headers={"Authorization": "Basic aquee4ro4Theeth"})
    assert resp.status_code == 401
