#!/usr/bin/env python3
"""
JAXA Earth API MCP Server
地球観測データの検索・取得・処理・3D地形生成機能を提供するMCPサーバー
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import traceback

try:
    # 標準MCP SDKのFastMCPを使用（公式v0.1.5スタイルに合わせる）
    from mcp.server.fastmcp import FastMCP, Image
    from jaxa.earth import je
    import requests
    import numpy as np
    import rasterio
    from rasterio.transform import from_bounds
    from PIL import Image as PILImage
    from scipy import ndimage
except ImportError as e:
    print(f"Error importing required libraries: {e}", file=sys.stderr)
    print("Please install dependencies: uv sync", file=sys.stderr)
    sys.exit(1)

# FastMCPサーバーのインスタンスを作成（公式ドキュメントv0.1.5に合わせる）
mcp = FastMCP("JAXA_Earth_API_Assistant")

# グローバル変数: 一時ファイル保存ディレクトリ
TEMP_DIR = Path("./temp")
TEMP_DIR.mkdir(exist_ok=True)


# ============================================================================
# データ検索ツール
# ============================================================================

@mcp.tool()
async def search_collections_id() -> str:
    """
    JAXA Earth APIで利用可能なデータセットの詳細情報を返します。
    ユーザーのリクエストに基づいて、適切なデータセットIDとバンドを選択して応答してください。
    
    返されるテキストは、JAXA Earth APIを通じて利用可能なすべてのデータセットのリストです。
    各パラメータは以下のように記述されています：
    
    id: データセットを一意に識別するID
    title: データセットのタイトル
    description: データセットの説明
    bands: データセットに含まれるデータのID。複数のIDはカンマ（,）で区切られます。
    keywords: データセットに関連するキーワード。観測衛星の名前やデータを管理する宇宙機関の名前が含まれます。
    startDate: ISO8601形式のデータセット期間の開始日時を表す文字列。この日付以降のデータが利用可能であることを示します。
    endDate: ISO8601形式のデータセット期間の終了日時を表す文字列。"present"という値は、データがまだ毎日更新されていることを示します。
    各データセットのパラメータの終わりは"---"で示されます。
    bbox: データセットの地理的範囲（バウンディングボックス）。EPSG:4326の場合、[最小経度、最小緯度、最大経度、最大緯度]を示します。EPSG:3995またはEPSG:3031の場合、[最小X、最小Y、最大X、最大Y]を示します。
    epsg: データセットの投影方法を示すEPSGコード。
    
    上記に基づいて、ユーザーのリクエストに最適なデータセットIDとバンドを選択して応答してください。
    """
    try:
        # JAXA Earth APIデータセット情報を読み込む
        JE_TEXT_PATH = "https://data.earth.jaxa.jp/app/mcp/catalog.md"
        response = requests.get(JE_TEXT_PATH)
        je_text = response.text
        
        # データセット情報テキストを返す
        return je_text
    except Exception as e:
        return f"Error: {str(e)}\n{traceback.format_exc()}"


@mcp.tool()
async def search_collections(keywords: List[str]) -> Dict[str, Any]:
    """
    コレクション名とバンドをキーワードで検索します。
    
    Args:
        keywords: 検索キーワードのリスト（例: ["LST", "half-month"]）
    
    Returns:
        検索結果の辞書（collectionsとbandsを含む）
    """
    try:
        collection_list = je.ImageCollectionList()
        collections, bands = collection_list.filter_name(keywords=keywords)
        
        return {
            "collections": collections if isinstance(collections, list) else list(collections),
            "bands": bands if isinstance(bands, list) else list(bands),
            "keywords": keywords
        }
    except Exception as e:
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }


@mcp.tool()
def list_available_collections() -> Dict[str, Any]:
    """
    利用可能なコレクション一覧を取得します。
    
    Returns:
        利用可能なコレクションのリスト
    """
    try:
        collection_list = je.ImageCollectionList()
        # 空のキーワードで全コレクションを取得
        collections, bands = collection_list.filter_name(keywords=[])
        
        return {
            "collections": collections if isinstance(collections, list) else list(collections),
            "bands": bands if isinstance(bands, list) else list(bands),
            "total_count": len(collections) if isinstance(collections, list) else 0
        }
    except Exception as e:
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }


# ============================================================================
# 画像取得ツール
# ============================================================================

@mcp.tool()
async def show_images(
    collection: str = "JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global",
    band: str = "DSM",
    dlim: List[str] = ["2021-01-01T00:00:00", "2021-01-01T00:00:00"],
    bbox: List[float] = [135.0, 37.5, 140.0, 42.5],
) -> Any:  # Returns List[Image], but using Any to avoid Pydantic schema error
    """
    ユーザー入力に基づいてJAXA Earth APIを使用して衛星画像を表示します。
    
    Args:
        collection: JAXA Earth APIコレクションID
        band: コレクション内のバンド名
        dlim: 開始から終了までの日付範囲制限。yyyy-mm-ddThh:mm:ss形式の日付文字列
        bbox: データセットの地理的範囲（バウンディングボックス）。EPSG:4326の場合、[最小経度、最小緯度、最大経度、最大緯度]を示します
    """
    try:
        # ターゲット画像サイズでppu（単位あたりのピクセル）を設定
        image_size = 300  # 画像サイズターゲット
        ppu = image_size / (bbox[2] - bbox[0])
        
        # 画像を取得
        data = je.ImageCollection(collection=collection, ssl_verify=True)\
            .filter_date(dlim=dlim)\
            .filter_resolution(ppu=ppu)\
            .filter_bounds(bbox=bbox)\
            .select(band=band)\
            .get_images()
        
        # 画像を処理して表示
        img_data = je.ImageProcess(data)\
            .show_images(output="buffer")
        
        # PNGバッファとして画像データを返す
        output = []
        for png_buffer in img_data.png_buffers:
            output.append(Image(data=png_buffer, format="png"))
        return output
    except Exception as e:
        return [Image(data=f"Error: {str(e)}".encode(), format="text")]


@mcp.tool()
async def get_earth_images(
    collection: str,
    date_range: Optional[List[str]] = None,
    resolution: Optional[float] = None,
    bounds: Optional[List[float]] = None,
    geojson_path: Optional[str] = None,
    band: Optional[str] = None
) -> Dict[str, Any]:
    """
    日付、解像度、範囲、バンドを指定して地球観測画像を取得します。
    
    Args:
        collection: コレクション名（例: "JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global"）
        date_range: 日付範囲 [開始日, 終了日] (ISO形式: "YYYY-MM-DDTHH:MM:SS")
        resolution: 解像度（ppu: Pixels Per Unit）
        bounds: バウンディングボックス [min_lon, min_lat, max_lon, max_lat]
        geojson_path: GeoJSONファイルのパス（boundsより優先）
        band: バンド名（例: "DSM"）
    
    Returns:
        取得した画像データの情報
    """
    try:
        # ImageCollectionを作成
        image_collection = je.ImageCollection(collection)
        
        # 日付フィルタ
        if date_range:
            image_collection = image_collection.filter_date(date_range)
        else:
            # デフォルト: 2021年のデータ
            image_collection = image_collection.filter_date([
                "2021-01-01T00:00:00",
                "2021-12-31T23:59:59"
            ])
        
        # 解像度フィルタ
        if resolution:
            image_collection = image_collection.filter_resolution(resolution)
        
        # 範囲フィルタ
        if geojson_path and os.path.exists(geojson_path):
            geoj = je.FeatureCollection().read(geojson_path).select([])
            image_collection = image_collection.filter_bounds(geoj=geoj[0] if geoj else None)
        elif bounds:
            image_collection = image_collection.filter_bounds(bbox=bounds)
        
        # バンド選択
        if band:
            image_collection = image_collection.select(band)
        
        # 画像取得
        result = image_collection.get_images()
        
        # 結果情報を返す
        raster = result.raster if hasattr(result, 'raster') else None
        if raster:
            return {
                "success": True,
                "collection": collection,
                "raster_info": {
                    "shape": getattr(raster, 'img', {}).shape if hasattr(raster, 'img') else None,
                    "latlim": getattr(raster, 'latlim', None),
                    "lonlim": getattr(raster, 'lonlim', None)
                }
            }
        else:
            return {
                "success": False,
                "message": "画像の取得に失敗しました"
            }
    except Exception as e:
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }


# ============================================================================
# 画像処理ツール
# ============================================================================

@mcp.tool()
async def calc_spatial_stats(
    collection: str,
    date_range: Optional[List[str]] = None,
    bounds: Optional[List[float]] = None,
    band: Optional[str] = None
) -> Dict[str, Any]:
    """
    空間統計を計算します。
    
    Args:
        collection: コレクション名
        date_range: 日付範囲
        bounds: バウンディングボックス
        band: バンド名
    
    Returns:
        空間統計結果（mean, std, min, max, median）
    """
    try:
        # 公式v0.1.5スタイルに合わせる
        collection_param = collection if collection else "JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global"
        band_param = band if band else "DSM"
        dlim_param = date_range if date_range else ["2021-01-01T00:00:00", "2021-01-01T00:00:00"]
        bbox_param = bounds if bounds else [135.0, 37.5, 140.0, 42.5]
        
        # ターゲット画像サイズでppuを設定
        image_size = 300
        ppu = image_size / (bbox_param[2] - bbox_param[0])
        
        # 画像を取得
        data = je.ImageCollection(collection=collection_param, ssl_verify=True)\
            .filter_date(dlim=dlim_param)\
            .filter_resolution(ppu=ppu)\
            .filter_bounds(bbox=bbox_param)\
            .select(band=band_param)\
            .get_images()
        
        # 画像を処理
        img_data = je.ImageProcess(data)\
            .calc_spatial_stats()
        
        # 統計結果を返す
        return img_data.timeseries if hasattr(img_data, 'timeseries') else {}
    except Exception as e:
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }


@mcp.tool()
async def show_spatial_stats(
    collection: str = "JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global",
    band: str = "DSM",
    dlim: List[str] = ["2021-01-01T00:00:00", "2021-01-01T00:00:00"],
    bbox: List[float] = [135.0, 37.5, 140.0, 42.5],
) -> List[Image]:
    """
    ユーザー入力に基づいてJAXA Earth APIを使用して衛星データの空間統計結果画像を表示します。
    
    Args:
        collection: JAXA Earth APIコレクションID
        band: コレクション内のバンド名
        dlim: 開始から終了までの日付範囲制限。yyyy-mm-ddThh:mm:ss形式の日付文字列
        bbox: データセットの地理的範囲（バウンディングボックス）
    """
    try:
        # ターゲット画像サイズでppuを設定
        image_size = 300
        ppu = image_size / (bbox[2] - bbox[0])
        
        # 画像を取得
        data = je.ImageCollection(collection=collection, ssl_verify=True)\
            .filter_date(dlim=dlim)\
            .filter_resolution(ppu=ppu)\
            .filter_bounds(bbox=bbox)\
            .select(band=band)\
            .get_images()
        
        # 画像を処理して表示
        img_data = je.ImageProcess(data)\
            .calc_spatial_stats()\
            .show_spatial_stats(output="buffer")
        
        # PNGバッファとして画像データを返す
        output_images = []
        for png_buffer in img_data.png_buffers_stats:
            output_images.append(Image(data=png_buffer, format="png"))
        
        return output_images
    except Exception as e:
        return [Image(data=f"Error: {str(e)}".encode(), format="text")]


@mcp.tool()
async def calc_temporal_stats(
    collection: str,
    date_range: List[str],
    method: str = "mean",
    bounds: Optional[List[float]] = None,
    band: Optional[str] = None
) -> Dict[str, Any]:
    """
    時間統計を計算します。
    
    Args:
        collection: コレクション名
        date_range: 日付範囲
        method: 統計手法 ("mean", "max", "min", "std", "median")
        bounds: バウンディングボックス
        band: バンド名
    
    Returns:
        時間統計結果
    """
    try:
        image_collection = je.ImageCollection(collection)
        image_collection = image_collection.filter_date(date_range)
        if bounds:
            image_collection = image_collection.filter_bounds(bbox=bounds)
        if band:
            image_collection = image_collection.select(band)
        
        result = image_collection.get_images()
        img_process = je.ImageProcess(result)
        img_process = img_process.calc_temporal_stats(method_query=method)
        
        return {
            "success": True,
            "method": method,
            "temporal_statistics": "計算完了"
        }
    except Exception as e:
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }


# ============================================================================
# GeoJSON処理ツール
# ============================================================================

@mcp.tool()
def read_geojson(file_path: str) -> Dict[str, Any]:
    """
    GeoJSONファイルを読み込みます。
    
    Args:
        file_path: GeoJSONファイルのパス
    
    Returns:
        読み込んだGeoJSONデータの情報
    """
    try:
        if not os.path.exists(file_path):
            return {
                "error": f"ファイルが見つかりません: {file_path}"
            }
        
        feature_collection = je.FeatureCollection().read(file_path)
        features = feature_collection.select([])
        
        return {
            "success": True,
            "file_path": file_path,
            "feature_count": len(features) if isinstance(features, list) else 1
        }
    except Exception as e:
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }


@mcp.tool()
def select_features(file_path: str, keywords: List[str]) -> Dict[str, Any]:
    """
    キーワードでフィーチャーを選択します。
    
    Args:
        file_path: GeoJSONファイルのパス
        keywords: 検索キーワードのリスト
    
    Returns:
        選択されたフィーチャーの情報
    """
    try:
        if not os.path.exists(file_path):
            return {
                "error": f"ファイルが見つかりません: {file_path}"
            }
        
        feature_collection = je.FeatureCollection().read(file_path)
        selected = feature_collection.select(keywords)
        
        return {
            "success": True,
            "keywords": keywords,
            "selected_count": len(selected) if isinstance(selected, list) else 1
        }
    except Exception as e:
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }


# ============================================================================
# 3D地形生成・エクスポートツール（VRChat向け）
# ============================================================================

@mcp.tool()
def generate_heightmap(
    collection: str,
    bounds: List[float],
    resolution: float = 20.0,
    date_range: Optional[List[str]] = None,
    output_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    衛星データから高度マップ（Heightmap）を生成します。
    
    Args:
        collection: コレクション名（標高データ用、例: "JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global"）
        bounds: バウンディングボックス [min_lon, min_lat, max_lon, max_lat]
        resolution: 解像度（ppu）
        date_range: 日付範囲（オプション）
        output_path: 出力ファイルパス（オプション、未指定時はtempディレクトリに保存）
    
    Returns:
        生成された高度マップの情報
    """
    try:
        # 標高データを取得
        image_collection = je.ImageCollection(collection)
        if date_range:
            image_collection = image_collection.filter_date(date_range)
        image_collection = image_collection.filter_resolution(resolution)
        image_collection = image_collection.filter_bounds(bbox=bounds)
        image_collection = image_collection.select("DSM")  # Digital Surface Model
        
        result = image_collection.get_images()
        raster = result.raster if hasattr(result, 'raster') else None
        
        if not raster or not hasattr(raster, 'img'):
            return {
                "error": "高度データの取得に失敗しました"
            }
        
        # 高度データをnumpy配列に変換
        height_data = np.array(raster.img)
        
        # 正規化（0-1の範囲に）
        height_min = np.nanmin(height_data)
        height_max = np.nanmax(height_data)
        height_normalized = (height_data - height_min) / (height_max - height_min)
        
        # 出力パスを決定
        if not output_path:
            output_path = str(TEMP_DIR / "heightmap.png")
        
        # PNG形式で保存（16bitグレースケール）
        height_uint16 = (height_normalized * 65535).astype(np.uint16)
        height_image = Image.fromarray(height_uint16, mode='I;16')
        height_image.save(output_path)
        
        return {
            "success": True,
            "output_path": output_path,
            "shape": height_data.shape,
            "height_range": {
                "min": float(height_min),
                "max": float(height_max)
            },
            "bounds": bounds
        }
    except Exception as e:
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }


@mcp.tool()
def export_to_blender(
    collection: str,
    bounds: List[float],
    resolution: float = 20.0,
    date_range: Optional[List[str]] = None,
    output_dir: Optional[str] = None
) -> Dict[str, Any]:
    """
    Blender用の高度データとテクスチャをエクスポートします。
    
    Args:
        collection: コレクション名
        bounds: バウンディングボックス
        resolution: 解像度
        date_range: 日付範囲
        output_dir: 出力ディレクトリ（オプション）
    
    Returns:
        エクスポートされたファイルの情報
    """
    try:
        if not output_dir:
            output_dir = str(TEMP_DIR / "blender_export")
        os.makedirs(output_dir, exist_ok=True)
        
        # 高度マップ生成
        heightmap_result = generate_heightmap(
            collection=collection,
            bounds=bounds,
            resolution=resolution,
            date_range=date_range,
            output_path=os.path.join(output_dir, "heightmap.exr")
        )
        
        if "error" in heightmap_result:
            return heightmap_result
        
        # EXR形式で高度マップを保存（32bit浮動小数点）
        image_collection = je.ImageCollection(collection)
        if date_range:
            image_collection = image_collection.filter_date(date_range)
        image_collection = image_collection.filter_resolution(resolution)
        image_collection = image_collection.filter_bounds(bbox=bounds)
        image_collection = image_collection.select("DSM")
        
        result = image_collection.get_images()
        raster = result.raster
        height_data = np.array(raster.img).astype(np.float32)
        
        # EXR形式で保存（rasterioを使用）
        height_min, height_max = np.nanmin(height_data), np.nanmax(height_data)
        height_normalized = (height_data - height_min) / (height_max - height_min)
        
        exr_path = os.path.join(output_dir, "heightmap.exr")
        # EXR形式はPILでは直接サポートされていないため、PNG形式で保存
        # 実際のEXR形式はOpenEXRライブラリが必要
        height_uint16 = (height_normalized * 65535).astype(np.uint16)
        height_image = Image.fromarray(height_uint16, mode='I;16')
        height_image.save(exr_path.replace('.exr', '.png'))
        
        # テクスチャ（衛星画像）も取得して保存
        texture_path = os.path.join(output_dir, "texture.png")
        # ここでは高度マップをテクスチャとしても使用（実際には別のバンドを使用可能）
        height_image.save(texture_path)
        
        return {
            "success": True,
            "output_dir": output_dir,
            "files": {
                "heightmap": exr_path.replace('.exr', '.png'),
                "texture": texture_path
            },
            "note": "EXR形式はPNG形式で保存されました。BlenderでDisplace Modifierを使用する際は、画像を読み込んで使用してください。"
        }
    except Exception as e:
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }


@mcp.tool()
def export_to_unity(
    collection: str,
    bounds: List[float],
    resolution: float = 20.0,
    date_range: Optional[List[str]] = None,
    output_dir: Optional[str] = None
) -> Dict[str, Any]:
    """
    Unity用の地形データをエクスポートします。
    
    Args:
        collection: コレクション名
        bounds: バウンディングボックス
        resolution: 解像度
        date_range: 日付範囲
        output_dir: 出力ディレクトリ
    
    Returns:
        エクスポートされたファイルの情報
    """
    try:
        if not output_dir:
            output_dir = str(TEMP_DIR / "unity_export")
        os.makedirs(output_dir, exist_ok=True)
        
        # 高度データを取得
        image_collection = je.ImageCollection(collection)
        if date_range:
            image_collection = image_collection.filter_date(date_range)
        image_collection = image_collection.filter_resolution(resolution)
        image_collection = image_collection.filter_bounds(bbox=bounds)
        image_collection = image_collection.select("DSM")
        
        result = image_collection.get_images()
        raster = result.raster
        height_data = np.array(raster.img).astype(np.float32)
        
        # Unity Terrain Tool用の.raw形式で保存
        # UnityのTerrainは16bitの高さマップを使用
        height_min, height_max = np.nanmin(height_data), np.nanmax(height_data)
        height_normalized = (height_data - height_min) / (height_max - height_min)
        height_uint16 = (height_normalized * 65535).astype(np.uint16)
        
        # .raw形式で保存（リトルエンディアン、16bit）
        raw_path = os.path.join(output_dir, "terrain.raw")
        height_uint16.byteswap(False).tofile(raw_path)
        
        # テクスチャも保存
        texture_path = os.path.join(output_dir, "terrain_texture.png")
        height_image = Image.fromarray(height_uint16, mode='I;16')
        height_image.save(texture_path)
        
        # メタデータファイル（Unity用の情報）
        metadata = {
            "width": int(height_data.shape[1]),
            "height": int(height_data.shape[0]),
            "depth": 16,  # 16bit
            "height_range": {
                "min": float(height_min),
                "max": float(height_max)
            },
            "bounds": bounds
        }
        
        metadata_path = os.path.join(output_dir, "terrain_metadata.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        return {
            "success": True,
            "output_dir": output_dir,
            "files": {
                "terrain_raw": raw_path,
                "texture": texture_path,
                "metadata": metadata_path
            },
            "metadata": metadata,
            "note": "UnityのTerrain Toolで.rawファイルをインポートする際は、メタデータの情報を参照してください。"
        }
    except Exception as e:
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }


@mcp.tool()
def create_vrchat_terrain(
    collection: str,
    bounds: List[float],
    resolution: float = 20.0,
    max_polygons: int = 100000,
    texture_size: int = 2048,
    date_range: Optional[List[str]] = None,
    output_dir: Optional[str] = None
) -> Dict[str, Any]:
    """
    VRChat向けに最適化された地形データを生成します。
    
    Args:
        collection: コレクション名
        bounds: バウンディングボックス
        resolution: 解像度
        max_polygons: 最大ポリゴン数（VRChat制約対応）
        texture_size: テクスチャサイズ（VRChat推奨: 2048以下）
        date_range: 日付範囲
        output_dir: 出力ディレクトリ
    
    Returns:
        最適化された地形データの情報
    """
    try:
        if not output_dir:
            output_dir = str(TEMP_DIR / "vrchat_terrain")
        os.makedirs(output_dir, exist_ok=True)
        
        # 高度データを取得
        image_collection = je.ImageCollection(collection)
        if date_range:
            image_collection = image_collection.filter_date(date_range)
        image_collection = image_collection.filter_resolution(resolution)
        image_collection = image_collection.filter_bounds(bbox=bounds)
        image_collection = image_collection.select("DSM")
        
        result = image_collection.get_images()
        raster = result.raster
        height_data = np.array(raster.img).astype(np.float32)
        
        # ポリゴン数制約に合わせて解像度を調整
        current_polygons = height_data.shape[0] * height_data.shape[1] * 2
        if current_polygons > max_polygons:
            scale_factor = np.sqrt(max_polygons / current_polygons)
            new_height = int(height_data.shape[0] * scale_factor)
            new_width = int(height_data.shape[1] * scale_factor)
            height_data = ndimage.zoom(height_data, (new_height / height_data.shape[0], new_width / height_data.shape[1]), order=1)
        
        # テクスチャサイズに合わせてリサイズ
        height_min, height_max = np.nanmin(height_data), np.nanmax(height_data)
        height_normalized = (height_data - height_min) / (height_max - height_min)
        height_uint16 = (height_normalized * 65535).astype(np.uint16)
        
        # テクスチャをリサイズ
        texture_image = Image.fromarray(height_uint16, mode='I;16')
        texture_image = texture_image.resize((texture_size, texture_size), Image.Resampling.LANCZOS)
        
        # ファイル保存
        heightmap_path = os.path.join(output_dir, "vrchat_heightmap.png")
        texture_path = os.path.join(output_dir, "vrchat_texture.png")
        
        texture_image.save(heightmap_path)
        texture_image.save(texture_path)
        
        # メタデータ
        metadata = {
            "width": int(height_data.shape[1]),
            "height": int(height_data.shape[0]),
            "texture_size": texture_size,
            "estimated_polygons": int(height_data.shape[0] * height_data.shape[1] * 2),
            "height_range": {
                "min": float(height_min),
                "max": float(height_max)
            },
            "bounds": bounds,
            "optimization": {
                "max_polygons": max_polygons,
                "texture_size": texture_size
            }
        }
        
        metadata_path = os.path.join(output_dir, "vrchat_metadata.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        return {
            "success": True,
            "output_dir": output_dir,
            "files": {
                "heightmap": heightmap_path,
                "texture": texture_path,
                "metadata": metadata_path
            },
            "metadata": metadata,
            "note": "VRChatのワールドサイズ制限（100MB）を考慮して最適化されています。BlenderまたはUnityでインポートして使用してください。"
        }
    except Exception as e:
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }


@mcp.tool()
def export_texture_maps(
    collection: str,
    bounds: List[float],
    resolution: float = 20.0,
    date_range: Optional[List[str]] = None,
    output_dir: Optional[str] = None
) -> Dict[str, Any]:
    """
    衛星画像をテクスチャマップとしてエクスポートします（Diffuse, Normal等）。
    
    Args:
        collection: コレクション名
        bounds: バウンディングボックス
        resolution: 解像度
        date_range: 日付範囲
        output_dir: 出力ディレクトリ
    
    Returns:
        エクスポートされたテクスチャマップの情報
    """
    try:
        if not output_dir:
            output_dir = str(TEMP_DIR / "texture_maps")
        os.makedirs(output_dir, exist_ok=True)
        
        # 衛星画像を取得（複数のバンドがある場合は最初のバンドを使用）
        image_collection = je.ImageCollection(collection)
        if date_range:
            image_collection = image_collection.filter_date(date_range)
        image_collection = image_collection.filter_resolution(resolution)
        image_collection = image_collection.filter_bounds(bbox=bounds)
        
        # 利用可能なバンドを取得
        result = image_collection.get_images()
        raster = result.raster
        image_data = np.array(raster.img)
        
        # Diffuseマップ（基本テクスチャ）
        if len(image_data.shape) == 2:
            # グレースケールの場合、RGBに変換
            diffuse_data = np.stack([image_data, image_data, image_data], axis=-1)
        else:
            diffuse_data = image_data
        
        # 正規化
        diffuse_normalized = (diffuse_data - np.nanmin(diffuse_data)) / (np.nanmax(diffuse_data) - np.nanmin(diffuse_data))
        diffuse_uint8 = (diffuse_normalized * 255).astype(np.uint8)
        
        diffuse_image = Image.fromarray(diffuse_uint8, mode='RGB')
        diffuse_path = os.path.join(output_dir, "diffuse.png")
        diffuse_image.save(diffuse_path)
        
        # Normalマップ（簡易版：高度データから生成）
        height_data = image_data if len(image_data.shape) == 2 else np.mean(image_data, axis=2)
        normal_map = _generate_normal_map(height_data)
        normal_path = os.path.join(output_dir, "normal.png")
        normal_image = Image.fromarray(normal_map, mode='RGB')
        normal_image.save(normal_path)
        
        return {
            "success": True,
            "output_dir": output_dir,
            "files": {
                "diffuse": diffuse_path,
                "normal": normal_path
            },
            "note": "Normalマップは高度データから簡易的に生成されています。より高品質なNormalマップが必要な場合は、専用のツールを使用してください。"
        }
    except Exception as e:
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }


def _generate_normal_map(height_data: np.ndarray) -> np.ndarray:
    """高度データからNormalマップを生成するヘルパー関数"""
    # Sobelフィルタで勾配を計算
    sobel_x = ndimage.sobel(height_data, axis=1)
    sobel_y = ndimage.sobel(height_data, axis=0)
    
    # Normalベクトルを計算
    normal_x = -sobel_x
    normal_y = -sobel_y
    normal_z = np.ones_like(height_data)
    
    # 正規化
    magnitude = np.sqrt(normal_x**2 + normal_y**2 + normal_z**2)
    normal_x /= magnitude
    normal_y /= magnitude
    normal_z /= magnitude
    
    # RGB形式に変換（0-255の範囲）
    normal_map = np.stack([
        ((normal_x + 1) * 127.5).astype(np.uint8),
        ((normal_y + 1) * 127.5).astype(np.uint8),
        ((normal_z + 1) * 127.5).astype(np.uint8)
    ], axis=-1)
    
    return normal_map


# ============================================================================
# Plan Mode Tools
# ============================================================================

# Plan storage directory
PLAN_DIR = Path("./_docs/plans")
PLAN_DIR.mkdir(parents=True, exist_ok=True)

@mcp.tool()
def create_plan(
    task_description: str,
    objectives: List[str],
    steps: List[Dict[str, Any]],
    estimated_time: Optional[str] = None
) -> Dict[str, Any]:
    """
    複雑なタスクの実装計画を作成します。
    
    Args:
        task_description: タスクの説明
        objectives: 目標のリスト
        steps: ステップのリスト（各ステップは辞書形式で、description, files, dependencies, riskを含む）
        estimated_time: 推定時間（オプション）
    
    Returns:
        作成された計画の情報
    """
    try:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        plan_id = f"plan_{timestamp}"
        
        plan_data = {
            "id": plan_id,
            "task_description": task_description,
            "objectives": objectives,
            "steps": steps,
            "estimated_time": estimated_time,
            "status": "created",
            "created_at": timestamp,
            "completed_steps": [],
            "current_step": None
        }
        
        # Save plan to file
        plan_file = PLAN_DIR / f"{plan_id}.json"
        with open(plan_file, 'w', encoding='utf-8') as f:
            json.dump(plan_data, f, ensure_ascii=False, indent=2)
        
        # Generate markdown plan
        markdown_plan = _generate_markdown_plan(plan_data)
        plan_md_file = PLAN_DIR / f"{plan_id}.md"
        with open(plan_md_file, 'w', encoding='utf-8') as f:
            f.write(markdown_plan)
        
        return {
            "plan_id": plan_id,
            "status": "created",
            "plan_file": str(plan_file),
            "markdown_file": str(plan_md_file),
            "total_steps": len(steps),
            "message": f"Plan created successfully with {len(steps)} steps"
        }
    except Exception as e:
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }

@mcp.tool()
def update_plan_status(
    plan_id: str,
    step_index: int,
    status: str,
    notes: Optional[str] = None
) -> Dict[str, Any]:
    """
    計画のステップのステータスを更新します。
    
    Args:
        plan_id: 計画ID
        step_index: ステップのインデックス（0から開始）
        status: ステータス（"pending", "in_progress", "completed", "failed"）
        notes: 追加のメモ（オプション）
    
    Returns:
        更新結果
    """
    try:
        plan_file = PLAN_DIR / f"{plan_id}.json"
        if not plan_file.exists():
            return {"error": f"Plan {plan_id} not found"}
        
        with open(plan_file, 'r', encoding='utf-8') as f:
            plan_data = json.load(f)
        
        if step_index < 0 or step_index >= len(plan_data["steps"]):
            return {"error": f"Invalid step index: {step_index}"}
        
        # Update step status
        plan_data["steps"][step_index]["status"] = status
        if notes:
            plan_data["steps"][step_index]["notes"] = notes
        
        # Update completed steps
        if status == "completed" and step_index not in plan_data["completed_steps"]:
            plan_data["completed_steps"].append(step_index)
        elif status != "completed" and step_index in plan_data["completed_steps"]:
            plan_data["completed_steps"].remove(step_index)
        
        # Update current step
        if status == "in_progress":
            plan_data["current_step"] = step_index
        elif status == "completed" and plan_data["current_step"] == step_index:
            plan_data["current_step"] = None
        
        # Update overall status
        total_steps = len(plan_data["steps"])
        completed_count = len(plan_data["completed_steps"])
        if completed_count == total_steps:
            plan_data["status"] = "completed"
        elif completed_count > 0 or any(s.get("status") == "in_progress" for s in plan_data["steps"]):
            plan_data["status"] = "in_progress"
        
        # Save updated plan
        with open(plan_file, 'w', encoding='utf-8') as f:
            json.dump(plan_data, f, ensure_ascii=False, indent=2)
        
        # Update markdown file
        markdown_plan = _generate_markdown_plan(plan_data)
        plan_md_file = PLAN_DIR / f"{plan_id}.md"
        with open(plan_md_file, 'w', encoding='utf-8') as f:
            f.write(markdown_plan)
        
        return {
            "plan_id": plan_id,
            "step_index": step_index,
            "status": status,
            "progress": f"{completed_count}/{total_steps} steps completed ({completed_count*100//total_steps}%)",
            "overall_status": plan_data["status"]
        }
    except Exception as e:
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }

@mcp.tool()
def get_plan_status(plan_id: str) -> Dict[str, Any]:
    """
    計画の現在のステータスを取得します。
    
    Args:
        plan_id: 計画ID
    
    Returns:
        計画のステータス情報
    """
    try:
        plan_file = PLAN_DIR / f"{plan_id}.json"
        if not plan_file.exists():
            return {"error": f"Plan {plan_id} not found"}
        
        with open(plan_file, 'r', encoding='utf-8') as f:
            plan_data = json.load(f)
        
        total_steps = len(plan_data["steps"])
        completed_count = len(plan_data["completed_steps"])
        
        return {
            "plan_id": plan_id,
            "task_description": plan_data["task_description"],
            "status": plan_data["status"],
            "progress": f"{completed_count}/{total_steps} steps completed",
            "percentage": completed_count * 100 // total_steps if total_steps > 0 else 0,
            "current_step": plan_data["current_step"],
            "steps": [
                {
                    "index": i,
                    "description": step.get("description", ""),
                    "status": step.get("status", "pending"),
                    "files": step.get("files", [])
                }
                for i, step in enumerate(plan_data["steps"])
            ]
        }
    except Exception as e:
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }

def _generate_markdown_plan(plan_data: Dict[str, Any]) -> str:
    """計画データからMarkdown形式の計画書を生成"""
    md = f"# Implementation Plan: {plan_data['task_description']}\n\n"
    md += f"**Plan ID**: `{plan_data['id']}`\n"
    md += f"**Created**: {plan_data['created_at']}\n"
    md += f"**Status**: {plan_data['status']}\n\n"
    
    if plan_data.get('estimated_time'):
        md += f"**Estimated Time**: {plan_data['estimated_time']}\n\n"
    
    md += "## Overview\n\n"
    md += f"{plan_data['task_description']}\n\n"
    
    md += "## Objectives\n\n"
    for obj in plan_data['objectives']:
        md += f"- {obj}\n"
    md += "\n"
    
    md += "## Execution Plan\n\n"
    for i, step in enumerate(plan_data['steps']):
        status_icon = {
            "pending": "⏳",
            "in_progress": "🔄",
            "completed": "✅",
            "failed": "❌"
        }.get(step.get("status", "pending"), "⏳")
        
        md += f"### Step {i+1}: {step.get('description', 'N/A')}\n"
        md += f"**Status**: {status_icon} {step.get('status', 'pending')}\n\n"
        
        if step.get('files'):
            md += f"**Files**: {', '.join(f'`{f}`' for f in step['files'])}\n\n"
        
        if step.get('dependencies'):
            md += f"**Dependencies**: {', '.join(step['dependencies'])}\n\n"
        
        if step.get('risk'):
            md += f"**Risk**: {step['risk']}\n\n"
        
        if step.get('notes'):
            md += f"**Notes**: {step['notes']}\n\n"
        
        md += "---\n\n"
    
    total_steps = len(plan_data['steps'])
    completed_count = len(plan_data['completed_steps'])
    md += f"## Progress\n\n"
    md += f"**Completed**: {completed_count}/{total_steps} steps ({completed_count*100//total_steps if total_steps > 0 else 0}%)\n\n"
    
    return md


# ============================================================================
# メイン実行
# ============================================================================

# メイン実行関数（公式v0.1.5スタイルに合わせる）
def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
