# Project Overview 概要

このプロジェクトは React / TypeScript / Django を用いた観測基盤である。

# Design Philosophy 全体の設計哲学

- 本プロジェクトは「観測」をテーマとしたデータ登録基盤である。
- 登録においては、「入力データ定義」という独自概念を用いる。CSV、EXCEL、外部 API、画面入力等の入力元に対して、どのようにデータを取り込み、どのような登録処理に流すかを定義する。
- 入力データ定義では、少なくとも以下の概念を扱う。
  - 入力データ種別: CSV、EXCEL、API、画面入力等、データ元の種別を表す。
  - 登録ポリシー: INSERT、UPSERT 等、DB 状態に応じた登録方針を表す。
- 観測、蓄積したデータは分析の基盤となる。
- RunResult は実行結果の監査証跡であり、Issue は処理中に発生した事象である。
- Issue はエラーだけでなく、業務上の警告や補足情報も表現する。
- RunResult は行単位・処理単位で発生した Issue 群を集約した上位概念であり、実行全体のサマリーとして扱う。

## Architecture(front) フロントコード設計

### 使用する言語、ライブラリ

- TypeScript
- React
- react-bootstrap
- react-hook-form
- zod
- zustand
- axios
- msw

### 役割分担の基本方針

- 画面は `pages` を入口にし、ページ固有の業務 UI は `features` に閉じ込める。
- 複数画面で使い回す UI 部品は `components` に置き、業務知識を持たせすぎない。
- API 呼び出しは `api` または `lib` に寄せ、コンポーネント内部に通信詳細を広げすぎない。
- フォーム入力は `react-hook-form` を基本とし、入力値検証は `zod` に集約する。
- グローバル共有が必要な状態だけを `zustand` で持ち、画面ローカル状態はコンポーネント内に留める。
- モックは `mocks` に隔離し、開発用挙動を本番コードに混在させない。

### ルートから見たディレクトリと概要

- `./frontend/src/components`
  - ページ横断で再利用する汎用コンポーネントを置く。
- `./frontend/src/pages`
  - ルーティング単位のページコンポーネントを置く。
- `./frontend/src/features`
  - 機能単位の UI、hooks、schema、types、store、api をまとめる。
- `./frontend/src/routes`
  - React Router の定義を置く。
- `./frontend/src/api`
  - ページ横断で利用する API 呼び出しを置く。
- `./frontend/src/lib`
  - axios クライアント、API パス、通信共通処理を置く。
- `./frontend/src/stores`
  - アプリ全体で共有する状態を置く。
- `./frontend/src/mocks`
  - msw の browser, handlers, response 定義を置く。
- `./frontend/src/types`
  - ページ横断で利用する型定義を置く。

### フロント実装時の判断基準

- `pages` には画面構成と feature の組み合わせ責務を持たせ、細かい業務ロジックは置きすぎない。
- `features` では「その機能に閉じる UI / hooks / schema / types / store」を近接配置する。
- バリデーションは画面 submit 時に散らさず、schema に寄せて一元管理する。
- API レスポンス型は feature 側で明示し、曖昧な `any` で吸収しない。
- 一覧・結果表示は、入力フォームと責務が分かれるならコンポーネントを分離する。
- 大量件数を扱う結果表示では、集計・サマリー・表示上限を意識し、入力画面を過積載にしない。

## Architecture(back) バックコード設計

### 使用する言語、ライブラリ

- Python
- Django
- pytest
- MySQL
- pandas

### 役割分担の基本方針

- Django の View は HTTP 入出力の受け口に留め、業務処理本体を直接抱え込まない。
- API Handler はリクエスト単位の実行制御を担い、Usecase 呼び出し、RunResult 生成、レスポンス変換を行う。
- Usecase は業務フローの主線を持ち、Processor 群を組み合わせて登録処理を完結させる。
- Processor は抽出、正規化、補完、登録のような手続き的処理を責務ごとに分割する。
- Domain は DTO、Issue、RunResult、定義解釈など、業務概念とルールを表現する。
- Infra は Django ORM、外部入力、永続化、動的 import 等の技術詳細を引き受ける。
- View / API から Domain に向かうほど Django 依存を薄くし、内側の層ほど再利用しやすく保つ。

### ルートから見たディレクトリと概要

- `./common/views`
  - Django View と画面描画向け補助処理を置く。
- `./common/views/api`
  - API エンドポイント、serializer、レスポンス変換を置く。
- `./common/services/api`
  - API Handler を置き、Usecase 実行から RunResult 永続化までを束ねる。
- `./common/services/usecase`
  - ユースケース本体を置く。
- `./common/services/processor`
  - extractor、normalizer、loader 等の処理ステップを置く。
- `./common/services/domain`
  - 入力定義解釈、RunResult 生成などの業務寄りロジックを置く。
- `./common/services/infra`
  - repository、persister、reader、registry 等の技術詳細を置く。
- `./common/issue`
  - Issue と RunResult の DTO、および関連コード定義を置く。
- `./common/models.py`
  - Django ORM モデルを置く。
- `./common/tests`
  - API Handler を中心とした pytest を置く。

### バック実装時の判断基準

- HTTP 都合の分岐と業務ロジックの分岐を同じ層に混在させない。
- Usecase の戻り値は、可能な限り Issue や DTO のような業務表現で返す。
- 例外は握り潰さず、必要に応じて Issue に変換して RunResult に集約する。
- 永続化の詳細は Infra に閉じ込め、Usecase から ORM 直書きを増やさない。
- Factory / Registry の責務は「定義に応じた実装選択」に限定し、過剰な業務判断を持たせない。
- 行単位の結果は Issue、実行単位の監査は RunResult で表現する方針を崩さない。

## Additional Guidance 補助ルールと概要

### Naming / Responsibility

- 名前は技術名より責務を優先し、何をするクラス・関数なのかが分かる命名にする。
- 1 ファイル 1 責務を厳密に求めすぎないが、変更理由が複数に割れる単位には肥大化させない。

### Error Handling

- 想定内の業務異常は Issue またはアプリケーション例外で扱い、単なる文字列エラーで流さない。
- UI 向け文言、監査向け情報、開発者向け詳細を必要に応じて分離する。

### API Boundary

- フロントとバックの境界では、リクエスト・レスポンスの型や DTO を明示する。
- エンドポイント追加時は、成功形だけでなく Issue を含む失敗形・警告形の返却も先に意識する。

### State Management

- フロントでは「一時入力状態」「画面ローカル状態」「複数画面共有状態」を分けて考える。
- バックでは「入力値」「途中生成物」「永続化対象 DTO」を混同しない。

### Observability

- 監査上重要な処理は、最終成否だけでなく、どの行で何が起きたかを追える構造にする。
- RunResult / Issue を壊さない変更を優先し、後追い分析可能性を落とさない。

## Coding Rules

- DTO は `dataclass` を基本とする。
- Repository は `Infra` に置く。
- Domain は Django に依存させない。
- 型定義を省略しすぎず、境界では入出力を明示する。
- 共通化は重複が 1 回あるだけで急がず、責務が固まってから行う。

## Test Rules

- `pytest` を利用する。
- 正常系・異常系を最低 1 ケースずつ作成する。
- API Handler のテストでは、成功レスポンスだけでなく Issue / RunResult への変換結果も確認する。
- Usecase / Processor のテストでは、分岐ごとの Issue 発生条件を明示的に検証する。
- monkeypatch する場合は、実行時に参照されるモジュール名前空間を正しく差し替える。
