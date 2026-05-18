import { useState } from "react";
import { uploadBulkRegisterFile } from "../api";
import type { bulkRegisterResponse } from "../types/bulkRegisterTypes";

/**
 * 一括登録のapiを呼び出す。
 *
 * @returns
 */
export const useBulkRegister = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<bulkRegisterResponse>();

  const submit = async (file: File, inputDefId: number) => {
    setIsLoading(true);

    const params = {
      inputDefId: inputDefId,
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
