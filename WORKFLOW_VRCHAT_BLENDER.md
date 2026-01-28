# VRChat/Blender向けワークフローガイド

このガイドでは、JAXA Earth APIの衛星データを使用してVRChatワールドを作成するための詳細なワークフローを説明します。

## 目次

1. [概要](#概要)
2. [準備](#準備)
3. [Blenderを使用したワークフロー](#blenderを使用したワークフロー)
4. [Unityを使用したワークフロー](#unityを使用したワークフロー)
5. [VRChatへのアップロード](#vrchatへのアップロード)
6. [トラブルシューティング](#トラブルシューティング)

## 概要

このワークフローでは、以下の手順でVRChatワールドを作成します：

1. **データ取得**: JAXA Earth APIから衛星データを取得
2. **地形生成**: 高度マップとテクスチャを生成
3. **3Dモデル化**: BlenderまたはUnityで地形を3Dモデル化
4. **最適化**: VRChatの制約に合わせて最適化
5. **アップロード**: VRChatにワールドをアップロード

## 準備

### 必要なソフトウェア

- **Blender** 3.0以上（Blenderワークフローを使用する場合）
- **Unity** 2019.4以上（Unityワークフローを使用する場合）
- **VRChat SDK3**（VRChatにアップロードする場合）
- **Cursor IDE** または **Codex IDE**（MCPサーバーを使用する場合）

### 必要なデータ

- 地形を作成したい地域の座標（経度・緯度）
- 希望する解像度と範囲

## Blenderを使用したワークフロー

### ステップ1: 高度マップの生成

Cursor IDEまたはCodex IDEで、以下のコマンドを実行します：

```
富士山周辺（経度138.5-139度、緯度35.2-35.5度）の高度マップを生成してください
```

または、より詳細に指定する場合：

```
generate_heightmap ツールを使用して、以下のパラメータで高度マップを生成してください：
- collection: JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global
- bounds: [138.5, 35.2, 139.0, 35.5]
- resolution: 20.0
- output_path: ./output/fuji_heightmap.png
```

生成されたファイル：
- `heightmap.png`: 16bitグレースケールの高度マップ

### ステップ2: テクスチャの生成

```
export_texture_maps ツールを使用して、同じ範囲のテクスチャマップを生成してください：
- collection: JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global
- bounds: [138.5, 35.2, 139.0, 35.5]
- resolution: 20.0
- output_dir: ./output/textures
```

生成されたファイル：
- `diffuse.png`: 基本テクスチャ（Diffuseマップ）
- `normal.png`: 法線マップ（Normalマップ）

### ステップ3: Blenderでの地形作成

#### 3.1 プロジェクトのセットアップ

1. Blenderを起動
2. 新しいプロジェクトを作成
3. デフォルトのCubeを削除（Xキー → Delete）

#### 3.2 平面の作成

1. **Shift + A** → **Mesh** → **Plane** を選択
2. 平面を選択した状態で、**Tab**キーで編集モードに切り替え
3. **A**キーで全選択
4. **Subdivide**（右クリックメニューまたは**W**キー → **Subdivide**）を実行
   - 分割数を適切に設定（例: 100x100）
   - より詳細な地形が必要な場合は、分割数を増やす

#### 3.3 Displace Modifierの追加

1. 平面を選択した状態で、**Modifier Properties**（スパナアイコン）を開く
2. **Add Modifier** → **Displace** を選択
3. **Texture**セクションで、**New**をクリック
4. 生成した`heightmap.png`を読み込む：
   - **Open**をクリック
   - `heightmap.png`を選択
5. **Strength**を調整（例: 0.5〜2.0）
   - 値が大きいほど、地形の起伏が大きくなります
6. **Apply**をクリックしてModifierを適用

#### 3.4 テクスチャの適用

1. **Material Properties**（球アイコン）を開く
2. **New**をクリックして新しいマテリアルを作成
3. **Base Color**の横の点をクリック → **Image Texture**を選択
4. 生成した`diffuse.png`を読み込む
5. **UV Editing**ワークスペースに切り替え
6. **UV** → **Unwrap** → **Smart UV Project**を実行
7. **Shading**ワークスペースに戻り、マテリアルを確認

#### 3.5 法線マップの適用（オプション）

1. マテリアルエディタで、**Add** → **Vector** → **Normal Map**を追加
2. **Normal Map**ノードの**Color**に、`normal.png`を接続
3. **Normal Map**ノードの出力を、**Principled BSDF**の**Normal**に接続

#### 3.6 地形の最適化

1. **Edit Mode**に切り替え（**Tab**キー）
2. **Decimate Modifier**を追加：
   - **Modifier Properties** → **Add Modifier** → **Decimate**
   - **Ratio**を調整してポリゴン数を削減
   - VRChatの推奨: 100,000ポリゴン以下
3. **Apply**をクリック

#### 3.7 スケールの調整

1. 地形のサイズを確認
2. 必要に応じて、**Object Mode**で**S**キーを押してスケールを調整
3. **Apply** → **Scale**を実行

### ステップ4: Unityへのエクスポート

#### 4.1 FBX形式でエクスポート

1. 地形を選択
2. **File** → **Export** → **FBX (.fbx)**
3. 以下の設定を確認：
   - **Selected Objects**: チェック
   - **Scale**: 1.00
   - **Apply Transform**: チェック
4. ファイル名を指定して保存（例: `terrain.fbx`）

#### 4.2 テクスチャファイルのコピー

Unityプロジェクトに以下のファイルをコピー：
- `diffuse.png`
- `normal.png`
- `terrain.fbx`

## Unityを使用したワークフロー

### ステップ1: 地形データの生成

Cursor IDEまたはCodex IDEで、以下のコマンドを実行します：

```
export_to_unity ツールを使用して、以下のパラメータで地形データを生成してください：
- collection: JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global
- bounds: [138.5, 35.2, 139.0, 35.5]
- resolution: 20.0
- output_dir: ./output/unity_terrain
```

生成されたファイル：
- `terrain.raw`: Unity Terrain Tool用の高度データ
- `terrain_texture.png`: テクスチャマップ
- `terrain_metadata.json`: メタデータ（幅、高さ、高度範囲など）

### ステップ2: Unityプロジェクトのセットアップ

1. Unityを起動
2. 新しいプロジェクトを作成（3Dテンプレート推奨）
3. VRChat SDK3をインポート（まだの場合）

### ステップ3: Terrainの作成

1. **Hierarchy**で右クリック → **3D Object** → **Terrain**
2. Terrainオブジェクトを選択
3. **Terrain Settings**（歯車アイコン）を開く

### ステップ4: 高度データのインポート

1. **Terrain Settings**で、**Import Raw**をクリック
2. 生成した`terrain.raw`を選択
3. `terrain_metadata.json`を参照して、以下の設定を入力：
   - **Width**: メタデータの`width`値
   - **Height**: メタデータの`height`値
   - **Depth**: 16（16bit）
   - **Byte Order**: Windows（リトルエンディアン）
4. **Import**をクリック

### ステップ5: テクスチャの適用

1. **Terrain Settings**で、**Paint Texture**（ブラシアイコン）を選択
2. **Edit Textures** → **Add Texture**
3. 生成した`terrain_texture.png`を選択
4. **Add**をクリック

### ステップ6: Terrainの最適化

1. **Terrain Settings**で、**Terrain Resolution**を調整：
   - **Terrain Width**: 必要に応じて縮小
   - **Terrain Height**: 必要に応じて縮小
   - **Detail Resolution**: パフォーマンスに応じて調整
2. **Detail Objects**を削減（必要に応じて）

## VRChatへのアップロード

### ステップ1: VRChat SDK3の設定

1. Unityで、**VRChat SDK** → **Show Control Panel**を開く
2. **Builder**タブを選択
3. **Build & Publish**をクリック

### ステップ2: ワールドの最適化確認

VRChatの推奨設定を確認：

- **ポリゴン数**: 100,000以下
- **テクスチャサイズ**: 2048x2048以下
- **ワールドサイズ**: 100MB以下
- **Draw Calls**: 最小化

### ステップ3: ビルドとアップロード

1. **Build & Publish**をクリック
2. ビルドが完了したら、VRChatにアップロード
3. ワールドをテストして、パフォーマンスを確認

## トラブルシューティング

### 問題1: 地形が平らに見える

**原因**: Displace ModifierのStrengthが低い、または高度マップの値が正規化されていない

**解決方法**:
- Displace Modifierの**Strength**を増やす
- 高度マップの生成時に、高度範囲を確認

### 問題2: テクスチャが正しく表示されない

**原因**: UVマッピングが正しく設定されていない

**解決方法**:
- Blenderで**Smart UV Project**を再実行
- UVマップを手動で調整

### 問題3: ポリゴン数が多すぎる

**原因**: 解像度が高すぎる、または分割数が多すぎる

**解決方法**:
- `create_vrchat_terrain`ツールを使用して、事前に最適化
- Blenderで**Decimate Modifier**を使用
- Unityで**Terrain Resolution**を調整

### 問題4: UnityでTerrainが正しくインポートされない

**原因**: .rawファイルの形式が正しくない

**解決方法**:
- `terrain_metadata.json`の情報を確認
- **Byte Order**を確認（Windows = リトルエンディアン）
- **Depth**を確認（16bit）

## 参考資料

- [Blender公式ドキュメント](https://docs.blender.org/)
- [Unity Terrain公式ドキュメント](https://docs.unity3d.com/Manual/terrain-UsingTerrains.html)
- [VRChatワールド制作ガイド](https://docs.vrchat.com/docs/world-creation)
- [JAXA Earth API公式ドキュメント](https://data.earth.jaxa.jp/api/python/)

## サンプルプロジェクト

サンプルプロジェクトは`examples/`ディレクトリにあります。

- `examples/blender/`: Blenderプロジェクトのサンプル
- `examples/unity/`: Unityプロジェクトのサンプル
- `examples/output/`: 生成された地形データのサンプル
