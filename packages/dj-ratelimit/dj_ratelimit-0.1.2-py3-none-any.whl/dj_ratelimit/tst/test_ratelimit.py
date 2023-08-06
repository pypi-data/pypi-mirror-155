import datetime
from unittest.mock import patch

import freezegun
import pytest

from django.test import RequestFactory
from django.conf import settings
from rest_framework.response import Response

from dj_ratelimit.src.bucket import (
    Bucket,
    ratelimit,
)
from dj_ratelimit.src.redis_client import (
    RatelimitRedisClientFactory,
)

from dj_ratelimit.tst import settings_default

settings.configure(default_settings=settings_default)
pytestmark = pytest.mark.django_db

rf = RequestFactory()


class MockUser(object):
    def __init__(self, username="", organization_id="1234"):
        self.pk = 1
        self.username = username
        self.organization_id = organization_id
        self.is_authenticated = True


def _mock_request(username="", organization_id="1234", headers={}):
    req = rf.post("/")
    req.user = MockUser(username=username, organization_id=organization_id)
    req.headers = headers
    return req


def test_bucket_ratelimit_throws_when_full():
    username = "Fake Name"
    account_token = "fake-token-id"

    headers = {"X-Account-Token": account_token}

    client = RatelimitRedisClientFactory.get_client()
    # Test using existing bucket
    with patch.object(RatelimitRedisClientFactory, "get_client", return_value=client):
        new_bucket = Bucket(rate="1/m", burst_limit=2)

        @ratelimit(bucket=new_bucket)
        def view(cls, request):
            resp = Response()
            resp.status_code = 200
            return resp

        freezetime = datetime.datetime.now()
        with freezegun.freeze_time(freezetime):
            assert view(None, _mock_request(username=username, headers=headers)).status_code == 200
            assert view(None, _mock_request(username=username, headers=headers)).status_code == 200
            # Rate limited
            assert view(None, _mock_request(username=username, headers=headers)).status_code == 429

    client = RatelimitRedisClientFactory.get_client()
    # Test using rate and burst limit
    with patch.object(RatelimitRedisClientFactory, "get_client", return_value=client):

        @ratelimit(rate="1/m", burst_limit=2)
        def view(cls, request):
            resp = Response()
            resp.status_code = 200
            return resp

        freezetime = datetime.datetime.now()
        with freezegun.freeze_time(freezetime):
            assert view(None, _mock_request(username=username, headers=headers)).status_code == 200
            assert view(None, _mock_request(username=username, headers=headers)).status_code == 200
            # Rate limited
            assert view(None, _mock_request(username=username, headers=headers)).status_code == 429


def test_bucket_ratelimit_empties_high_limit():
    username = "Fake Name"
    account_token = "fake-token-id"

    headers = {"X-Account-Token": account_token}

    client = RatelimitRedisClientFactory.get_client()

    with patch.object(RatelimitRedisClientFactory, "get_client", return_value=client):

        @ratelimit(rate="10/m", burst_limit=20)
        def view(cls, request):
            resp = Response()
            resp.status_code = 200
            return resp

        # Fill bucket up to burst limit
        freezetime = datetime.datetime.now()
        with freezegun.freeze_time(freezetime):
            for _ in range(20):
                assert view(None, _mock_request(username=username, headers=headers)).status_code == 200
            # Rate limited
            assert view(None, _mock_request(username=username, headers=headers)).status_code == 429

        # Leak at 10 r/s
        unlock_rate_time = freezetime + datetime.timedelta(minutes=1)
        for i in range(10):
            with freezegun.freeze_time(unlock_rate_time + datetime.timedelta(milliseconds=1000 * i / 10)):
                assert view(None, _mock_request(username=username, headers=headers)).status_code == 200
        with freezegun.freeze_time(unlock_rate_time + datetime.timedelta(milliseconds=1000 * 9/10)):
            # Rate limited
            assert view(None, _mock_request(username=username, headers=headers)).status_code == 429


def test_bucket_ratelimit_empties_after_ttl():
    username = "Fake Name"
    account_token = "fake-token-id"

    headers = {"X-Account-Token": account_token}

    client = RatelimitRedisClientFactory.get_client()

    with patch.object(RatelimitRedisClientFactory, "get_client", return_value=client):

        @ratelimit(rate="10/m", burst_limit=20)
        def view(cls, request):
            resp = Response()
            resp.status_code = 200
            return resp

        # Fill bucket up to burst limit
        freezetime = datetime.datetime.now()
        with freezegun.freeze_time(freezetime):
            for _ in range(20):
                assert view(None, _mock_request(username=username, headers=headers)).status_code == 200

        # Wait for ttl, assert we can burst again
        unlock_rate_time = freezetime + datetime.timedelta(minutes=2)
        with freezegun.freeze_time(unlock_rate_time):
            for _ in range(20):
                assert view(None, _mock_request(username=username, headers=headers)).status_code == 200
            # Rate limited
            assert view(None, _mock_request(username=username, headers=headers)).status_code == 429
