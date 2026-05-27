import { useState } from "react";
import { uploadBulkRegisterFile } from "../api";
import type { bulkRegisterResponse } from "../types/bulkRegisterTypes";

/**
 * 一括登録のapi呼出hook
 *
 * @returns
 */
export const useBulkRegister = () => {
  /* state：処理中ローディング */
  const [isLoading, setIsLoading] = useState(false);
  /* state：処理結果 */
  const [result, setResult] = useState<bulkRegisterResponse>();

  const submit = async (file: File, inputDefId: number) => {
    setIsLoading(true);

    const params = {
      // 入力データ定義ID
      inputDefId: inputDefId,
      // ファイル
      file: file,
    };

    try {
      const data = await uploadBulkRegisterFile(params);
      setResult(data);
    } finally {
      setIsLoading(false);
    }
  };

  return { submit, result, isLoading };
};
