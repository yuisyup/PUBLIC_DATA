from typing import *

class RegisterResultUtil:

    def merge_register_result(
        self,
        success: int,
        failure: int,
        insert_errors: List[Dict[str, Any]],
        unresolved_logs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        成功件数・失敗件数・エラーリスト（登録時）・未解決ログ（FK解決時）を統合したresult辞書を返す。

        :param success: 成功件数
        :param failure: 失敗件数（FK未解決と登録時例外の合計）
        :param insert_errors: 登録処理時のエラーログ（例外）
        :param unresolved_logs: FK未解決のエラーログ
        :return: 統合された結果辞書
        """
        return {
            "success": success,
            "failure": failure,
            "errors": unresolved_logs + insert_errors
        }
