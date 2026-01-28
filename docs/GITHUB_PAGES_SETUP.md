# GitHub Pages セットアップ手順

GitHub Pagesを有効化して、このサイトを公開する手順です。

## 手動設定（推奨）

1. GitHubリポジトリのページにアクセス: https://github.com/zapabob/jaxa-earth-vrchat-terrain
2. **Settings** タブをクリック
3. 左サイドバーから **Pages** を選択
4. **Source** セクションで以下を設定：
   - **Branch**: `main`
   - **Folder**: `/docs`
5. **Save** をクリック

数分後、以下のURLでサイトにアクセスできます：
- https://zapabob.github.io/jaxa-earth-vrchat-terrain/

## 自動設定（GitHub CLI）

以下のコマンドで自動設定することもできます：

```bash
gh api repos/zapabob/jaxa-earth-vrchat-terrain/pages \
  -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -d '{"source":{"branch":"main","path":"/docs"}}'
```

## 確認

設定後、数分待ってから以下のURLにアクセスしてください：
- https://zapabob.github.io/jaxa-earth-vrchat-terrain/

サイトが表示されれば成功です！
