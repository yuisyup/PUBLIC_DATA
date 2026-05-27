export type IssueSeverity = "ERROR" | "WARNING" | "INFO";

export type IssuePhase =
  | "GET_REGISTER_USECASE"
  | "EXTRACT"
  | "NORMALIZE"
  | "LOAD"
  | string;

export type SkipScope = "NONE" | "ROW" | "COLUMN" | "ALL";

export type bulkRegisterStatus =
  | "SUCCESS"
  | "SUCCESS_WITH_WARN"
  | "FAILED"
  | string;

/**
 * 行レベル発生事象リスト
 */
export type IssueDto = {
  severity: IssueSeverity;
  phase: IssuePhase;
  code: string;
  row: number | null;
  message: string;
  skip: SkipScope;
  context: Record<string, unknown> | null;
};

/**
 * データ一括登録結果レスポンス
 */
export type bulkRegisterResponse = {
  success: boolean;
  runId: string;
  status: bulkRegisterStatus;
  summary: {
    totalIssues: number;
    errorCount: number;
    warningCount: number;
    infoCount: number;
  };
  issues: IssueDto[];
};
