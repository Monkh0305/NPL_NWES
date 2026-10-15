from unittest.mock import Mock

import httpx
import pytest

from app.services.gemini_transport import post_with_retry


@pytest.mark.parametrize('status', [500, 502, 503, 504])
def test_transient_failure_recovers(monkeypatch, status):
    sleep = Mock()
    monkeypatch.setattr('app.services.gemini_transport.time.sleep', sleep)
    client = Mock()
    client.post.side_effect = [httpx.Response(status), httpx.Response(200)]
    result = post_with_retry('https://example.test', headers={}, json={}, timeout=90, client=client)
    assert result.status_code == 200
    assert client.post.call_count == 2
    sleep.assert_called_once_with(1)


def test_retries_stop_after_three_attempts(monkeypatch):
    sleep = Mock()
    monkeypatch.setattr('app.services.gemini_transport.time.sleep', sleep)
    client = Mock()
    client.post.return_value = httpx.Response(503)
    assert post_with_retry('https://example.test', headers={}, json={}, timeout=90, client=client).status_code == 503
    assert client.post.call_count == 3
    assert [call.args[0] for call in sleep.call_args_list] == [1, 2]


@pytest.mark.parametrize('status', [400, 401, 403, 404, 429])
def test_permanent_and_quota_errors_not_retried(status):
    client = Mock()
    client.post.return_value = httpx.Response(status)
    assert post_with_retry('https://example.test', headers={}, json={}, timeout=90, client=client).status_code == status
    assert client.post.call_count == 1


def test_no_retry_when_time_budget_exhausted(monkeypatch):
    monkeypatch.setattr('app.services.gemini_transport.time.monotonic', Mock(side_effect=[0, 0, 89.5]))
    sleep = Mock()
    monkeypatch.setattr('app.services.gemini_transport.time.sleep', sleep)
    client = Mock()
    client.post.return_value = httpx.Response(503)
    post_with_retry('https://example.test', headers={}, json={}, timeout=90, client=client)
    assert client.post.call_count == 1
    sleep.assert_not_called()
