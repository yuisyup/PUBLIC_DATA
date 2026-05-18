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

export type IssueDto = {
  severity: IssueSeverity;
  phase: IssuePhase;
  code: string;
  row: number | null;
  message: string;
  skip: SkipScope;
  context: Record<string, unknown> | null;
};

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
