import os
import sys
import pytest
from src import app

# os.path.dirname
# Fungsi: Mengambil nama direktori dari path file yang diberikan.
# -------------------------------------------------------------------
# os.path.abspath(__file__)
# Fungsi: Mengambil path absolut dari file yang sedang dieksekusi.
# current_dir = os.path.dirname(os.path.abspath(__file__))
# src_dir = os.path.abspath(os.path.join(current_dir, '..'))
# sys.path.append(src_dir)

@pytest.fixture()
def test_client():
    flask_app = app

    # Create a test client using the Flask application configured for testing
    # The test client makes requests to the application without running a live server.
    with flask_app.test_client() as testing_client:
        yield testing_client  # this is where the testing happens!
