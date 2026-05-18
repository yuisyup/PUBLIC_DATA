from typing import *
import traceback

from common.exceptions.register_errors import RegisterPolicyNotFoundError

from common.utils.import_utils import ImportUtils
from common.services.processor.register.loader.policy_execute.register_processor_protocol import (
    RegisterProcessorProtocol,
)
from common.services.infra.persistance.django_model_persister import ModelPersister


class PolicyProcessorFactory:

    def get_register_processor_by_policy(
        self, policy_processor_class_path: str, persister: ModelPersister
    ) -> RegisterProcessorProtocol:
        """
        データ登録・更新基幹ポリシーの実行制御インスタンスを取得

        :param policy_processor_class_path: 登録ポリシー実行クラスのパス
        :param persister: データ永続化インスタンス
        :return policy_class: 登録/更新ポリシーインスタンス
        :raise RegisterPolicyNotFoundError: マスタデータ・ポリシークラス不整合
        """

        try:
            policy_class: Type[RegisterProcessorProtocol] = ImportUtils.import_class(
                policy_processor_class_path
            )
        except (ImportError, AttributeError) as e:
            raise RegisterPolicyNotFoundError(
                context={
                    "policy_processor_class_path": policy_processor_class_path,
                    "error_message": str(e),
                    "trace": traceback.format_exc().splitlines()[-5:],
                }
            ) from e

        return policy_class(persister)
