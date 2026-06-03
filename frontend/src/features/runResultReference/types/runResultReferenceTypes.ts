import type { IssueDto } from "../../bulkRegister/types/bulkRegisterTypes";

export type RunResultReferenceSearchParams = {
  inputType?: string;
  inputDefId?: string;
  createdAt?: string;
};

export type RunResultReferenceRow = {
  runId: string;
  inputDefId: string | null;
  inputDefName: string | null;
  targetModel: string | null;
  createdAt: string;
};

export type RunResultReferenceResponse = {
  success: boolean;
  results: RunResultReferenceRow[];
  issues: IssueDto[];
};

export type RunResultDetailRecord = {
  runId: string;
  mode: string;
  source: string;
  inputDefId: string | null;
  csvDefId: string | null;
  targetModel: string | null;
  executedBy: string | null;
  invokedBy: string | null;
  inputName: string | null;
  inputFingerprint: string | null;
  tagsJson: Record<string, unknown> | null;
  startedAt: string;
  finishedAt: string | null;
  durationMs: number | null;
  status: string;
  totalRows: number;
  parsedRows: number;
  fkResolvedRows: number;
  processedRows: number;
  insertedRows: number;
  updatedRows: number;
  skippedRows: number;
  errorRows: number;
  infoCount: number;
  warnCount: number;
  errorCount: number;
  summaryMessage: string | null;
  exceptionType: string | null;
  exceptionMessage: string | null;
  createdAt: string;
};

export type IssueContextDetailRecord = {
  id: string;
  issueId: string;
  key: string;
  valueText: string | null;
  valueJson: Record<string, unknown> | null;
  createdAt: string;
};

export type IssueDetailRecord = {
  id: string;
  runId: string;
  domain: string;
  phase: string;
  severity: string;
  code: string;
  rowIndex: number | null;
  message: string | null;
  skipScope: string;
  createdAt: string;
  contexts: IssueContextDetailRecord[];
};

export type RunResultReferenceDetailResponse = {
  success: boolean;
  runResult: RunResultDetailRecord | null;
  issues: IssueDetailRecord[];
  issuesForError: IssueDto[];
};
