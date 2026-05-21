import type { bulkRegisterResponse } from "./types/bulkRegisterTypes";
import { API_PATHS } from "./../../lib/apiPaths";
import { apiClient } from "./../../lib/axios";

/**
 * 添付ファイルの内容を、入力定義IDの内容に従いアップロードする。
 *
 * @param params 1.入力定義ID(number) / 2.ファイルデータ(file)
 * @returns bulkRegisterResponse
 */
export async function uploadBulkRegisterFile(params: {
  inputDefId: number;
  file: File;
}): Promise<bulkRegisterResponse> {
  const formData = new FormData();

  formData.append("inputDefId", String(params.inputDefId));
  formData.append("file", params.file);

  const res = await apiClient.post<bulkRegisterResponse>(
    API_PATHS.bulkRegister.register,
    formData,
    {
      headers: {
        "Content-Type": undefined,
      },
    },
  );

  return res.data;
}
