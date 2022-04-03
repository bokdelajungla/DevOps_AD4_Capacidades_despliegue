
import os
from unittest import mock

import argparse

from server import create_app
from server import check_file
from server import main
from config.default import PORT


def test_create_app():
    app = create_app()
    assert(app is not None)


def test_create_file():
    assert (check_file("testFile.txt") == 0)


def test_file_already_exists():
    assert (check_file("testFile.txt") == 1)
    os.remove("testFile.txt")



def test_default_parameters():
    file, port = main()
    assert file == FILENAME
    assert port == PORT


@mock.patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(file="tests/test.txt", port=23456))
def test_parameters(mock_args):
    file, port = main()
    assert file == "tests/test.txt"
    assert port == 23456


def test_homepage():
    app = create_app()
    with app.test_client() as test_client:
        response = test_client.get('/')
    assert response.status_code == 200
    assert b"Servicio Web para Cadenas" in response.data

