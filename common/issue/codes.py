from typing import *

# 「系」コード
DomainCode = Literal["COMMON", "REGISTER", "REFERENCE", "ANALYZE"]

# 追加：どの局面で起きた問題か
IssuePhase = Literal[
    # ===== 共通 =====
    "UNKNOWN",
    # ===== 登録 =====
    "REGISTER.GET_USECASE",
    "REGISTER.CSV_PARSE",
    "REGISTER.EDIT_DATAFRAME_COLUMN_NAME",
    "REGISTER.NORMALIZE",
    "REGISTER.FK_RESOLVE",
    "REGISTER.GET_POLICY",
    "REGISTER.GET_TARGET_MODEL_CLASS",
    "REGISTER.VALIDATE",
    "REGISTER.POST_PROCESS",
    "REGISTER.FINISH",
]

# 発生事象コード
IssueCode = Literal[
    # ===== 共通 =====
    "COMMON.UNSPECIFIED",
    # ===== 登録 =====
    "REGISTER.SUCCESS",  # 成功
    "REGISTER.NORMALIZE_KEY_NOT_FOUND",  # 前処理キー不正
    "REGISTER.FAILED_CREATE_FK_LOOKUP_KWARGS",  # FK変換先Model検索条件の生成に失敗（カラム数不一致など）
    "REGISTER.MODEL_CLASS_NOT_FOUND",  # FK変換先Modelのクラスオブジェクトの解決に失敗
    "REGISTER.MODEL_DATA_NOT_FOUND",  # FK変換先Modelのデータ取得に失敗
    "REGISTER.AMBIGUOUS",  # FK変換先Modelの取得結果が複数県（検索条件orデータ不備）
    "REGISTER.DB_ERROR",  # DB例外
    "REGISTER.DEF_NOT_FOUND",  # 入力定義マスタ取得失敗
    "REGISTER.COLUMN_DEF_NOT_FOUND",  # 入力定義カラムマスタ取得失敗
    "REGISTER.USECASE_CLASS_NOT_FOUND",  # データ登録ユースケースクラスの解決に失敗
    "REGISTER.POLICY_CLASS_NOT_FOUND",  # データ登録ユポリシーケースクラスの解決に失敗
    "REGISTER.DEF_ERROR_INCOMPLETE",  # 入力データ定義の不備
    "REGISTER.FAILED_CREATE_DUPLICATION_LOOKUP_KWARGS",  # 入力データ定義の検索条件カラム数不一致
    "REGISTER.DUPLICATION",  # INSERT_ONLY（重複禁止）ポリシーの際の重複カラム
    "REGISTER.FAILED_REGISTER_BY_VALIDATION",  # full_clean()によるバリデーションエラー
    "REGISTER.UNEXPECTED_ERROR",  # 想定外のエラー
]

# 追加：重要度（UI表示や、成功/失敗判定で使える）
IssueSeverity = Literal["INFO", "WARN", "ERROR"]

# 追加：スキップの粒度
SkipScope = Literal[
    "NONE",  # スキップなし
    "ROW",  # 行をスキップ
    "COLUMN",  # 列ごとスキップ（FK解決の定義不備など）
    "ALL",  # 全体を中断（致命的）
]
