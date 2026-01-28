# GitHubリポジトリセットアップガイド

このガイドでは、このプロジェクトをGitHubリポジトリとして公開する手順を説明します。

## 前提条件

- Gitがインストールされていること
- GitHubアカウントを持っていること

## セットアップ手順

### 1. リポジトリの初期化

```bash
cd jaxa-earth-mcp
git init
```

### 2. ファイルの追加

```bash
git add .
```

### 3. 初回コミット

```bash
git commit -m "Initial commit: JAXA Earth API MCP Server with VRChat/Blender support"
```

### 4. GitHubでリポジトリを作成

1. GitHubにログイン
2. 新しいリポジトリを作成
3. **リポジトリ名を設定**（推奨: `jaxa-earth-vrchat-terrain`）
   - 詳細は[REPOSITORY_NAME.md](REPOSITORY_NAME.md)を参照
4. **説明を追加**:
   ```
   Transform JAXA satellite data into VRChat worlds! Generate 3D terrain from Earth observation data for Blender/Unity/VRChat. Works with Cursor/Codex IDE.
   ```
   または日本語:
   ```
   JAXAの衛星データからVRChatワールドの地形を自動生成！Blender/Unity/VRChatで使える3D地形を生成するMCPサーバー
   ```
5. **Public**を選択（個人公開として）
6. **Topics（タグ）を追加**:
   - `jaxa`, `earth-api`, `satellite-data`, `vrchat`, `blender`, `unity`, `terrain-generation`, `mcp`, `mcp-server`, `cursor-ide`, `codex-ide`, `python`, `3d-modeling`, `gis`, `geospatial`
7. **README、.gitignore、LICENSEは追加しない**（既にプロジェクトに含まれています）

### 5. リモートリポジトリの追加

```bash
git remote add origin https://github.com/YOUR_USERNAME/jaxa-earth-vrchat-terrain.git
```

**注意**: `YOUR_USERNAME`を実際のGitHubユーザー名に置き換え、リポジトリ名も選択した名前に合わせてください。

**注意**: `YOUR_USERNAME`を実際のGitHubユーザー名に置き換えてください。

### 6. ブランチ名の設定（オプション）

```bash
git branch -M main
```

### 7. プッシュ

```bash
git push -u origin main
```

## リポジトリの設定

### GitHubリポジトリの設定

1. **Settings** → **General** → **Features**
   - **Issues**: 有効化
   - **Discussions**: 必要に応じて有効化
   - **Wiki**: 必要に応じて有効化

2. **Settings** → **Pages**（オプション）
   - GitHub Pagesを有効化してドキュメントを公開

3. **Settings** → **Actions** → **General**
   - Actions permissionsを設定

### Topics（タグ）の追加

リポジトリのトップページで、以下のトピックを追加することを推奨：

- `jaxa`
- `earth-api`
- `mcp`
- `mcp-server`
- `satellite-data`
- `vrchat`
- `blender`
- `unity`
- `terrain-generation`
- `cursor-ide`
- `codex-ide`
- `python`

## リリースの作成

### 初回リリース

1. **Releases** → **Create a new release**
2. **Tag version**: `v0.1.0`
3. **Release title**: `v0.1.0 - Initial Release`
4. **Description**:

```markdown
## 初回リリース

JAXA Earth API MCP Serverの初回リリースです。

### 主な機能

- JAXA公式v0.1.5実装準拠
- Cursor IDEとCodex IDE対応
- VRChat/Blender向け3D地形生成機能
- 包括的なデータ検索・取得・処理機能

### ドキュメント

- [README.md](README.md)
- [WORKFLOW_VRCHAT_BLENDER.md](WORKFLOW_VRCHAT_BLENDER.md)
```

5. **Publish release**をクリック

## 継続的な開発

### ブランチ戦略

- `main`: 安定版
- `develop`: 開発版
- `feature/*`: 新機能
- `fix/*`: バグ修正

### コミットメッセージ

以下の形式を推奨：

```
[種類] 簡潔な説明

詳細な説明（オプション）
```

種類:
- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメント
- `style`: コードスタイル
- `refactor`: リファクタリング
- `test`: テスト
- `chore`: その他

## 参考資料

- [GitHub公式ドキュメント](https://docs.github.com/)
- [Git公式ドキュメント](https://git-scm.com/doc)
