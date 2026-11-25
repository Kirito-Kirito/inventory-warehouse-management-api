# 在庫管理バックエンドAPI

**Django** および **Django REST Framework (DRF)** を用いて構築した、在庫、商品、カテゴリー、仕入先、倉庫、および在庫移動（`IN` / `OUT` / `ADJUSTMENT`）を管理するための RESTful バックエンド API です。

## 主な機能

- **JWT 認証**: `djangorestframework-simplejwt` によるトークンベースの認証。
- **ロールベースアクセス制御（RBAC）**: カスタムユーザーロール（`ADMIN`、`MANAGER`、`STAFF`）に応じたきめ細かな ViewSet 権限設定：
  - `Supplier`、`Category`、`Warehouse`、`Stock Movement` エンドポイントには `IsStaffOrReadOnly` を適用。
  - `Product` エンドポイントには `IsAuthenticatedDeleteStaffOnly` を適用（認証済みユーザーは作成・参照・更新が可能で、`DELETE` はスタッフ／スーパーユーザーのみに制限）。
- **在庫移動バリデーション**: 在庫 `IN` および `OUT` 操作のエッジケース検証に対応（マイナス在庫、0以下の数量、利用可能在庫を超える出庫などを防止）。
- **環境変数による設定管理**: `SECRET_KEY`、`DEBUG`、`ALLOWED_HOSTS` などの機密・環境依存設定をローカルの `.env` ファイルから読み込み。
- **インタラクティブ API ドキュメント**: `drf-spectacular` による OpenAPI スキーマ、Swagger UI、ReDoc の提供。
- **ユニット＆結合テスト**: 権限、JWT 認証、在庫 `OUT` のエッジケースなどを網羅した自動 API テスト。

## 使用技術

- **言語**: Python
- **フレームワーク**: Django, Django REST Framework
- **認証**: `djangorestframework-simplejwt`
- **API スキーマ＆ドキュメント**: `drf-spectacular`
- **データベース**: SQLite（ローカル開発環境）

## プロジェクト構成（概要）

- `config/` — プロジェクト設定、ルート URL、環境変数読み込み
- `account/` — カスタムユーザーモデル、ロール、認証処理
- `inventory/` — カテゴリー、仕入先、倉庫、商品の管理
- `transactions/` — 在庫移動（`IN` / `OUT` / `ADJUSTMENT`）のロジックおよびエンドポイント

## API エンドポイント一覧

| カテゴリ | メソッド | エンドポイント | アクセス / 権限 | 概要 |
| :--- | :--- | :--- | :--- | :--- |
| **認証** | `POST` | `/api/token/` | 公開 | JWT アクセストークン・リフレッシュトークンの取得 |
| **認証** | `POST` | `/api/token/refresh/` | 公開 | 期限切れアクセストークンの更新 |
| **商品** | `GET` | `/api/v1/products/` | 認証済み / 読み取り | 全商品の一覧取得 |
| **商品** | `POST` | `/api/v1/products/` | 認証済み | 新規商品の作成 |
| **商品** | `PUT` / `PATCH` | `/api/v1/products/{id}/` | 認証済み | 既存商品の更新 |
| **商品** | `DELETE` | `/api/v1/products/{id}/` | スタッフ / スーパーユーザーのみ | 商品の削除 |
| **カテゴリー** | `GET` / `POST` / `PUT` / `DELETE` | `/api/v1/categories/` | 書き込みはスタッフのみ、その他は読み取り専用 | 商品カテゴリーの管理 |
| **仕入先** | `GET` / `POST` / `PUT` / `DELETE` | `/api/v1/suppliers/` | 書き込みはスタッフのみ、その他は読み取り専用 | 仕入先の管理 |
| **倉庫** | `GET` / `POST` / `PUT` / `DELETE` | `/api/v1/warehouses/` | 書き込みはスタッフのみ、その他は読み取り専用 | 倉庫の管理 |
| **在庫移動** | `GET` / `POST` | `/api/v1/movements/` | 書き込みはスタッフのみ、その他は読み取り専用 | 在庫 `IN` / `OUT` / `ADJUSTMENT` 移動の記録 |

### 認証ヘッダーの例

保護されたエンドポイントへのリクエストには、`Authorization` ヘッダーに JWT の `access` トークンを含めてください：

```http
Authorization: Bearer <your_access_token>
```
## ローカル環境のセットアップとインストール

### 1. リポジトリのクローンと仮想環境の作成

```bash
git clone <your-repository-url>
cd <your-project-folder>
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate
```

### 2. 依存パッケージのインストール
```bash
pip install -r requirements.txt
```

### 3. 環境変数の設定
プロジェクトルートに .env ファイルを作成してください（.env は Git にコミットしないでください）：

```env
SECRET_KEY=replace-with-your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 4. マイグレーションの実行と開発サーバーの起動
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## API ドキュメント
サーバー起動後、以下の URL からインタラクティブなドキュメントにアクセスできます：

- Swagger UI: http://127.0.0.1:8000/api/docs/

- ReDoc: http://127.0.0.1:8000/api/redoc/

- OpenAPI Schema: http://127.0.0.1:8000/api/schema/

## テストの実行
詳細なログ付きでテストスイートを実行します：

```bash
python manage.py test inventory
python manage.py test -v 2
```