# Project Overview

このプロジェクトはReact/TypeScript/Djangoを用いた観測基盤である。

# Design Philosophy

本プロジェクトは
「観測」をテーマとした
データ登録基盤である。

Issueは例外ではなく
業務上の警告も表現する。

RunResultは
実行結果の監査証跡である。

## Architecture

- common配下に業務ロジックを集約
- Usecase / Processor / Domain / Infra
- Issue / RunResultでエラー管理

## Coding Rules

- DTOは dataclass
- Repositoryは Infra
- Domainは Django依存禁止

## Test Rules

- pytest利用
- 正常系・異常系を最低1ケースずつ作成
