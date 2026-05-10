import { apiClient } from "./client";
import type { InputDefinition } from "../types/InputDef";

type InputDefinitionResponse = {
    results: InputDefinition[];
};

export async function fetchInputDefinitions(
    inputType: string
): Promise<InputDefinition[]> {
    const response = await apiClient.get<InputDefinitionResponse>(
        "/common/input-definitions/",
        {
            params: {
                input_type: inputType,
            },
        }
    );

    return response.data.results;
}