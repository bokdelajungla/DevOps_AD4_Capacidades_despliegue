
from server import app


def test_almacena_post_no_token():
    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        response = test_client.post('/almacena?string=main')
        assert response.status_code == 200
        assert b"token is missing" in response.data
    return 0

def test_almacena_bad_request_no_string_parameter():
    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        response = test_client.post('/almacena?bad=main')
        assert response.status_code == 200
        assert b"token is missing" in response.data
    return 0

def test_almacena_get():
    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        response = test_client.get('/almacena?string=main')
        assert response.status_code == 405
    return 0
