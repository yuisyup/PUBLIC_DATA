from typing import *
from django.db.models.query import QuerySet

from common.exceptions.app_error import FailedCreateInputDefChoicesError
from common.models import MsInputDef, MsInputColumnDef
from common.services.domain.register.dto import FkResolveSpecInput, InputDefRaw


class InputDefinitionRepository:

    def get_input_def(self, input_id: int):
        try:
            input_def: MsInputDef = MsInputDef.objects.get(pk=input_id)
        except MsInputDef.DoesNotExist:
            return None

        return input_def

    def get_input_def_as_dto(self, input_id: int) -> InputDefRaw:

        input_def: MsInputDef = self.get_input_def(input_id)

        # 取得失敗の場合
        if not input_def:
            return None

        return InputDefRaw(
            input_id=input_def.input_id,
            input_name=input_def.input_name,
            target_model_name=input_def.target_model_name,
            input_type=input_def.input_type,
            delimiter=input_def.delimiter,
            has_header=input_def.has_header,
            register_policy=input_def.register_policy,
            insert_duplication_lookup_fields=input_def.insert_duplication_lookup_fields,
            input_type_usecase_class_path=input_def.input_type.input_type_usecase_class_path,
            policy_processor_class_path=input_def.register_policy.policy_processor_class_path,
        )

    def lookup_column_defs(self, input_id: int):

        # カラム定義取得
        column_defs: QuerySet[MsInputColumnDef] = MsInputColumnDef.objects.filter(
            input_id=input_id
        ).order_by("column_order")
        if not column_defs.exists():
            return None

        return column_defs

    def lookup_column_defs_as_dto(self, input_id: int) -> List[FkResolveSpecInput]:

        # カラム定義取得
        column_defs: QuerySet[MsInputColumnDef] = self.lookup_column_defs(input_id)
        # 取得失敗の場合
        if column_defs is None:
            return None

        spec_list: List[FkResolveSpecInput] = []

        for column_def in column_defs:

            spec_input = FkResolveSpecInput(
                input_id=input_id,
                column_order=column_def.column_order,
                input_source_key=column_def.input_source_key,
                model_target_field_name=column_def.model_target_field_name,
                is_fk_flag=column_def.is_fk_flag,
                is_lookup_only=column_def.is_lookup_only,
                input_lookup_fields=column_def.input_lookup_fields,
                fk_target_model=column_def.fk_target_model,
                fk_target_field=column_def.fk_target_field,
                fk_lookup_fields=column_def.fk_lookup_fields,
                display_name=column_def.display_name,
            )
            spec_list.append(spec_input)

        return spec_list

    def get_input_def_choices_by_type(
        self, lookup: Dict[str, Any]
    ) -> List[tuple[int, str]]:
        """
        指定の条件で入力データ定義を取得し、選択肢リストとして返却する。

        :param lookup: 検索条件（カラム名, 値）
        :type lookup: Dict[str, Any]
        :return: 選択肢リスト（id, 名前）
        :rtype: List[tuple[int, str]]
        """

        try:
            input_def_list: QuerySet[MsInputDef] = MsInputDef.objects.filter(**lookup)
        except Exception as e:
            raise FailedCreateInputDefChoicesError from e

        # id, 名前でのタプルリストを返却
        choices: List[tuple[int, str]] = [
            (str(ms.input_id), str(ms.input_name)) for ms in input_def_list
        ]

        return choices
