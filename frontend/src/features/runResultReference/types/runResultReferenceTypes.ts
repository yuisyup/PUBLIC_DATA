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
