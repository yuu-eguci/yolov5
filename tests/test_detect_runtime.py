import ast
import importlib
import re
import sys
from importlib import metadata
from pathlib import Path

import pytest

torch = pytest.importorskip('torch')  # these tests need requirements.txt installed

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from utils import general  # noqa: E402


def normalize(name):
    return re.sub(r'[-_.]+', '-', name).lower()


def module_level_imports(file):
    for node in ast.parse(file.read_text()).body:  # imports inside functions and try blocks are optional
        if isinstance(node, ast.Import):
            yield from (alias.name.split('.')[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0:
            yield node.module.split('.')[0]


def test_requirements_list_every_module_level_import():
    files = [*ROOT.glob('*.py'), *ROOT.glob('models/*.py'), *ROOT.glob('utils/*.py')]
    modules = {m for f in files for m in module_level_imports(f)} - set(sys.stdlib_module_names)
    modules -= {f.stem for f in ROOT.glob('*.py')} | {'models', 'utils'}  # local modules
    distributions = metadata.packages_distributions()
    required = {normalize(re.split(r'[<>=!~ #]', line)[0]) for line in (ROOT / 'requirements.txt').read_text().splitlines()
                if line.strip() and not line.startswith('#')}
    missing = {m for m in modules if not {normalize(d) for d in distributions.get(m, [m])} & required}
    assert not missing


def test_utils_general_imports_without_pkg_resources(monkeypatch):
    monkeypatch.setitem(sys.modules, 'pkg_resources', None)  # removed from setuptools>=81
    importlib.reload(general)


def test_check_requirements_reports_only_missing_packages(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(general, 'check_online', lambda: False)  # never pip install from tests
    file = tmp_path / 'requirements.txt'
    file.write_text('# comment\nnumpy>=1.0  # installed\nthop\nnot-installed-package>=1.0\n\ntorch>=999\n')
    general.check_requirements(file, exclude=('thop',))
    out = capsys.readouterr().out
    assert 'not-installed-package>=1.0 not found' in out
    assert 'torch>=999 not found' in out
    assert 'numpy' not in out and 'thop' not in out


def test_check_python_compares_versions():
    assert general.check_python('3.6.2')
    assert not general.check_python('99.0', required=False)


def test_detect_runs_with_v5_style_checkpoint(tmp_path):
    from detect import detect
    from models.yolo import Model

    weights = tmp_path / 'random.pt'
    torch.save({'model': Model(ROOT / 'models/yolov5s.yaml').half(), 'ema': None}, weights)  # same layout as v5.0
    detect(weights=str(weights), source=str(ROOT / 'data/images'), imgsz=64, device='cpu',
           project=str(tmp_path), name='exp')
    assert sorted(p.name for p in (tmp_path / 'exp').iterdir()) == ['bus.jpg', 'zidane.jpg']
