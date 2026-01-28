#!/usr/bin/env python3
"""
MCPサーバー経由で気温データを取得するスクリプト
座標は環境変数または設定ファイルから読み込みます
"""

import asyncio
import json
import sys
import os
from pathlib import Path
from typing import List, Dict, Any
import subprocess

# 位置情報（環境変数または設定ファイルから読み込み）
def get_coordinates() -> tuple[float, float, float, float]:
    """座標を環境変数または設定ファイルから取得"""
    lat1 = os.getenv('POINT1_LAT')
    lon1 = os.getenv('POINT1_LON')
    lat2 = os.getenv('POINT2_LAT')
    lon2 = os.getenv('POINT2_LON')
    
    if all([lat1, lon1, lat2, lon2]):
        return float(lat1), float(lon1), float(lat2), float(lon2)
    
    config_file = Path("config/coordinates.json")
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return (
                config.get('point1', {}).get('lat', 0),
                config.get('point1', {}).get('lon', 0),
                config.get('point2', {}).get('lat', 0),
                config.get('point2', {}).get('lon', 0)
            )
    
    return 0.0, 0.0, 0.0, 0.0

# 2024年夏の期間
SUMMER_2024_START = "2024-06-01T00:00:00"
SUMMER_2024_END = "2024-08-31T23:59:59"

def calculate_bounding_box(lat1: float, lon1: float, lat2: float, lon2: float) -> List[float]:
    """2点を結ぶ円の直径として、バウンディングボックスを計算"""
    center_lat = (lat1 + lat2) / 2
    center_lon = (lon1 + lon2) / 2
    
    lat_diff = abs(lat1 - lat2)
    lon_diff = abs(lon1 - lon2)
    
    radius_lat = lat_diff * 0.6 * 1.2
    radius_lon = lon_diff * 0.6 * 1.2
    
    min_lat = center_lat - radius_lat
    max_lat = center_lat + radius_lat
    min_lon = center_lon - radius_lon
    max_lon = center_lon + radius_lon
    
    return [min_lon, min_lat, max_lon, max_lat]

def search_collections_mcp(keywords: List[str]) -> Dict[str, Any]:
    """MCPサーバー経由でコレクションを検索"""
    # 実際の実装では、MCPクライアントを使用
    # ここでは直接jaxa-earthを使用
    try:
        from jaxa.earth import je
        # コレクション検索のロジック
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def main():
    """メイン処理"""
    print("=" * 60)
    print("気温分布分析 (MCP経由)")
    print("=" * 60)
    
    # 座標を取得
    lat1, lon1, lat2, lon2 = get_coordinates()
    if lat1 == 0 and lon1 == 0 and lat2 == 0 and lon2 == 0:
        print("エラー: 座標が設定されていません。", file=sys.stderr)
        sys.exit(1)
    
    # バウンディングボックスを計算
    bbox = calculate_bounding_box(lat1, lon1, lat2, lon2)
    print(f"\nバウンディングボックス: {bbox}")
    
    # MCPサーバーのツールを使用してデータを取得
    # 実際の実装では、MCPクライアントライブラリを使用
    print("\nMCPサーバー経由でデータを取得中...")
    print("（実際の実装では、MCPクライアントを使用してツールを呼び出します）")
    
    # 分析スクリプトを実行
    print("\n分析スクリプトを実行中...")
    result = subprocess.run(
        [
            "uv", "run",
            "--with", "mcp",
            "--with", "jaxa-earth",
            "--extra-index-url", "https://data.earth.jaxa.jp/api/python/repository/",
            "--with", "matplotlib",
            "--with", "scipy",
            "python", "analyze_ueda_temperature.py"
        ],
        cwd=Path(__file__).parent,
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.stderr:
        print("エラー:", result.stderr, file=sys.stderr)

if __name__ == "__main__":
    main()
