import os

import pytest

def test_home():
    url = URL

    r = SESSION.get(url)

    assert r.status_code == 200
