# プロジェクト構造

```
jaxa-earth-mcp/
├── .cursor/                    # Cursor IDE設定
│   └── mcp.json               # MCPサーバー設定
├── .codex/                     # Codex IDE設定
│   └── mcp.json               # MCPサーバー設定
├── .github/                    # GitHub設定
│   ├── workflows/              # GitHub Actions
│   │   └── ci.yml             # CI/CD設定
│   └── ISSUE_TEMPLATE/        # Issueテンプレート
│       ├── bug_report.md
│       └── feature_request.md
├── examples/                   # サンプルと例
│   └── README.md
├── mcp_server.py              # メインのMCPサーバーファイル
├── pyproject.toml             # プロジェクト設定と依存関係
├── README.md                  # メインのREADME
├── LICENSE                    # MITライセンス
├── CONTRIBUTING.md            # 貢献ガイドライン
├── WORKFLOW_VRCHAT_BLENDER.md # VRChat/Blenderワークフローガイド
├── GITHUB_SETUP.md            # GitHubセットアップガイド
├── PROJECT_STRUCTURE.md       # このファイル
└── .gitignore                 # Git除外設定
```

## 主要ファイルの説明

### mcp_server.py

メインのMCPサーバーファイル。以下の機能を提供：

- **公式v0.1.5準拠のツール**:
  - `search_collections_id`: コレクション情報取得
  - `show_images`: 衛星画像表示
  - `calc_spatial_stats`: 空間統計計算
  - `show_spatial_stats`: 空間統計結果画像表示

- **追加ツール**:
  - `search_collections`: キーワード検索
  - `list_available_collections`: コレクション一覧
  - `get_earth_images`: 詳細な画像取得
  - `calc_temporal_stats`: 時間統計
  - `read_geojson`, `select_features`: GeoJSON処理
  - `generate_heightmap`: 高度マップ生成
  - `export_to_blender`: Blender用エクスポート
  - `export_to_unity`: Unity用エクスポート
  - `create_vrchat_terrain`: VRChat向け最適化
  - `export_texture_maps`: テクスチャマップエクスポート

### pyproject.toml

プロジェクトの設定と依存関係を定義：

- プロジェクトメタデータ
- 依存関係（mcp, jaxa-earth, numpy, rasterio, Pillow, scipy, requests）
- JAXA Earth APIリポジトリの設定
- 開発用依存関係

### README.md

プロジェクトの概要、インストール手順、使用方法を説明。

### WORKFLOW_VRCHAT_BLENDER.md

VRChat/Blender向けの詳細なワークフローガイド：

- Blenderワークフロー（ステップバイステップ）
- Unityワークフロー（ステップバイステップ）
- VRChatへのアップロード手順
- トラブルシューティング

### GITHUB_SETUP.md

GitHubリポジトリとして公開する手順を説明。

### CONTRIBUTING.md

プロジェクトへの貢献方法を説明。

## IDE設定ファイル

### .cursor/mcp.json

Cursor IDE用のMCPサーバー設定。プロジェクトルートに配置することで自動認識。

### .codex/mcp.json

Codex IDE用のMCPサーバー設定。プロジェクトルートに配置することで自動認識。

## 出力ディレクトリ

生成されたファイルは以下のディレクトリに保存されます（デフォルト: `./temp/`）：

- `temp/heightmap.png`: 高度マップ
- `temp/blender_export/`: Blender用エクスポート
- `temp/unity_export/`: Unity用エクスポート
- `temp/vrchat_terrain/`: VRChat向け最適化データ
- `temp/texture_maps/`: テクスチャマップ

**注意**: `temp/`ディレクトリは`.gitignore`で除外されています。
