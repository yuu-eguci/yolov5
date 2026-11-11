import sys
import types
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
for name in ('torch', 'requests'):  # tests run without the heavy runtime dependencies
    try:
        __import__(name)
    except ImportError:
        sys.modules[name] = types.ModuleType(name)

from utils import google_utils  # noqa: E402


class LatestReleaseResponse:  # what the GitHub API returns today for releases/latest
    def json(self):
        return {'tag_name': 'v7.0', 'assets': [{'name': 'yolov5s.pt'}]}


@pytest.fixture
def downloads(monkeypatch):
    urls = []
    monkeypatch.setattr(google_utils, 'safe_download', lambda file, url, **kwargs: urls.append(url))
    monkeypatch.setattr(sys.modules['requests'], 'get', lambda *args, **kwargs: LatestReleaseResponse(), raising=False)
    return urls


def test_pretrained_weights_are_downloaded_from_v5_0_release(tmp_path, downloads):
    google_utils.attempt_download(tmp_path / 'yolov5s.pt')
    assert downloads == ['https://github.com/ultralytics/yolov5/releases/download/v5.0/yolov5s.pt']


def test_unknown_weights_are_not_downloaded(tmp_path, downloads):
    google_utils.attempt_download(tmp_path / 'my_model.pt')
    assert downloads == []
