"""Draw YOLO-format labels on dataset images to check the annotations.

Usage:
    $ python view_labels.py --images ../coco128/images/train2017 --labels ../coco128/labels/train2017
"""

import argparse
from pathlib import Path

import yaml
from PIL import Image, ImageDraw

IMG_FORMATS = ['bmp', 'jpg', 'jpeg', 'png', 'tif', 'tiff', 'webp']
COLORS = [(255, 56, 56), (72, 249, 10), (0, 194, 255), (255, 157, 151), (146, 204, 23), (52, 69, 147)]


def draw_labels(im, label_file, names):
    draw = ImageDraw.Draw(im)
    w, h = im.size
    for line in label_file.read_text().splitlines():
        if not line.strip():
            continue
        c, x, y, bw, bh = line.split()[:5]
        c = int(c)
        x, y, bw, bh = float(x) * w, float(y) * h, float(bw) * w, float(bh) * h
        box = [x - bw / 2, y - bh / 2, x + bw / 2, y + bh / 2]
        color = COLORS[c % len(COLORS)]
        name = names[c] if c < len(names) else str(c)
        draw.rectangle(box, outline=color, width=2)
        _, _, tw, th = draw.textbbox((0, 0), name)
        top = box[1] - th - 2 if box[1] >= th + 2 else box[1]  # name tag above the box, or inside at the image top
        tag = [box[0], top, box[0] + tw + 2, top + th + 2]
        draw.rectangle(tag, fill=color)
        draw.text((tag[0] + 1, tag[1] + 1), name, fill=(255, 255, 255))
    return im


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--images', required=True, help='directory of images')
    parser.add_argument('--labels', required=True, help='directory of YOLO-format *.txt labels')
    parser.add_argument('--data', default='data/coco128.yaml', help='dataset *.yaml with class names')
    parser.add_argument('--output', default='runs/labels', help='directory to save labeled images')
    opt = parser.parse_args(argv)

    names = yaml.safe_load(Path(opt.data).read_text())['names']
    output = Path(opt.output)
    output.mkdir(parents=True, exist_ok=True)
    images = sorted(p for p in Path(opt.images).iterdir() if p.suffix[1:].lower() in IMG_FORMATS)
    for image in images:
        im = Image.open(image).convert('RGB')
        label_file = Path(opt.labels) / f'{image.stem}.txt'
        if label_file.exists():
            draw_labels(im, label_file, names)
        im.save(output / image.name)
    print(f'{len(images)} images saved to {output}')


if __name__ == '__main__':
    main()
