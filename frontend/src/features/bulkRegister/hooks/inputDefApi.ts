import { API_PATHS } from "../../../lib/apiPaths";
import { apiClient } from "../../../lib/axios";

import type { InputDefinition } from "../types/InputDef";

type InputDefinitionResponse = {
  results: InputDefinition[];
};

export async function fetchInputDefinitions(
  inputType: string,
): Promise<InputDefinition[]> {
  const response = await apiClient.get<InputDefinitionResponse>(
    API_PATHS.bulkRegister.inputDefs,
    {
      params: {
        input_type: inputType,
      },
    },
  );

  return response.data.results;
}
