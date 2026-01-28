# Git履歴から個人情報を削除する手順

既にGitHubにプッシュされたコミットに個人情報が含まれている場合、以下の手順で履歴から削除できます。

## ⚠️ 重要: 作業前の注意事項

- **バックアップを取る**: 作業前に必ずリポジトリをバックアップしてください
- **Force Pushが必要**: 履歴を書き換えるため、`git push --force`が必要です
- **他のコントリビューターへの影響**: 履歴を書き換えると、他の人がクローンしたリポジトリと不整合が生じます

## 方法1: git filter-repoを使用（推奨）

`git filter-repo`は`git filter-branch`の後継で、より安全で高速です。

### インストール

```bash
# pipでインストール
pip install git-filter-repo
```

### 実行手順

```bash
cd jaxa-earth-mcp

# 個人情報を含むファイルの履歴から座標を削除
git filter-repo --path analyze_ueda_temperature.py --invert-paths
git filter-repo --path get_ueda_temperature_analysis.py --invert-paths
git filter-repo --path get_ueda_temperature_mcp.py --invert-paths

# または、特定の文字列を置換（例）
# 実際の座標値や個人情報に置き換えてください
git filter-repo --replace-text <(echo "LATITUDE_VALUE_1==>0.0")
git filter-repo --replace-text <(echo "LATITUDE_VALUE_2==>0.0")
git filter-repo --replace-text <(echo "LONGITUDE_VALUE_1==>0.0")
git filter-repo --replace-text <(echo "LONGITUDE_VALUE_2==>0.0")
```

### プッシュ

```bash
git push --force --all
git push --force --tags
```

## 方法2: BFG Repo-Cleanerを使用

### 手順

1. **BFG Repo-Cleanerをダウンロード**
   - https://rtyley.github.io/bfg-repo-cleaner/ からダウンロード

2. **置換ファイルを作成**

`replacements.txt`を作成（例）:
```
LATITUDE_VALUE_1==>0.0
LATITUDE_VALUE_2==>0.0
LONGITUDE_VALUE_1==>0.0
LONGITUDE_VALUE_2==>0.0
LOCATION_NAME_1==>Location 1
LOCATION_NAME_2==>Location 2
FACILITY_NAME_1==>Point 1
FACILITY_NAME_2==>Point 2
```

**注意**: 上記は例です。実際の座標値や個人情報に置き換えてください。

3. **BFGを実行**

```bash
# リポジトリをミラークローン
git clone --mirror https://github.com/zapabob/jaxa-earth-vrchat-terrain.git

# BFGで置換
java -jar bfg.jar --replace-text replacements.txt jaxa-earth-vrchat-terrain.git

# クリーンアップ
cd jaxa-earth-vrchat-terrain.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# プッシュ
git push --force
```

## 方法3: 新しいブランチで上書き（最も安全）

履歴を書き換えずに、新しいコミットで上書きする方法:

```bash
# 現在のブランチをバックアップ
git branch backup-main

# 個人情報を削除した新しいコミットを作成
# （既に完了している）

# 新しいリポジトリを作成するか、既存のリポジトリをクリーンな状態にリセット
git checkout --orphan clean-main
git add .
git commit -m "Initial commit: JAXA Earth API MCP Server (personal information removed)"
git branch -D main
git branch -m main
git push --force origin main
```

## 削除対象の文字列

以下のような文字列がGit履歴に含まれている可能性があります：

- 座標値（緯度・経度）
- 住所情報
- 施設名や個人を特定できる情報
- その他の個人情報

**注意**: 実際の削除対象は、プロジェクトごとに異なります。上記は一般的な例です。

## 確認方法

履歴から個人情報が削除されたか確認:

```bash
# 特定の文字列を履歴から検索（例）
# 実際の座標値や個人情報に置き換えてください
git log --all --full-history -S "LATITUDE_VALUE" --source --all
git log --all --full-history -S "LOCATION_NAME" --source --all
```

結果が何も返ってこなければ、削除成功です。

## 参考リンク

- [GitHub: Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)
- [git-filter-repo](https://github.com/newren/git-filter-repo)
