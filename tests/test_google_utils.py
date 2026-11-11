import importlib
import importlib.util
import sys
import types
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


@pytest.fixture
def downloads(monkeypatch):
    stubbed = importlib.util.find_spec('torch') is None  # run without the heavy runtime dependency
    if stubbed:
        monkeypatch.setitem(sys.modules, 'torch', types.ModuleType('torch'))
        monkeypatch.delitem(sys.modules, 'utils.google_utils', raising=False)
    google_utils = importlib.import_module('utils.google_utils')
    urls = []
    monkeypatch.setattr(google_utils, 'safe_download', lambda file, url, **kwargs: urls.append(url))
    yield google_utils, urls
    if stubbed:
        sys.modules.pop('utils.google_utils', None)  # do not leak a module bound to the stub


def test_pretrained_weights_are_downloaded_from_v5_0_release(tmp_path, downloads):
    google_utils, urls = downloads
    google_utils.attempt_download(tmp_path / 'yolov5s.pt')
    assert urls == ['https://github.com/ultralytics/yolov5/releases/download/v5.0/yolov5s.pt']


def test_unknown_weights_are_not_downloaded(tmp_path, downloads):
    google_utils, urls = downloads
    google_utils.attempt_download(tmp_path / 'my_model.pt')
    assert urls == []
