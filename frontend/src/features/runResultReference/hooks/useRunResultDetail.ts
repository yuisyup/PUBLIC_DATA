import { useEffect, useState } from "react";
import { AxiosError } from "axios";
import { fetchRunResultDetail } from "../api";
import type { RunResultReferenceDetailResponse } from "../types/runResultReferenceTypes";

export function useRunResultDetail(runId?: string) {
  const [detail, setDetail] = useState<RunResultReferenceDetailResponse>();
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (!runId) {
      return;
    }

    let ignore = false;
    const targetRunId = runId;

    async function load() {
      setIsLoading(true);
      try {
        const data = await fetchRunResultDetail(targetRunId);
        if (!ignore) {
          setDetail(data);
        }
      } catch (error) {
        if (
          error instanceof AxiosError &&
          error.response?.data &&
          !ignore
        ) {
          setDetail(error.response.data as RunResultReferenceDetailResponse);
          return;
        }
        if (!ignore) {
          setDetail({
            success: false,
            runResult: null,
            issues: [],
            issuesForError: [
              {
                severity: "ERROR",
                phase: "RUN_RESULT_REFERENCE_DETAIL.GET",
                code: "RUN_RESULT_REFERENCE_DETAIL.NETWORK_ERROR",
                row: null,
                message: "詳細取得でエラーが発生しました。",
                skip: "ALL",
                context: null,
              },
            ],
          });
        }
      } finally {
        if (!ignore) {
          setIsLoading(false);
        }
      }
    }

    load();

    return () => {
      ignore = true;
    };
  }, [runId]);

  return { detail: runId ? detail : undefined, isLoading };
}
