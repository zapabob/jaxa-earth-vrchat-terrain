#!/usr/bin/env python3
"""
JAXA Earth API MCP Server - Streamlit UI
Appleデザインの自然言語インターフェースでMCP機能を実行
"""

import streamlit as st
import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
import traceback
from datetime import datetime

# MCPサーバーのツールを直接インポート（関数を直接呼び出し）
try:
    import sys
    from pathlib import Path
    
    # 現在のディレクトリをパスに追加
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))
    
    # MCPサーバーの関数を直接インポート
    import importlib.util
    mcp_server_path = current_dir / "mcp_server.py"
    spec = importlib.util.spec_from_file_location("mcp_server", mcp_server_path)
    mcp_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mcp_module)
    
    # 関数を取得（@mcp.tool()デコレータでラップされた関数を直接呼び出し可能）
    search_collections_id = mcp_module.search_collections_id
    search_collections = mcp_module.search_collections
    list_available_collections = mcp_module.list_available_collections
    show_images = mcp_module.show_images
    calc_spatial_stats = mcp_module.calc_spatial_stats
    show_spatial_stats = mcp_module.show_spatial_stats
    get_earth_images = getattr(mcp_module, 'get_earth_images', None)
    process_geojson = getattr(mcp_module, 'process_geojson', None)
    generate_heightmap = getattr(mcp_module, 'generate_heightmap', None)
    export_heightmap = getattr(mcp_module, 'export_heightmap', None)
    create_plan = mcp_module.create_plan
    update_plan_status = mcp_module.update_plan_status
    get_plan_status = mcp_module.get_plan_status
    
    from jaxa.earth import je
    import numpy as np
    from PIL import Image as PILImage
    import io
except Exception as e:
    st.error(f"必要なライブラリのインポートに失敗しました: {e}")
    st.code(traceback.format_exc())
    st.stop()

# ページ設定
st.set_page_config(
    page_title="JAXA Earth API - MCP Interface",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apple風のカスタムCSS
APPLE_CSS = """
<style>
    /* Apple風のデザイン */
    .main {
        padding: 2rem 3rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    h1 {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
        font-weight: 600;
        color: #1d1d1f;
        letter-spacing: -0.5px;
        margin-bottom: 1rem;
    }
    
    h2, h3 {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
        font-weight: 500;
        color: #1d1d1f;
    }
    
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 1px solid #d2d2d7;
        padding: 12px 16px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #0071e3;
        box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #0071e3 0%, #0051d5 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 500;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0, 113, 227, 0.2);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #0051d5 0%, #003d9e 100%);
        box-shadow: 0 4px 12px rgba(0, 113, 227, 0.3);
        transform: translateY(-1px);
    }
    
    .stSelectbox > div > div > select {
        border-radius: 12px;
        border: 1px solid #d2d2d7;
    }
    
    .info-box {
        background: white;
        border-radius: 16px;
        padding: 20px;
        margin: 16px 0;
        box-shadow: 0 2px 16px rgba(0, 0, 0, 0.08);
    }
    
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 4px solid #28a745;
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
    }
    
    .error-box {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border-left: 4px solid #dc3545;
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
    }
    
    .code-block {
        background: #f5f5f7;
        border-radius: 8px;
        padding: 12px;
        font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace;
        font-size: 14px;
        overflow-x: auto;
    }
</style>
"""

st.markdown(APPLE_CSS, unsafe_allow_html=True)

# セッション状態の初期化
if 'execution_history' not in st.session_state:
    st.session_state.execution_history = []
if 'current_result' not in st.session_state:
    st.session_state.current_result = None
if 'selected_tool' not in st.session_state:
    st.session_state.selected_tool = None

# サイドバー
with st.sidebar:
    st.title("🌍 JAXA Earth API")
    st.markdown("---")
    
    st.subheader("利用可能な機能")
    
    # ツール選択
    tool_options = {
        "🔍 コレクション検索": "search_collections",
        "📋 コレクション一覧": "list_collections",
        "🖼️ 画像取得": "show_images",
        "📊 空間統計": "calc_spatial_stats",
        "🗺️ 高度マップ生成": "generate_heightmap",
        "📝 計画作成": "create_plan",
    }
    
    selected_tool_name = st.selectbox(
        "機能を選択",
        options=list(tool_options.keys()),
        key="tool_selector"
    )
    
    st.session_state.selected_tool = tool_options[selected_tool_name]
    
    st.markdown("---")
    st.markdown("### 💡 使い方")
    st.markdown("""
    1. 自然言語でリクエストを入力
    2. 自動的に適切なMCPツールが選択されます
    3. 結果がリアルタイムで表示されます
    """)

# メインコンテンツ
st.title("🌍 JAXA Earth API - MCP Interface")
st.markdown("自然言語で地球観測データを検索・取得・可視化")

# 自然言語入力
user_input = st.text_area(
    "自然言語でリクエストを入力してください",
    placeholder="例: 富士山周辺の標高データを取得して、高度マップを生成してください",
    height=100,
    key="user_input"
)

col1, col2 = st.columns([1, 4])

with col1:
    execute_button = st.button("🚀 実行", type="primary", use_container_width=True)

with col2:
    clear_button = st.button("🗑️ 履歴をクリア", use_container_width=True)

if clear_button:
    st.session_state.execution_history = []
    st.session_state.current_result = None
    st.rerun()

# 実行処理
if execute_button and user_input:
    with st.spinner("処理中..."):
        try:
            # 自然言語からツールとパラメータを推論
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(execute_natural_language_request(user_input))
            loop.close()
            
            st.session_state.current_result = result
            st.session_state.execution_history.append({
                "timestamp": datetime.now().isoformat(),
                "input": user_input,
                "result": result
            })
        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")
            st.code(traceback.format_exc())

# 結果表示
if st.session_state.current_result:
    display_result(st.session_state.current_result)

# 実行履歴
if st.session_state.execution_history:
    with st.expander("📜 実行履歴", expanded=False):
        for i, entry in enumerate(reversed(st.session_state.execution_history[-10:])):
            st.markdown(f"**{i+1}. {entry['timestamp']}**")
            st.markdown(f"入力: {entry['input']}")
            st.markdown("---")


async def execute_natural_language_request(user_input: str) -> Dict[str, Any]:
    """
    自然言語リクエストを解析して適切なMCPツールを実行
    """
    user_input_lower = user_input.lower()
    
    # キーワードベースのツール選択
    if "検索" in user_input or "search" in user_input_lower or "コレクション" in user_input:
        keywords = extract_keywords(user_input)
        result = await search_collections(keywords)
        return {
            "tool": "search_collections",
            "input": user_input,
            "result": result
        }
    
    elif "一覧" in user_input or "list" in user_input_lower:
        result = list_available_collections()
        return {
            "tool": "list_collections",
            "input": user_input,
            "result": result
        }
    
    elif "画像" in user_input or "image" in user_input_lower or "表示" in user_input:
        # パラメータを抽出
        params = extract_image_params(user_input)
        result = await show_images(**params)
        return {
            "tool": "show_images",
            "input": user_input,
            "params": params,
            "result": result
        }
    
    elif "統計" in user_input or "stat" in user_input_lower:
        params = extract_spatial_stats_params(user_input)
        result = await calc_spatial_stats(**params)
        return {
            "tool": "calc_spatial_stats",
            "input": user_input,
            "params": params,
            "result": result
        }
    
    elif "高度マップ" in user_input or "heightmap" in user_input_lower or "地形" in user_input:
        params = extract_heightmap_params(user_input)
        if generate_heightmap:
            result = generate_heightmap(**params)
        else:
            result = {"error": "generate_heightmap関数が利用できません"}
        return {
            "tool": "generate_heightmap",
            "input": user_input,
            "params": params,
            "result": result
        }
    
    elif "計画" in user_input or "plan" in user_input_lower:
        # 計画作成は複雑なので、デフォルトパラメータを使用
        result = create_plan(
            task_description=user_input,
            objectives=[],
            steps=[],
            estimated_time=None
        )
        return {
            "tool": "create_plan",
            "input": user_input,
            "result": result
        }
    
    else:
        # デフォルト: コレクション検索
        keywords = extract_keywords(user_input)
        result = await search_collections(keywords)
        return {
            "tool": "search_collections",
            "input": user_input,
            "result": result
        }


def extract_keywords(text: str) -> List[str]:
    """自然言語からキーワードを抽出"""
    # 簡単なキーワード抽出（実際にはより高度なNLPを使用可能）
    keywords = []
    common_terms = {
        "温度": "LST",
        "標高": "DSM",
        "高度": "DSM",
        "地表面温度": "LST",
        "植生": "NDVI",
        "海面水温": "SST",
    }
    
    for term, keyword in common_terms.items():
        if term in text:
            keywords.append(keyword)
    
    # 英語キーワードも抽出
    if "temperature" in text.lower():
        keywords.append("LST")
    if "elevation" in text.lower() or "height" in text.lower():
        keywords.append("DSM")
    
    return keywords if keywords else ["LST", "DSM"]


def extract_image_params(text: str) -> Dict[str, Any]:
    """画像取得のパラメータを抽出"""
    # デフォルト値
    params = {
        "collection": "JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global",
        "band": "DSM",
        "dlim": ["2021-01-01T00:00:00", "2021-01-01T00:00:00"],
        "bbox": [135.0, 35.0, 140.0, 40.0],  # 関東地方
    }
    
    # 富士山周辺
    if "富士山" in text or "fuji" in text.lower():
        params["bbox"] = [138.5, 35.2, 139.0, 35.5]
    
    # 日付範囲の抽出（簡易版）
    # 実際にはより高度な日付解析が必要
    
    return params


def extract_spatial_stats_params(text: str) -> Dict[str, Any]:
    """空間統計のパラメータを抽出"""
    params = {
        "collection": "JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global",
        "band": "DSM",
        "bbox": [135.0, 35.0, 140.0, 40.0],
    }
    
    if "富士山" in text or "fuji" in text.lower():
        params["bbox"] = [138.5, 35.2, 139.0, 35.5]
    
    return params


def extract_heightmap_params(text: str) -> Dict[str, Any]:
    """高度マップ生成のパラメータを抽出"""
    params = {
        "collection": "JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global",
        "band": "DSM",
        "bbox": [135.0, 35.0, 140.0, 40.0],
        "output_format": "png",
    }
    
    if "富士山" in text or "fuji" in text.lower():
        params["bbox"] = [138.5, 35.2, 139.0, 35.5]
    
    return params


def display_result(result: Dict[str, Any]):
    """結果を表示"""
    tool = result.get("tool", "unknown")
    
    st.markdown("### 📊 実行結果")
    
    if tool == "search_collections":
        display_search_result(result["result"])
    elif tool == "list_collections":
        display_list_result(result["result"])
    elif tool == "show_images":
        display_images(result["result"])
    elif tool == "calc_spatial_stats":
        display_spatial_stats(result["result"])
    elif tool == "generate_heightmap":
        display_heightmap(result["result"])
    else:
        st.json(result["result"])


def display_search_result(result: Dict[str, Any]):
    """検索結果を表示"""
    if "error" in result:
        st.error(f"エラー: {result['error']}")
        return
    
    collections = result.get("collections", [])
    bands = result.get("bands", [])
    
    st.success(f"✅ {len(collections)}個のコレクションが見つかりました")
    
    if collections:
        st.markdown("#### コレクション一覧")
        for i, collection in enumerate(collections[:10]):  # 最初の10個を表示
            st.markdown(f"**{i+1}. {collection}**")
    
    if bands:
        st.markdown("#### 利用可能なバンド")
        st.code(", ".join(bands[:20]))  # 最初の20個を表示


def display_list_result(result: Dict[str, Any]):
    """コレクション一覧を表示"""
    if "error" in result:
        st.error(f"エラー: {result['error']}")
        return
    
    total = result.get("total_count", 0)
    st.success(f"✅ 合計 {total} 個のコレクションが利用可能です")
    
    collections = result.get("collections", [])
    if collections:
        st.markdown("#### コレクション一覧（最初の20個）")
        for i, collection in enumerate(collections[:20]):
            st.markdown(f"- {collection}")


def display_images(result: Any):
    """画像を表示"""
    if isinstance(result, list) and len(result) > 0:
        st.success(f"✅ {len(result)} 枚の画像を取得しました")
        
        for i, img in enumerate(result):
            if hasattr(img, 'data') and hasattr(img, 'format'):
                if img.format == "png":
                    st.image(img.data, caption=f"画像 {i+1}", use_container_width=True)
                else:
                    st.text(img.data.decode() if isinstance(img.data, bytes) else str(img.data))
    else:
        st.warning("画像が取得できませんでした")


def display_spatial_stats(result: Dict[str, Any]):
    """空間統計を表示"""
    if "error" in result:
        st.error(f"エラー: {result['error']}")
        return
    
    st.success("✅ 空間統計を計算しました")
    
    # 統計値を表示
    if "mean" in result:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("平均", f"{result.get('mean', 0):.2f}")
        with col2:
            st.metric("標準偏差", f"{result.get('std', 0):.2f}")
        with col3:
            st.metric("最小値", f"{result.get('min', 0):.2f}")
        with col4:
            st.metric("最大値", f"{result.get('max', 0):.2f}")
    
    st.json(result)


def display_heightmap(result: Dict[str, Any]):
    """高度マップを表示"""
    if "error" in result:
        st.error(f"エラー: {result['error']}")
        return
    
    st.success("✅ 高度マップを生成しました")
    
    if "output_path" in result:
        output_path = result["output_path"]
        if Path(output_path).exists():
            st.image(output_path, caption="生成された高度マップ", use_container_width=True)
            st.download_button(
                "📥 ダウンロード",
                data=open(output_path, "rb").read(),
                file_name=Path(output_path).name,
                mime="image/png"
            )
    
    st.json(result)
