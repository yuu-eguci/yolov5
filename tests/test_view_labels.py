import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import view_labels  # noqa: E402

WHITE = (255, 255, 255)


def run(tmp_path, labels_by_image, names=('cat',)):
    images, labels, output = tmp_path / 'images', tmp_path / 'labels', tmp_path / 'output'
    images.mkdir(exist_ok=True)
    labels.mkdir()
    for stem, text in labels_by_image.items():
        Image.new('RGB', (100, 80), WHITE).save(images / f'{stem}.png')
        if text is not None:
            (labels / f'{stem}.txt').write_text(text)
    data = tmp_path / 'data.yaml'
    data.write_text(f'names: {list(names)}\n')
    view_labels.main(['--images', str(images), '--labels', str(labels), '--data', str(data), '--output', str(output)])
    return output


def test_draws_box_from_yolo_label(tmp_path):
    output = run(tmp_path, {'a': '0 0.5 0.5 0.5 0.5\n'})  # box (25, 20) - (75, 60)
    im = Image.open(output / 'a.png')
    assert im.getpixel((50, 60)) != WHITE  # bottom edge
    assert im.getpixel((75, 40)) != WHITE  # right edge
    assert im.getpixel((50, 40)) == WHITE  # inside
    assert im.getpixel((5, 75)) == WHITE  # outside


def test_class_id_outside_names_is_still_drawn(tmp_path):
    output = run(tmp_path, {'a': '5 0.5 0.5 0.5 0.5\n'})
    assert Image.open(output / 'a.png').getpixel((50, 60)) != WHITE


def test_image_without_label_file_is_saved_unchanged(tmp_path):
    output = run(tmp_path, {'b': None})
    assert Image.open(output / 'b.png').convert('RGB').getextrema() == ((255, 255),) * 3


def test_non_image_files_are_ignored(tmp_path):
    (tmp_path / 'images').mkdir()
    (tmp_path / 'images' / '.DS_Store').write_text('not an image')
    output = run(tmp_path, {'a': None})
    assert sorted(p.name for p in output.iterdir()) == ['a.png']


def test_name_tag_stays_inside_image_for_box_at_top_edge(tmp_path):
    output = run(tmp_path, {'a': '0 0.25 0.25 0.5 0.5\n'})  # box (0, 0) - (50, 40)
    assert Image.open(output / 'a.png').getpixel((3, 6)) != WHITE  # name tag drawn below the top edge
