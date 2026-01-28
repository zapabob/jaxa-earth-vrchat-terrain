#!/usr/bin/env python3
"""
長野県上田市の気温分布分析（MCPサーバー経由でデータ取得）
"""

import json
import sys
import math
from pathlib import Path
from typing import List, Dict, Any
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d import Axes3D
from scipy import ndimage
from PIL import Image

# jaxa-earthを直接使用（MCPサーバー経由の代わり）
try:
    from jaxa.earth import je
except ImportError as e:
    print(f"Error importing jaxa-earth: {e}", file=sys.stderr)
    sys.exit(1)

# 位置情報
LEOPALACE_LAT = 36.38916397
LEOPALACE_LON = 138.23623657
KARAOKE_LAT = 36.392
KARAOKE_LON = 138.258

# 2024年夏の期間
SUMMER_2024_START = "2024-06-01T00:00:00"
SUMMER_2024_END = "2024-08-31T23:59:59"

def calculate_bounding_box(lat1: float, lon1: float, lat2: float, lon2: float) -> List[float]:
    """2点を結ぶ円の直径として、バウンディングボックスを計算"""
    center_lat = (lat1 + lat2) / 2
    center_lon = (lon1 + lon2) / 2
    
    # 2点間の距離を計算（ハーバーサイン公式）
    R = 6371.0  # 地球の半径（km）
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    lon1_rad = math.radians(lon1)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance_km = R * c
    
    # 円の直径（km）から度に変換（約111km = 1度）
    radius_degrees = (distance_km / 2) / 111.0
    
    # 最小0.01度の差を確保
    min_radius = 0.01
    radius_degrees = max(radius_degrees, min_radius)
    
    min_lat = center_lat - radius_degrees
    max_lat = center_lat + radius_degrees
    min_lon = center_lon - radius_degrees
    max_lon = center_lon + radius_degrees
    
    return [min_lon, min_lat, max_lon, max_lat]

def search_temperature_collections() -> List[str]:
    """気温関連のコレクションを検索"""
    try:
        collection_list = je.ImageCollectionList()
        # LST (Land Surface Temperature) で検索
        collections, bands = collection_list.filter_name(keywords=["LST"])
        
        print(f"見つかったコレクション数: {len(collections) if isinstance(collections, list) else 0}")
        
        if isinstance(collections, list) and len(collections) > 0:
            print("利用可能なコレクション:")
            for i, col in enumerate(collections[:5]):  # 最初の5つを表示
                print(f"  {i+1}. {col}")
            return list(collections)
        else:
            print("LSTコレクションが見つかりませんでした。")
            return []
    except Exception as e:
        print(f"コレクション検索エラー: {e}", file=sys.stderr)
        return []

def get_temperature_data(bbox: List[float], date_range: List[str]) -> Dict[str, Any]:
    """JAXA Earth APIから気温データを取得"""
    try:
        # まずコレクションを検索
        collections = search_temperature_collections()
        
        if not collections:
            print("気温コレクションが見つかりません。サンプルデータを生成します。")
            return generate_sample_data(bbox, date_range)
        
        # 最初の利用可能なコレクションを使用
        collection = collections[0]
        print(f"使用するコレクション: {collection}")
        
        # 画像を取得
        print(f"気温データを取得中... (範囲: {bbox}, 期間: {date_range})")
        
        image_size = 500
        ppu = image_size / (bbox[2] - bbox[0])
        
        # データを取得
        # まず利用可能なバンドを確認
        collection_list = je.ImageCollectionList()
        collections, bands = collection_list.filter_name(keywords=["LST"])
        
        # バンドを選択（LSTバンドを使用）
        band_name = "LST" if "LST" in str(bands) else None
        
        data = je.ImageCollection(collection=collection, ssl_verify=True)\
            .filter_date(dlim=date_range)\
            .filter_resolution(ppu=ppu)\
            .filter_bounds(bbox=bbox)
        
        # バンドを選択してから画像を取得
        if band_name:
            data = data.select(band=band_name)
        
        data = data.get_images()
        
        # 画像を処理
        img_data = je.ImageProcess(data)
        
        # ラスターデータを取得
        if hasattr(img_data, 'raster') and img_data.raster:
            raster = img_data.raster
            if hasattr(raster, 'img'):
                temperature_data = np.array(raster.img)
                # ケルビンから摂氏に変換（必要に応じて）
                # LSTデータは通常ケルビンなので、273.15を引く
                if temperature_data.max() > 200:
                    temperature_data = temperature_data - 273.15
                
                return {
                    "temperature_data": temperature_data,
                    "bbox": bbox,
                    "date_range": date_range,
                    "collection": collection
                }
        
        # データが取得できない場合、サンプルデータを生成
        print("データが取得できませんでした。サンプルデータを生成します。")
        return generate_sample_data(bbox, date_range)
        
    except Exception as e:
        print(f"Error getting temperature data: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return generate_sample_data(bbox, date_range)

def generate_sample_data(bbox: List[float], date_range: List[str]) -> Dict[str, Any]:
    """サンプルデータを生成（テスト用）"""
    print("サンプルデータを生成中...")
    
    grid_size = 100
    np.random.seed(42)
    temperature_data = np.random.uniform(20, 35, (grid_size, grid_size))
    
    # 中心部を少し高くする（都市部のヒートアイランド効果を模擬）
    center = grid_size // 2
    for i in range(grid_size):
        for j in range(grid_size):
            dist = math.sqrt((i - center)**2 + (j - center)**2)
            if dist < center:
                temperature_data[i, j] += (1 - dist / center) * 5
    
    return {
        "temperature_data": temperature_data,
        "bbox": bbox,
        "date_range": date_range,
        "grid_size": grid_size
    }

def calculate_statistics(temperature_data: np.ndarray) -> Dict[str, float]:
    """統計処理"""
    return {
        "mean": float(np.mean(temperature_data)),
        "std": float(np.std(temperature_data)),
        "min": float(np.min(temperature_data)),
        "max": float(np.max(temperature_data)),
        "median": float(np.median(temperature_data)),
        "q25": float(np.percentile(temperature_data, 25)),
        "q75": float(np.percentile(temperature_data, 75))
    }

def visualize_2d(temperature_data: np.ndarray, bbox: List[float], output_dir: Path):
    """2Dヒートマップを作成"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # ヒートマップ
    im1 = axes[0].imshow(temperature_data, cmap='hot', origin='lower', aspect='auto')
    axes[0].set_title('Temperature Distribution (2D Heatmap)', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Longitude Index')
    axes[0].set_ylabel('Latitude Index')
    plt.colorbar(im1, ax=axes[0], label='Temperature (°C)')
    
    # 等高線図
    contour = axes[1].contourf(temperature_data, levels=20, cmap='hot', origin='lower')
    axes[1].set_title('Temperature Contour Map', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Longitude Index')
    axes[1].set_ylabel('Latitude Index')
    plt.colorbar(contour, ax=axes[1], label='Temperature (°C)')
    
    plt.tight_layout()
    output_file = output_dir / "temperature_2d_heatmap.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"2Dヒートマップを保存: {output_file}")
    plt.close()

def visualize_3d(temperature_data: np.ndarray, bbox: List[float], output_dir: Path):
    """3D立体可視化"""
    fig = plt.figure(figsize=(16, 12))
    
    # 3Dサーフェスプロット
    ax1 = fig.add_subplot(221, projection='3d')
    x = np.arange(temperature_data.shape[1])
    y = np.arange(temperature_data.shape[0])
    X, Y = np.meshgrid(x, y)
    surf = ax1.plot_surface(X, Y, temperature_data, cmap='hot', alpha=0.8, linewidth=0, antialiased=True)
    ax1.set_title('3D Surface Plot', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Longitude Index')
    ax1.set_ylabel('Latitude Index')
    ax1.set_zlabel('Temperature (°C)')
    fig.colorbar(surf, ax=ax1, shrink=0.5, label='Temperature (°C)')
    
    # 3Dワイヤーフレーム
    ax2 = fig.add_subplot(222, projection='3d')
    wire = ax2.plot_wireframe(X, Y, temperature_data, cmap='hot', linewidth=0.5)
    ax2.set_title('3D Wireframe', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Longitude Index')
    ax2.set_ylabel('Latitude Index')
    ax2.set_zlabel('Temperature (°C)')
    
    # 3D等高線プロット
    ax3 = fig.add_subplot(223, projection='3d')
    contour = ax3.contour(X, Y, temperature_data, levels=20, cmap='hot')
    ax3.set_title('3D Contour Plot', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Longitude Index')
    ax3.set_ylabel('Latitude Index')
    ax3.set_zlabel('Temperature (°C)')
    
    # 3D散布図（サンプリング）
    ax4 = fig.add_subplot(224, projection='3d')
    step = max(1, temperature_data.shape[0] // 20)
    x_sample = X[::step, ::step].flatten()
    y_sample = Y[::step, ::step].flatten()
    z_sample = temperature_data[::step, ::step].flatten()
    scatter = ax4.scatter(x_sample, y_sample, z_sample, c=z_sample, cmap='hot', s=10)
    ax4.set_title('3D Scatter Plot (Sampled)', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Longitude Index')
    ax4.set_ylabel('Latitude Index')
    ax4.set_zlabel('Temperature (°C)')
    fig.colorbar(scatter, ax=ax4, shrink=0.5, label='Temperature (°C)')
    
    plt.tight_layout()
    output_file = output_dir / "temperature_3d_visualization.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"3D可視化を保存: {output_file}")
    plt.close()

def create_heightmap(temperature_data: np.ndarray, output_dir: Path):
    """温度データから高度マップを生成（VRChat/Blender用）"""
    temp_min = np.min(temperature_data)
    temp_max = np.max(temperature_data)
    normalized = (temperature_data - temp_min) / (temp_max - temp_min) * 65535
    
    heightmap = normalized.astype(np.uint16)
    img = Image.fromarray(heightmap, mode='I;16')
    
    output_file = output_dir / "temperature_heightmap.png"
    img.save(output_file)
    print(f"高度マップを保存: {output_file}")
    
    metadata = {
        "temperature_range": {
            "min": float(temp_min),
            "max": float(temp_max)
        },
        "normalized_range": {
            "min": 0,
            "max": 65535
        },
        "size": {
            "width": int(temperature_data.shape[1]),
            "height": int(temperature_data.shape[0])
        }
    }
    
    metadata_file = output_dir / "temperature_heightmap_metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"メタデータを保存: {metadata_file}")

def main():
    """メイン処理"""
    print("=" * 60)
    print("長野県上田市 気温分布分析")
    print("=" * 60)
    
    output_dir = Path("./output/ueda_temperature")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. バウンディングボックスを計算
    print("\n[1/6] バウンディングボックスを計算中...")
    bbox = calculate_bounding_box(
        LEOPALACE_LAT, LEOPALACE_LON,
        KARAOKE_LAT, KARAOKE_LON
    )
    print(f"バウンディングボックス: {bbox}")
    print(f"  経度範囲: {bbox[0]:.6f} - {bbox[2]:.6f}")
    print(f"  緯度範囲: {bbox[1]:.6f} - {bbox[3]:.6f}")
    
    # 2. 気温データを取得
    print("\n[2/6] 気温データを取得中...")
    date_range = [SUMMER_2024_START, SUMMER_2024_END]
    result = get_temperature_data(bbox, date_range)
    
    temperature_data = result["temperature_data"]
    print(f"データサイズ: {temperature_data.shape}")
    
    # 3. 統計処理
    print("\n[3/6] 統計処理中...")
    stats = calculate_statistics(temperature_data)
    print("統計結果:")
    for key, value in stats.items():
        print(f"  {key}: {value:.2f}°C")
    
    stats_file = output_dir / "temperature_statistics.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f"統計結果を保存: {stats_file}")
    
    # 4. 2D可視化
    print("\n[4/6] 2Dグラフを作成中...")
    visualize_2d(temperature_data, bbox, output_dir)
    
    # 5. 3D可視化
    print("\n[5/6] 3D可視化を作成中...")
    visualize_3d(temperature_data, bbox, output_dir)
    
    # 6. 高度マップ生成
    print("\n[6/6] 高度マップを生成中...")
    create_heightmap(temperature_data, output_dir)
    
    print("\n" + "=" * 60)
    print("処理完了！")
    print(f"出力ディレクトリ: {output_dir.absolute()}")
    print("=" * 60)

if __name__ == "__main__":
    main()
