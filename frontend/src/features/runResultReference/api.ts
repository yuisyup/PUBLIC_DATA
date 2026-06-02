import { apiClient } from "../../lib/axios";
import { API_PATHS } from "../../lib/apiPaths";
import type {
  RunResultReferenceResponse,
  RunResultReferenceSearchParams,
} from "./types/runResultReferenceTypes";

export async function searchRunResults(
  params: RunResultReferenceSearchParams,
): Promise<RunResultReferenceResponse> {
  const res = await apiClient.get<RunResultReferenceResponse>(
    API_PATHS.runResultReference.search,
    {
      params: {
        input_type: params.inputType || undefined,
        input_def_id: params.inputDefId || undefined,
        created_at: params.createdAt || undefined,
      },
    },
  );

  return res.data;
}
