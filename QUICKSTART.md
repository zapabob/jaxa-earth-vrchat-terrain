# クイックスタートガイド

このガイドでは、JAXA Earth API MCP Serverを最短でセットアップして使用する方法を説明します。

## 5分で始める

### 1. 依存関係のインストール

```bash
cd jaxa-earth-mcp
uv sync
```

または：

```bash
uv add jaxa-earth --extra-index-url https://data.earth.jaxa.jp/api/python/repository/
uv add mcp
```

### 2. IDEの設定

#### Cursor IDE

プロジェクトルートの`.cursor/mcp.json`が自動認識されます。Cursor IDEを再起動するだけです。

#### Codex IDE

プロジェクトルートの`.codex/mcp.json`が自動認識されます。Codex IDEを再起動するだけです。

### 3. 動作確認

IDEを再起動後、以下のように試してください：

```
利用可能なJAXA Earth APIのコレクションを一覧表示してください
```

## 基本的な使用例

### コレクションの検索

```
地表面温度（LST）に関するコレクションを検索してください
```

### 画像の表示

```
2021年の関東地方（経度139-141度、緯度35-37度）の標高データの画像を表示してください
```

### 統計の計算

```
2021年の関東地方の標高データの空間統計を計算してください
```

## VRChat向けクイックスタート

### 1. 高度マップの生成

```
富士山周辺（経度138.5-139度、緯度35.2-35.5度）の高度マップを生成してください
```

### 2. Blender用エクスポート

```
富士山周辺の地形データをBlender用にエクスポートしてください
```

### 3. Unity用エクスポート

```
富士山周辺の地形データをUnity用にエクスポートしてください
```

詳細なワークフローは[WORKFLOW_VRCHAT_BLENDER.md](WORKFLOW_VRCHAT_BLENDER.md)を参照してください。

## トラブルシューティング

### MCPサーバーが認識されない

1. IDEを完全に再起動
2. 設定ファイルのパスを確認
3. `uv`コマンドが正しくインストールされているか確認

### 依存関係のエラー

```bash
uv sync
```

を実行して、依存関係を再インストールしてください。

## 次のステップ

- [README.md](README.md) - 詳細なドキュメント
- [WORKFLOW_VRCHAT_BLENDER.md](WORKFLOW_VRCHAT_BLENDER.md) - VRChat/Blenderワークフロー
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - プロジェクト構造
