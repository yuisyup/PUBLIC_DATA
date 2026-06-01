# Project Overview 概要

このプロジェクトはReact/TypeScript/Djangoを用いた観測基盤である。

# Design Philosophy 全体の設計哲学

- 本プロジェクトは「観測」をテーマとした
データ登録基盤である。

- 登録においては、「入力データ定義」という独自概念を用いる。CSV、EXCELといった外部ファイル、また公開されている外部api等からどのようにデータを取り込むかを定義する(ソース上のキーワード：InputDef)。定義のための区分値として、入力データ種別(CSV、EXCEL、api、画面入力等、データ元の種別のこと)、登録ポリシー(新規のみINSERT、UPSERT等、DBの状態に応じた処理振り分けの定義)の概念を用いる。

- 観測、蓄積したデータは分析の基盤となる。

- RunResult(実行結果の監査証跡)及び、Issue(発生事象)という概念がある。主にReadのみの機能以外での使用が想定され、行単位での実行結果をIssueで管理する。Issueはエラーだけでなく、業務上の警告も表現する。RunResultは、行ごとの実行結果をサマリーとしてまとめた、Issueの上位概念である。

## Architecture(front) フロントコード設計

### 使用する言語、ライブラリ

- TypeScript
- React
- react bootstrap
- react hook form
- zod
- zustand
- axios

### ルートから見たディレクトリと概要
- ./frontend/src
  - /components ページ横断のコンポーネント
  - /pages ページファイル
  - /features ページで使用するコンポーネント、型定義等
  - /routes Reactルーター
  - /lib axiosを用いたAPI管理を集約
  - /mocks msw使用時のモック定義
  - /types ページ横断の型定義

## Architecture(back) バックコード設計

### 使用する言語、ライブラリ

- Python
- Django
- pytest
- MySQL

### ルートから見たディレクトリと概要

- .common/
- Usecase / Processor / Domain / Infra

## Coding Rules

- DTOは dataclass
- Repositoryは Infra
- Domainは Django依存禁止

## Test Rules

- pytest利用
- 正常系・異常系を最低1ケースずつ作成
