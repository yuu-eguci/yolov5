yuu-eguci/yolov5
===

ultralytics/yolov5 をフォークしたリポジトリです。次の 2 つを自分で体験することを目的にしています。

- 自分の画像に物体検出の矩形 (バウンディングボックス) を描く
- データセットの画像にアノテーションファイルの矩形を重ねて、中身を確認する

コードは 2021 年 6 月時点の ultralytics/yolov5 (v5.0 系) をもとにしています。オリジナルの README は [README-original.md](README-original.md) にあります。

## セットアップ

```bash
git clone https://github.com/yuu-eguci/yolov5
cd yolov5
python3 -m pip install -r requirements.txt
```

Python 3.11 と、requirements.txt から入る最新の依存パッケージで、CPU での物体検出を確認しています。

Linux で GPU を使わない場合は、先に CPU 版の torch を入れるとダウンロード量を減らせます。

```bash
python3 -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

## 自分の画像を物体検出する

画像をフォルダ (例: `my_images/`) に置き、`--source` に指定します。

```bash
python3 detect.py --source my_images --weights yolov5s.pt --conf-thres 0.50
```

- 矩形を描いた画像は `runs/detect/exp/` に保存されます。2 回目以降は `exp2`, `exp3`, ... に保存されます。
- `--source` を省略すると、`data/images/` のサンプル画像 (bus.jpg, zidane.jpg) を検出します。
- 学習済みの重み `yolov5s.pt` が手元にない場合は、ultralytics/yolov5 の v5.0 リリースから自動でダウンロードします。このコードで読み込めるのは v5.0 の重みなので、最新リリースではなく v5.0 に固定しています。
- 重みのファイルは pickle 形式で、読み込むときに中のコードが実行されます。`--weights` には信頼できるファイルだけを指定してください。

### 結果の例

![README-image](https://user-images.githubusercontent.com/28250432/121980826-9bbd6a00-cdc7-11eb-9654-3a934e05af4c.png)

## データセットの画像とアノテーションを確認する

`view_labels.py` は YOLO 形式のラベルファイルを読み、画像に矩形とクラス名を描いて保存します。ラベルファイルは画像と同じ名前の `.txt` で、1 行に 1 つの矩形を `クラス番号 x_center y_center width height` (座標は 0〜1 に正規化した値) の形式で書いたものです。

COCO128 で確認する場合は、まずデータセットをリポジトリの 1 つ上の階層に展開します。

```bash
curl -L -O https://github.com/ultralytics/yolov5/releases/download/v1.0/coco128.zip
unzip -q coco128.zip -d ..
```

次のコマンドで、矩形を描いた画像を `runs/labels/` に保存します。

```bash
python3 view_labels.py --images ../coco128/images/train2017 --labels ../coco128/labels/train2017 --data data/coco128.yaml
```

- 保存先は `--output` で変更できます (既定値は `runs/labels`)。同じ名前のファイルは上書きします。
- クラス名は `--data` で指定した YAML の `names` から取ります (既定値は `data/coco128.yaml`)。`names` にないクラス番号は、番号のまま表示します。
- ラベルファイルがない画像は、矩形を描かずにそのまま保存します。

## テスト

```bash
python3 -m pip install pytest
python3 -m pytest tests
```

テストは小さな合成画像、一時ディレクトリ、ランダムな重みのモデルを使い、ネットワークにはアクセスしません。torch が入っていない環境では、torch が必要なテストをスキップします。

GitHub Actions (`.github/workflows/ci-testing.yml`) では、`yuu-eguci-dev` への push と pull request のたびに、ubuntu-latest と Python 3.11 の CPU 環境でテストを実行し、続けて v5.0 の `yolov5s.pt` で `data/images/` を物体検出します。
