import json
from unittest.mock import Mock

import httpx
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.config import settings
from app.db.models import VideoContentSummary
from app.services.gemini_service import GeminiError
from app.services.video_summary_service import summarize_video


def model_response(**overrides):
    result = dict(accessible=True, overview="Video overview", key_points=["Matchup"],
                  outlook="Speaker's outlook", tactics="Not discussed in this video")
    result.update(overrides)
    return httpx.Response(200, json={"candidates": [{"finishReason": "STOP", "content": {
        "parts": [{"text": json.dumps(result)}]}}]})


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "test-secret")
    client = Mock()
    client.post.return_value = model_response()
    return client


def test_video_attachment_and_source(client):
    result = summarize_video("abcdefghijk", client)
    request = client.post.call_args.kwargs["json"]
    assert request["contents"][0]["parts"][0] == {
        "file_data": {"file_uri": "https://www.youtube.com/watch?v=abcdefghijk"}}
    assert result["source"] == "video"
    assert "based_on_comments" not in result
    assert result["tactics"] == "Not discussed in this video"


def test_inaccessible_video_does_not_return_fabricated_summary(client):
    client.post.return_value = model_response(accessible=False)
    with pytest.raises(GeminiError):
        summarize_video("abcdefghijk", client)


@pytest.mark.parametrize("video_id", ["mock_001", "https://other.example/video", "short"])
def test_invalid_video_rejected_without_api_call(client, video_id):
    with pytest.raises(GeminiError):
        summarize_video(video_id, client)
    client.post.assert_not_called()


@pytest.mark.parametrize("status", [400, 401, 403, 429, 500])
def test_upstream_errors_hide_secrets(client, status):
    client.post.return_value = httpx.Response(status, text="test-secret")
    with pytest.raises(GeminiError) as exc:
        summarize_video("abcdefghijk", client)
    assert "test-secret" not in str(exc.value)


def test_malformed_result_rejected(client):
    client.post.return_value = model_response(key_points="not a list")
    with pytest.raises(GeminiError):
        summarize_video("abcdefghijk", client)


def test_cached_video_summary_persists_independently_of_comments(monkeypatch):
    from app.routers import analysis
    engine = create_engine("sqlite://")
    VideoContentSummary.__table__.create(engine)
    summary = {"source": "video", "overview": "Actual video content"}
    generate = Mock(return_value=summary)
    monkeypatch.setattr(analysis, "summarize_video", generate)
    with Session(engine) as db:
        assert analysis.get_video_summary("abcdefghijk", db) == summary
    with Session(engine) as db:
        assert analysis.get_video_summary("abcdefghijk", db) == summary
    generate.assert_called_once_with("abcdefghijk")
    engine.dispose()
