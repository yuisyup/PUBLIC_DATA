import { useState } from "react";
import { AxiosError } from "axios";
import { searchRunResults } from "../api";
import type {
  RunResultReferenceResponse,
  RunResultReferenceSearchParams,
} from "../types/runResultReferenceTypes";

export function useRunResultReference() {
  const [result, setResult] = useState<RunResultReferenceResponse>();
  const [isLoading, setIsLoading] = useState(false);

  async function search(params: RunResultReferenceSearchParams) {
    setIsLoading(true);
    try {
      const data = await searchRunResults(params);
      setResult(data);
      return data;
    } catch (error) {
      if (error instanceof AxiosError && error.response?.data) {
        const data = error.response.data as RunResultReferenceResponse;
        setResult(data);
        return data;
      }
      throw error;
    } finally {
      setIsLoading(false);
    }
  }

  function clear() {
    setResult(undefined);
  }

  return { search, clear, result, isLoading };
}
