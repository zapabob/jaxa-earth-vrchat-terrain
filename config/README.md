# 設定ファイル

## coordinates.json

気温分布分析スクリプトで使用する座標を設定します。

### 設定方法

1. `coordinates.json.example`をコピーして`coordinates.json`を作成
2. 2点の座標を設定

```json
{
  "point1": {
    "lat": 0.0,
    "lon": 0.0,
    "description": "First point coordinates"
  },
  "point2": {
    "lat": 0.0,
    "lon": 0.0,
    "description": "Second point coordinates"
  }
}
```

### 環境変数での設定

環境変数でも設定できます：

```bash
export POINT1_LAT=0.0
export POINT1_LON=0.0
export POINT2_LAT=0.0
export POINT2_LON=0.0
```

### 注意

- `coordinates.json`は`.gitignore`に追加されています
- 個人情報を含むため、GitHubにコミットしないでください
