from django.db import models
import uuid

"""
ーーーーーーーーーーーーーーーーーーーーーーー
国・地域マスタ
ーーーーーーーーーーーーーーーーーーーーーーー
"""


# 国マスタ
class MsCountry(models.Model):
    country_code = models.CharField(primary_key=True, max_length=2)
    country_name_ja = models.CharField(max_length=40, blank=True, null=True)
    country_name_en = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return str(self.country_code) + " : " + str(self.country_name_ja)

    class Meta:
        db_table = "ms_country"
        verbose_name = "国マスタ"
        verbose_name_plural = "国マスタ"


# 地域マスタ
class MsRegion(models.Model):
    country = models.ForeignKey(MsCountry, on_delete=models.CASCADE)
    region_code = models.CharField(max_length=6)
    region_name_ja = models.CharField(max_length=100)
    region_name_en = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.region_code) + " : " + str(self.region_name_ja)

    class Meta:
        db_table = "ms_region"
        verbose_name = "地域マスタ"
        verbose_name_plural = "地域マスタ"
        unique_together = ("country", "region_code")


"""
ーーーーーーーーーーーーーーーーーーーーーーー
入力データ定義マスタ
ーーーーーーーーーーーーーーーーーーーーーーー
"""


class MsRegisterPolicy(models.Model):
    policy_code = models.CharField(max_length=10, primary_key=True)
    policy_name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    policy_processor_class_path = models.CharField(max_length=300)

    def __str__(self):
        return str(self.policy_code) + " : " + str(self.policy_name)

    class Meta:
        db_table = "ms_register_policy"
        verbose_name = "データ登録/更新ポリシーマスタ"
        verbose_name_plural = "データ登録/更新ポリシーマスタ"


class MsInputType(models.Model):
    input_type_code = models.CharField(max_length=10, primary_key=True)
    input_type_name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    input_type_usecase_class_path = models.CharField(max_length=300)

    def __str__(self):
        return str(self.input_type_code) + " : " + str(self.input_type_name)

    class Meta:
        db_table = "ms_input_type"
        verbose_name = "データ入力種別マスタ"
        verbose_name_plural = "データ入力種別マスタ"


class MsInputDef(models.Model):
    input_id = models.AutoField(primary_key=True)
    input_name = models.CharField(max_length=40)
    target_model_name = models.CharField(max_length=40)
    input_type = models.ForeignKey(
        MsInputType, on_delete=models.PROTECT, db_column="input_type_code"
    )
    delimiter = models.CharField(max_length=5, null=True, blank=True)
    has_header = models.BooleanField(null=True, blank=True)
    register_policy = models.ForeignKey(
        MsRegisterPolicy, on_delete=models.PROTECT, db_column="policy_code"
    )
    insert_duplication_lookup_fields = models.JSONField(null=True, blank=True)

    def __str__(self):
        return str(self.input_name) + " : TO " + str(self.target_model_name)

    class Meta:
        db_table = "ms_input_def"
        verbose_name = "データ入力定義マスタ"
        verbose_name_plural = "データ入力定義マスタ"


class MsInputColumnDef(models.Model):
    input_id = models.ForeignKey(
        MsInputDef, on_delete=models.CASCADE, db_column="input_id"
    )
    column_order = models.PositiveSmallIntegerField()
    input_source_key = models.CharField(max_length=40)
    model_target_field_name = models.CharField(max_length=40, null=True, blank=True)
    is_fk_flag = models.BooleanField()
    is_lookup_only = models.BooleanField(default=False)
    input_lookup_fields = models.JSONField(null=True, blank=True)
    fk_target_model = models.CharField(max_length=40, null=True, blank=True)
    fk_target_field = models.CharField(max_length=40, null=True, blank=True)
    fk_lookup_fields = models.JSONField(null=True, blank=True)
    display_name = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return (
            str(self.input_id.input_name)
            + " : "
            + str(self.column_order)
            + " : "
            + str(self.display_name)
        )

    class Meta:
        db_table = "ms_input_column_def"
        verbose_name = "データ入力定義カラムマスタ"
        verbose_name_plural = "データ入力定義カラムマスタ"
        unique_together = ("input_id", "column_order")


class MsInputNormilizerStepDef(models.Model):
    """
    入力定義ごとの前処理定義（子テーブル）
    - 1行 = 1つの前処理
    - seq順に適用
    """

    input_id = models.ForeignKey(
        MsInputDef, on_delete=models.CASCADE, db_column="input_id"
    )
    seq = models.PositiveIntegerField(default=1)
    normalizer_step_key = models.CharField(max_length=100)

    is_enabled = models.BooleanField(default=True)

    # 将来用（いまは未使用でもOK）
    params_json = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ms_input_normilizer_step_def"
        indexes = [
            models.Index(fields=["input_id", "seq"]),
        ]
        unique_together = [
            ("input_id", "seq"),
        ]
        verbose_name = "データ入力定義前処理マスタ"
        verbose_name_plural = "データ入力定義前処理マスタ"

    def __str__(self) -> str:
        return f"{self.input_id}:{self.seq}:{self.normalizer_step_key}"


"""
ーーーーーーーーーーーーーーーーーーーーーーー
処理実行結果管理テーブル
ーーーーーーーーーーーーーーーーーーーーーーー
"""


class RunResultRecord(models.Model):
    """
    RunResult（実行1回）の永続化モデル
    - DTO: RunResult（run_result_dto.py）を保存する
    - DTOのrun_id(UUID)をそのままPKにする
    """

    run_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # context
    mode = models.CharField(max_length=20)  # "SCREEN" etc
    source = models.CharField(max_length=20)  # "CSV" etc
    input_def_id = models.CharField(max_length=50, null=True, blank=True)
    csv_def_id = models.CharField(max_length=50, null=True, blank=True)
    target_model = models.CharField(max_length=200, null=True, blank=True)
    executed_by = models.CharField(max_length=100, null=True, blank=True)
    invoked_by = models.CharField(max_length=100, null=True, blank=True)
    input_name = models.CharField(max_length=255, null=True, blank=True)
    input_fingerprint = models.CharField(max_length=128, null=True, blank=True)
    tags_json = models.JSONField(null=True, blank=True)

    # timing
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField(null=True, blank=True)
    duration_ms = models.IntegerField(null=True, blank=True)

    # status
    status = models.CharField(max_length=30)  # "SUCCESS" / "FAILED" / ...

    # counts（必要なものだけから開始でOK）
    total_rows = models.IntegerField(default=0)
    parsed_rows = models.IntegerField(default=0)
    fk_resolved_rows = models.IntegerField(default=0)
    processed_rows = models.IntegerField(default=0)
    inserted_rows = models.IntegerField(default=0)
    updated_rows = models.IntegerField(default=0)
    skipped_rows = models.IntegerField(default=0)
    error_rows = models.IntegerField(default=0)

    info_count = models.IntegerField(default=0)
    warn_count = models.IntegerField(default=0)
    error_count = models.IntegerField(default=0)

    # summary
    summary_message = models.TextField(null=True, blank=True)
    exception_type = models.CharField(max_length=200, null=True, blank=True)
    exception_message = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tr_run_result"
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["status"]),
            models.Index(fields=["input_def_id"]),
        ]
        verbose_name = "処理実行結果管理"
        verbose_name_plural = "処理実行結果管理"

    def __str__(self) -> str:
        return f"【{self.created_at}】 {self.run_id} : {self.summary_message}"


class IssueRecord(models.Model):
    """
    Issue（1件）の永続化モデル
    - DTO: Issue（dataclass）を保存する
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    run = models.ForeignKey(
        RunResultRecord,
        on_delete=models.CASCADE,
        related_name="issues",
        db_index=True,
    )

    domain = models.CharField(max_length=50)
    phase = models.CharField(max_length=100)
    severity = models.CharField(max_length=10)  # INFO/WARN/ERROR
    code = models.CharField(max_length=200)

    row_index = models.IntegerField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    skip_scope = models.CharField(max_length=20, default="NONE")  # NONE/ROW/ALL

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tr_issue"
        indexes = [
            models.Index(fields=["severity"]),
            models.Index(fields=["code"]),
            models.Index(fields=["phase"]),
        ]
        verbose_name = "処理実行結果管理詳細"
        verbose_name_plural = "処理実行結果管理詳細"

    def __str__(self) -> str:
        return f"【{self.created_at}】{self.run.run_id} : {self.phase} : {self.severity} : {self.code}"


class IssueContextRecord(models.Model):
    """
    Issue.context（dict）を正規化保存する子テーブル
    - key 単位で1行
    - 値は text と json を併用（どちらか埋める）
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    issue = models.ForeignKey(
        IssueRecord,
        on_delete=models.CASCADE,
        related_name="contexts",
        db_index=True,
    )

    key = models.CharField(max_length=100)
    value_text = models.TextField(null=True, blank=True)
    value_json = models.JSONField(null=True, blank=True)

    # 監査
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tr_issue_context"
        indexes = [
            models.Index(fields=["key"]),
        ]
        verbose_name = "処理実行結果管理詳細コンテキスト"
        verbose_name_plural = "処理実行結果詳細コンテキスト"

    def __str__(self) -> str:
        return f"【{self.created_at}】{self.issue.id} : {self.key} : {self.value_text}"


"""
ーーーーーーーーーーーーーーーーーーーーーーー
テスト用テーブル
ーーーーーーーーーーーーーーーーーーーーーーー
"""


class TestNameList(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, null=True, blank=True)
    born_in = models.DateField(null=True, blank=True)
    country = models.ForeignKey(
        MsCountry, on_delete=models.CASCADE, db_column="country_code"
    )
    execute_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "test_name_list"
        verbose_name = "テスト用名簿"
        verbose_name_plural = "テスト用名簿"
