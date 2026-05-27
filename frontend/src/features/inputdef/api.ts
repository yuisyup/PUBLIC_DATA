import { apiClient } from "../../lib/axios";
import { API_PATHS } from "../../lib/apiPaths";

import type { InputDefinition, InputType } from "./types/inputDefTypes";

type ListResponse<T> = {
  results: T[];
};

/**
 * 入力データ種別を全件取得する。
 *
 * @returns
 */
export async function fetchInputTypes(): Promise<InputType[]> {
  const res = await apiClient.get<ListResponse<InputType>>(
    API_PATHS.inputDef.inputTypes,
  );

  return res.data.results;
}

/**
 * 入力データ種別を基に、入力データ定義を取得する。
 *
 * @param inputType 入力データ種別
 * @returns
 */
export async function fetchInputDefinitions(
  inputType: string,
): Promise<InputDefinition[]> {
  const res = await apiClient.get<ListResponse<InputDefinition>>(
    API_PATHS.inputDef.inputDefs,
    {
      params: {
        input_type: inputType,
      },
    },
  );

  return res.data.results;
}
