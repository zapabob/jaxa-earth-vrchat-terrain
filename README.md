# 🌍 JAXA Earth API → VRChat Terrain Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![MCP Server](https://img.shields.io/badge/MCP-Server-green.svg)](https://modelcontextprotocol.io/)

**JAXAの衛星データからVRChatワールドの地形を自動生成！** 🚀

JAXA Earth APIの地球観測データを、**Blender/Unity/VRChat**で使える3D地形に変換するMCPサーバーです。**Cursor IDE**と**Codex IDE**から自然言語で操作でき、リアルな地球の地形をVRChatワールドに取り込めます。

## ✨ 何ができる？

- 🛰️ **JAXAの衛星データを取得** - 標高、地表面温度、植生指数など様々なデータにアクセス
- 🎮 **VRChat向けに最適化** - ポリゴン数・テクスチャサイズを自動調整
- 🎨 **Blender/Unity対応** - ワンクリックでエクスポート、すぐに使える
- 💬 **自然言語で操作** - 「富士山周辺の地形をVRChat用にエクスポートして」と話すだけ
- 🔧 **Cursor/Codex対応** - お好みのIDEで利用可能

## 🎯 主な用途

- **VRChatワールド制作**: リアルな地球の地形をVRChatワールドに取り込む
- **Blenderプロジェクト**: 衛星データから3D地形を生成
- **Unityゲーム開発**: 実在する場所の地形をゲームに使用
- **データ分析**: 地球観測データの可視化と分析

## 🚀 クイックスタート

### 1. インストール（1分）

```bash
# リポジトリをクローン（YOUR_USERNAMEを実際のGitHubユーザー名に置き換え）
git clone https://github.com/YOUR_USERNAME/jaxa-earth-vrchat-terrain.git
cd jaxa-earth-vrchat-terrain

# 依存関係をインストール
uv sync
```

### 2. IDE設定（30秒）

Cursor/Codex IDEを再起動するだけ！設定ファイルは自動認識されます。

### 3. 使ってみる（10秒）

IDEで以下のように話しかけるだけ：

```
富士山周辺の地形をVRChat用にエクスポートして
```

**完了！** BlenderやUnityで使える地形データが生成されます。

詳細は[QUICKSTART.md](QUICKSTART.md)を参照してください。

## 📋 機能一覧

### 🛰️ データ取得
- **コレクション検索**: キーワードでデータセットを検索
- **画像取得**: 日付・範囲・解像度を指定して衛星画像を取得
- **統計計算**: 空間統計・時間統計を自動計算

### 🎮 VRChat/Blender/Unity向け
- **高度マップ生成**: 衛星データから16bit高度マップを生成
- **Blenderエクスポート**: Displace Modifierで使える形式
- **Unityエクスポート**: Terrain Toolで直接インポート可能
- **VRChat最適化**: ポリゴン数・テクスチャサイズを自動調整
- **テクスチャ生成**: Diffuse・Normalマップを自動生成

### 🔧 開発者向け
- **MCP Server**: Cursor/Codex IDEから自然言語で操作
- **公式v0.1.5準拠**: JAXA公式実装スタイルに完全準拠
- **非同期処理**: 高速なデータ処理
- **エラーハンドリング**: 分かりやすいエラーメッセージ

## 📦 インストール

### 前提条件

- Python 3.13以上
- [uv](https://github.com/astral-sh/uv) パッケージマネージャー（推奨）またはpip
- Cursor IDE または Codex IDE

### セットアップ

```bash
# リポジトリをクローン（YOUR_USERNAMEを実際のGitHubユーザー名に置き換え）
git clone https://github.com/YOUR_USERNAME/jaxa-earth-vrchat-terrain.git
cd jaxa-earth-vrchat-terrain

# 依存関係をインストール
uv sync
```

**uvがない場合**:

```bash
pip install mcp jaxa-earth numpy rasterio Pillow scipy requests
# jaxa-earthは以下のコマンドでインストール
pip install jaxa-earth --extra-index-url https://data.earth.jaxa.jp/api/python/repository/
```

## IDE設定

### Cursor IDE設定

#### 方法1: プロジェクト設定（推奨）

プロジェクトルートに`.cursor/mcp.json`ファイルが既に作成されています。Cursor IDEを再起動すると、自動的にMCPサーバーが認識されます。

### 方法2: グローバル設定

1. Cursor IDEを開く
2. **Settings > Features > MCP** に移動
3. **"+ Add New MCP Server"** をクリック
4. 以下の設定を追加：

```json
{
  "mcpServers": {
    "jaxa_api_tools": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\path\\to\\jaxa-earth-mcp",
        "run",
        "--with", "mcp",
        "--with", "jaxa-earth",
        "--extra-index-url", "https://data.earth.jaxa.jp/api/python/repository/",
        "mcp_server.py"
      ]
    }
  }
}
```

**注意**: MCPサーバーの名前は公式ドキュメントに合わせて`jaxa_api_tools`としていますが、任意の名前を使用できます。

**注意**: `C:\\path\\to\\jaxa-earth-mcp` を実際のプロジェクトパスに置き換えてください。

#### 動作確認

Cursor IDEを再起動後、Agentモードで以下のように確認できます：

```
利用可能なJAXA Earth APIのコレクションを一覧表示してください
```

### Codex IDE設定

#### 方法1: プロジェクト設定（推奨）

プロジェクトルートに`.codex/mcp.json`ファイルが既に作成されています。Codex IDEを再起動すると、自動的にMCPサーバーが認識されます。

#### 方法2: グローバル設定

1. Codex IDEを開く
2. **Settings > MCP** に移動
3. **"+ Add New MCP Server"** をクリック
4. 以下の設定を追加：

```json
{
  "mcpServers": {
    "jaxa_api_tools": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\path\\to\\jaxa-earth-mcp",
        "run",
        "--with", "mcp",
        "--with", "jaxa-earth",
        "--extra-index-url", "https://data.earth.jaxa.jp/api/python/repository/",
        "mcp_server.py"
      ]
    }
  }
}
```

**注意**: `C:\\path\\to\\jaxa-earth-mcp` を実際のプロジェクトパスに置き換えてください。

#### 動作確認

Codex IDEを再起動後、以下のように確認できます：

```
利用可能なJAXA Earth APIのコレクションを一覧表示してください
```

## 💡 使用例

### 基本的な使い方

IDEで自然言語で話しかけるだけ！

```
# コレクションを検索
地表面温度（LST）に関するコレクションを検索してください

# 画像を表示
2021年の関東地方の標高データの画像を表示してください

# 統計を計算
2021年の関東地方の標高データの空間統計を計算してください
```

### 🎮 VRChat向け（これがメイン機能！）

```
# 高度マップを生成
富士山周辺（経度138.5-139度、緯度35.2-35.5度）の高度マップを生成してください

# Blender用にエクスポート
富士山周辺の地形データをBlender用にエクスポートしてください

# Unity用にエクスポート
富士山周辺の地形データをUnity用にエクスポートしてください

# VRChat向けに最適化（推奨！）
富士山周辺の地形データをVRChat向けに最適化してエクスポートしてください。
最大ポリゴン数は50000、テクスチャサイズは2048にしてください
```

### 🌟 実用例

- **実在する場所のVRChatワールド**: 自分の住んでいる街、旅行先、好きな場所の地形をVRChatに
- **ゲーム開発**: 実在する山や谷をゲームの地形として使用
- **データ可視化**: 地球観測データを3Dで可視化

## 🎬 デモ・スクリーンショット

> **注意**: スクリーンショットを追加する場合は、`docs/images/`ディレクトリに配置してください。

### ワークフロー

詳細なステップバイステップガイドは[WORKFLOW_VRCHAT_BLENDER.md](WORKFLOW_VRCHAT_BLENDER.md)を参照してください。

#### 🎨 Blenderワークフロー（3ステップ）

1. **データ生成**: IDEで「地形をBlender用にエクスポートして」と話しかける
2. **Blenderでインポート**: Displace Modifierで高度マップを読み込む
3. **完成**: テクスチャを適用して完成！

#### 🎮 Unityワークフロー（2ステップ）

1. **データ生成**: IDEで「地形をUnity用にエクスポートして」と話しかける
2. **Unityでインポート**: Terrain Toolで.rawファイルを読み込む

**たったこれだけ！** 詳細は[WORKFLOW_VRCHAT_BLENDER.md](WORKFLOW_VRCHAT_BLENDER.md)を参照してください。

## 📊 利用可能なデータ

JAXA Earth APIから以下のようなデータを取得できます：

| データ種類 | コレクション例 | 用途 |
|---------|------------|------|
| 🏔️ **標高データ** | `JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global` | 地形生成、高度マップ |
| 🌡️ **地表面温度** | `JAXA.EORC_ALOS.LST_*` | 温度マップ、気候可視化 |
| 🌿 **植生指数** | `JAXA.EORC_ALOS.NDVI_*` | 植生マップ、環境分析 |
| 🌧️ **降水量** | `JAXA.EORC_ALOS.GSMaP_*` | 降雨マップ、気象分析 |
| 🌊 **海面水温** | `JAXA.EORC_ALOS.SST_*` | 海洋データ、水温マップ |

詳細はIDEで「利用可能なコレクションを一覧表示してください」と話しかけると確認できます。

## ❓ よくある質問（FAQ）

### Q: MCPサーバーが認識されない

**A**: IDEを完全に再起動してください。それでも認識されない場合は、`.cursor/mcp.json`または`.codex/mcp.json`のパスを確認してください。

### Q: データ取得に時間がかかる

**A**: 範囲を小さくするか、解像度を下げてください。VRChat向け最適化ツールを使用すると自動的に最適化されます。

### Q: メモリ不足エラーが出る

**A**: `create_vrchat_terrain`ツールを使用すると、自動的にメモリ使用量を最適化します。

### Q: Blenderで地形が平らに見える

**A**: Displace Modifierの**Strength**を増やしてください。通常は0.5〜2.0が適切です。

### Q: UnityでTerrainが正しくインポートされない

**A**: `terrain_metadata.json`の情報を確認し、**Byte Order**を**Windows**（リトルエンディアン）に設定してください。

詳細は[WORKFLOW_VRCHAT_BLENDER.md](WORKFLOW_VRCHAT_BLENDER.md)のトラブルシューティングセクションを参照してください。

## 📚 ドキュメント

- 🚀 [クイックスタート](QUICKSTART.md) - 5分で始める
- 🎬 [VRChat/Blenderワークフロー](WORKFLOW_VRCHAT_BLENDER.md) - 詳細な手順ガイド
- 📁 [プロジェクト構造](PROJECT_STRUCTURE.md) - ファイル構成の説明
- 🔧 [GitHubセットアップ](GITHUB_SETUP.md) - リポジトリ公開手順
- 🤝 [貢献ガイドライン](CONTRIBUTING.md) - コントリビューション方法

### 外部リンク

- [JAXA Earth API公式ドキュメント v0.1.5](https://data.earth.jaxa.jp/api/python/v0.1.5/en/)
- [MCP Server設定ガイド（公式）](https://data.earth.jaxa.jp/api/python/v0.1.5/en/mcpserver.html)
- [Zenn記事: JAXAが公開したMCPサーバーを触ってみる](https://zenn.dev/ra0kley/articles/cb2fc726f167da)

## 🤝 貢献

プルリクエストやIssueを歓迎します！

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add some amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを開く

詳細は[CONTRIBUTING.md](CONTRIBUTING.md)を参照してください。

## ⭐ スターをください！

このプロジェクトが役に立ったら、スターを押していただけると嬉しいです！

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)を参照してください。

**注意**: このプロジェクトはJAXA Earth APIを使用しています。JAXA Earth APIの利用規約に従ってください。
詳細は[JAXA Earth APIライセンス](https://data.earth.jaxa.jp/license/)を参照してください。

## 🗺️ ロードマップ

- [ ] EXR形式のサポート（Blender向け）
- [ ] LOD自動生成機能
- [ ] バッチ処理機能
- [ ] キャッシュ機能
- [ ] より高品質なNormalマップ生成

## 🙏 謝辞

- [JAXA第一宇宙技術部門](https://www.jaxa.jp/) - JAXA Earth APIの提供
- [Zenn記事](https://zenn.dev/ra0kley/articles/cb2fc726f167da) - インスピレーションと参考情報

## 📝 更新履歴

- **2026-01-28**: 🎉 初版リリース
  - JAXA公式v0.1.5準拠
  - Cursor/Codex IDE対応
  - VRChat/Blender/Unity向け3D地形生成機能
  - 詳細なワークフローガイド

---

<div align="center">

**⭐ このプロジェクトが役に立ったら、スターを押してください！ ⭐**

Made with ❤️ for VRChat creators and 3D artists

[![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/jaxa-earth-vrchat-terrain?style=social)](https://github.com/YOUR_USERNAME/jaxa-earth-vrchat-terrain)
[![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/jaxa-earth-vrchat-terrain?style=social)](https://github.com/YOUR_USERNAME/jaxa-earth-vrchat-terrain)

</div>
