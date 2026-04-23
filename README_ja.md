# Pokemon Champions OBS Overlay

「ポケモンチャンピオンズ」のライブ配信向けOBSオーバーレイツールです。  
選出画面でホットキーを押すだけで、対戦相手のプレイヤー名とポケモン6匹をOBS画面に自動反映します。

[English version here](README.md)

## 機能

- 対戦相手のプレイヤー名をOCRで読み取り、テキストとしてOBSに反映
- 対戦相手のポケモン6匹を個別にキャプチャし、横並びに合成してOBSに反映
- ホットキー1発でキャプチャ実行・クリア

## 必要環境

- Windows
- OBS Studio 30.0.0以上（WebSocket機能有効）
- Python 3.12以上
- キャプチャーボード

## インストール

```bash
pip install -r requirements.txt
```

### 依存ライブラリ

| パッケージ | 用途 |
|---|---|
| `obsws-python` | OBS WebSocket通信 |
| `opencv-python` | キャプチャーボードの映像取得・画像処理 |
| `numpy` | 画像データの配列操作 |
| `Pillow` | 透過PNG画像の生成 |
| `keyboard` | グローバルホットキーの検出 |
| `python-dotenv` | `.env`ファイルからOBSパスワードを読み込み |
| `easyocr` | 対戦相手のトレーナー名OCR（日英中韓対応） |

## セットアップ

### 1. OBSの設定

- WebSocketサーバーを有効化：ツール → WebSocketサーバー設定（ポート: 4455）
- 以下のソースを作成してください（名前は完全一致が必要）：
  - `pokecham_auto-name` — **テキスト (GDI+)** ソース（対戦相手のプレイヤー名用）
  - `pokecham_auto-poke` — **画像**ソース（対戦相手のポケモン一覧用）

### 2. キャプチャーボードのデバイスIDを確認

以下を実行して、使用可能なカメラデバイスの一覧を表示します：

```bash
python find_camera.py
```

ゲーム映像が映っているデバイス番号を確認し、`config.py` の `DEVICE_ID` に設定してください。

正しいデバイスが選択されているか確認するには：

```bash
python check_camera.py
```

### 3. 環境変数の設定

`.env.example` をコピーして `.env` を作成し、OBS WebSocketのパスワードを入力してください：

```
OBS_PASSWORD=your_password_here
```

接続確認は以下で行えます：

```bash
python test_connection.py
```

### 4. 座標の調整

> **注意：** キャプチャーボードの出力が1080pであれば、デフォルトの座標のままで動作します。不用意に変更するとズレが生じる原因になるため、基本的にはそのままにしておくことを推奨します。

`config.py` の座標は、キャプチャ解像度が1080p以外の場合のみ調整してください。

```python
DEVICE_ID = 5               # キャプチャーボードのデバイスID

NAME_REGION = (1563, 95, 1845, 141)   # プレイヤー名エリア (x1, y1, x2, y2)
POKEMON_REGIONS = [                    # ポケモン6枠
    (1603, 156, 1844, 264),
    ...
]
```

`coord_picker.py` を使うと、ライブ映像上でクリックして座標を視覚的に確認できます：

```bash
python coord_picker.py
```

1クリック目で左上、2クリック目で右下を指定すると領域が確定し、座標がコンソールに表示されます。  
その値を `config.py` にコピーしてください。

## 使い方

`start_overlay.bat` をダブルクリックして起動します。

> **注意：** 初回起動時にEasyOCRのモデルが自動ダウンロードされます（約100MB）。2回目以降は不要です。モデルの読み込みに数秒かかる場合があります。

| ホットキー | 動作 |
|---|---|
| `F9` | 現在のフレームをキャプチャしてOBSに反映 |
| `F10` | OBSの表示をクリア |
| `Esc` | ツールを終了 |

## 使用例

### Step 1 — 選出画面で `F9` を押す

対戦相手の選出画面が表示されたら、`F9` を押して相手のトレーナー名とポケモン一覧をキャプチャします。

![選出画面の例](images/ex_select.png)

> 画面右側に相手のポケモン6体が表示されているタイミングで押してください。

### Step 2 — OBSに相手情報が反映される

キャプチャしたデータが即座にOBSに送られ、配信画面にオーバーレイ表示されます。

![OBS配信UIの例](images/ex_obs_uisample.png)

> 右上に相手のポケモン6体、左上に相手のトレーナー名が表示されます（画像はプライバシー保護のため加工済み）。  
> OBS上でのレイアウト（位置・サイズ）はご自身の配信スタイルに合わせて自由に調整してください。

### Step 3 — 対戦終了後に `F10` でクリア

試合が終わったら `F10` を押してOBSのオーバーレイを消去します。

## ファイル構成

```
PokemonChampions-obs-overlay/
├── overlay.py          # メインスクリプト
├── config.py           # 座標・設定
├── requirements.txt    # Pythonライブラリ一覧
├── start_overlay.bat   # 起動用バッチファイル
├── .env.example        # .envのテンプレート
├── find_camera.py      # キャプチャーボードのデバイスID確認ツール
├── check_camera.py     # カメラ映像のプレビューツール
├── coord_picker.py     # 座標確認ツール
└── test_connection.py  # OBS WebSocket接続テストツール
```

## 注意事項

- `.env` ファイルは絶対にGitにコミットしないでください（OBSパスワードが含まれます）
- 座標はご自身の画面環境に合わせて必ず調整してください
- OBSを起動した状態でツールを実行してください
