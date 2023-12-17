import pytest


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
