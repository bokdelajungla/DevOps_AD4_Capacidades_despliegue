
from server import Flask
from server import app
from server import HOST
from server import main
from unittest import mock
import argparse
import json


def test_consulta_get_no_token():
    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        response = test_client.get('/consulta?string=test')
        assert response.status_code == 200
        assert b"token is missing" in response.data
        #assert b"4" in response.data
    return 0

def test_consulta_bad_request_no_string_parameter():
    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        response = test_client.get('/consulta?bad=test')
        assert b"token is missing" in response.data
    return 0

def test_consulta_bad_request_2_words():
    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        response = test_client.get('/consulta?string=test espacio')
        assert response.status_code == 200
        assert b"token is missing" in response.data
    return 0

def test_consulta_bad_request_wrong_method():
    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        response = test_client.post('/consulta?string=test')
        assert response.status_code == 405
    return 0
