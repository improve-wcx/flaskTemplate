from app import app


def test_hello(caplog):
    caplog.clear()
    client = app.test_client()
    with caplog.at_level("INFO"):
        resp = client.get("/")

    assert resp.status_code == 200
    assert b"Hello, World!" in resp.data

    # Ensure the request was logged
    assert any("GET /" in rec.getMessage() for rec in caplog.records)
