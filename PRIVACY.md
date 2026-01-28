# プライバシー保護について

## 個人情報の取り扱い

このプロジェクトでは、個人情報（住所、座標など）をGitHubに公開しないよう配慮しています。

## 座標の設定方法

気温分布分析スクリプトで使用する座標は、以下の方法で設定できます：

### 方法1: 環境変数

```bash
export POINT1_LAT=緯度1
export POINT1_LON=経度1
export POINT2_LAT=緯度2
export POINT2_LON=経度2
```

### 方法2: 設定ファイル

`config/coordinates.json`ファイルを作成して設定します：

```json
{
  "point1": {
    "lat": 緯度1,
    "lon": 経度1,
    "description": "First point"
  },
  "point2": {
    "lat": 緯度2,
    "lon": 経度2,
    "description": "Second point"
  }
}
```

**重要**: `config/coordinates.json`は`.gitignore`に追加されているため、GitHubにコミットされません。

## 既存のコミットから個人情報を削除する場合

既にGitHubに個人情報が含まれるコミットがある場合、以下の方法で削除できます：

1. **BFG Repo-Cleanerを使用**（推奨）
2. **git filter-branchを使用**
3. **新しいリポジトリを作成**

詳細は[GitHub公式ドキュメント](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)を参照してください。
