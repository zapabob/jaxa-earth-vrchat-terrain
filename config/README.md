# 設定ファイル

## coordinates.json

気温分布分析スクリプトで使用する座標を設定します。

### 設定方法

1. `coordinates.json.example`をコピーして`coordinates.json`を作成
2. 2点の座標を設定

```json
{
  "point1": {
    "lat": 36.38916397,
    "lon": 138.23623657,
    "description": "First point"
  },
  "point2": {
    "lat": 36.392,
    "lon": 138.258,
    "description": "Second point"
  }
}
```

### 環境変数での設定

環境変数でも設定できます：

```bash
export POINT1_LAT=36.38916397
export POINT1_LON=138.23623657
export POINT2_LAT=36.392
export POINT2_LON=138.258
```

### 注意

- `coordinates.json`は`.gitignore`に追加されています
- 個人情報を含むため、GitHubにコミットしないでください
