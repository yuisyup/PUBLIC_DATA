import { http, HttpResponse } from "msw";
import { API_PATHS } from "../lib/apiPaths";
import { mockRegisterSuccess } from "./responses/register";

const mockApiPath = (path: string) => `*${path}`;

const inputTypes = [
  { code: "CSV", displayName: "CSV" },
  { code: "XLSX", displayName: "Excel" },
  { code: "API", displayName: "API" },
];

const inputDefinitions = [
  {
    id: 1,
    inputType: "CSV",
    inputCode: "customer_csv",
    displayName: "Customer CSV",
    accept: ".csv,text/csv",
  },
  {
    id: 2,
    inputType: "CSV",
    inputCode: "order_csv",
    displayName: "Order CSV",
    accept: ".csv,text/csv",
  },
  {
    id: 3,
    inputType: "XLSX",
    inputCode: "inventory_xlsx",
    displayName: "Inventory Excel",
    accept:
      ".xlsx,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  },
  {
    id: 4,
    inputType: "API",
    inputCode: "partner_api",
    displayName: "Partner API",
  },
];

const runResultReferences = [
  {
    runId: "11111111-1111-1111-1111-111111111111",
    inputDefId: "1",
    inputDefName: "Customer CSV",
    targetModel: "Customer",
    createdAt: "2026-06-01T10:00:00+09:00",
  },
  {
    runId: "22222222-2222-2222-2222-222222222222",
    inputDefId: "2",
    inputDefName: "Order CSV",
    targetModel: "Order",
    createdAt: "2026-06-02T11:30:00+09:00",
  },
  {
    runId: "33333333-3333-3333-3333-333333333333",
    inputDefId: "3",
    inputDefName: "Inventory Excel",
    targetModel: "Inventory",
    createdAt: "2026-06-02T13:00:00+09:00",
  },
];

const runResultDetails = {
  "11111111-1111-1111-1111-111111111111": {
    success: true,
    runResult: {
      runId: "11111111-1111-1111-1111-111111111111",
      mode: "SCREEN",
      source: "CSV",
      inputDefId: "1",
      csvDefId: null,
      targetModel: "Customer",
      executedBy: "mock-user",
      invokedBy: null,
      inputName: "customers.csv",
      inputFingerprint: "mock-fingerprint",
      tagsJson: { feature_key: "bulk_register" },
      startedAt: "2026-06-01T10:00:00+09:00",
      finishedAt: "2026-06-01T10:00:02+09:00",
      durationMs: 2000,
      status: "SUCCESS_WITH_WARN",
      totalRows: 2,
      parsedRows: 2,
      fkResolvedRows: 2,
      processedRows: 2,
      insertedRows: 1,
      updatedRows: 1,
      skippedRows: 0,
      errorRows: 0,
      infoCount: 1,
      warnCount: 1,
      errorCount: 0,
      summaryMessage: "mock summary",
      exceptionType: null,
      exceptionMessage: null,
      createdAt: "2026-06-01T10:00:03+09:00",
    },
    issues: [
      {
        id: "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        runId: "11111111-1111-1111-1111-111111111111",
        domain: "REGISTER",
        phase: "REGISTER.VALIDATE",
        severity: "WARN",
        code: "REGISTER.CSV_WARNING",
        rowIndex: 2,
        message: "mock warning",
        skipScope: "ROW",
        createdAt: "2026-06-01T10:00:01+09:00",
        contexts: [
          {
            id: "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
            issueId: "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            key: "column",
            valueText: "name",
            valueJson: { expected: "not blank" },
            createdAt: "2026-06-01T10:00:01+09:00",
          },
        ],
      },
    ],
    issuesForError: [],
  },
};

export const handlers = [
  http.get("/api/user", () => {
    return HttpResponse.json({ id: 1, name: "Taro Yamada" });
  }),

  http.get(mockApiPath(API_PATHS.inputDef.inputTypes), () => {
    return HttpResponse.json({ results: inputTypes });
  }),

  http.get(mockApiPath(API_PATHS.inputDef.inputDefs), ({ request }) => {
    const url = new URL(request.url);
    const inputType = url.searchParams.get("input_type");
    const results = inputType
      ? inputDefinitions.filter((def) => def.inputType === inputType)
      : inputDefinitions;

    return HttpResponse.json({ results });
  }),

  http.post(
    mockApiPath(API_PATHS.bulkRegister.register),
    async ({ request }) => {
      const formData = await request.formData();
      const inputDefId = formData.get("inputDefId");
      const file = formData.get("file");

      if (!inputDefId || !file || typeof file === "string") {
        return HttpResponse.json(
          {
            success: false,
            runId: "mock-run-invalid",
            status: "FAILED",
            summary: {
              totalIssues: 1,
              errorCount: 1,
              warningCount: 0,
              infoCount: 0,
            },
            issues: [
              {
                severity: "ERROR",
                phase: "GET_REGISTER_USECASE",
                code: "INVALID_REQUEST",
                row: null,
                message: "inputDefId or file is missing.",
                skip: "ALL",
                context: null,
              },
            ],
          },
          { status: 400 },
        );
      }

      return HttpResponse.json(mockRegisterSuccess);
    },
  ),

  http.get(mockApiPath(API_PATHS.runResultReference.search), ({ request }) => {
    const url = new URL(request.url);
    const inputType = url.searchParams.get("input_type");
    const inputDefId = url.searchParams.get("input_def_id");
    const createdAt = url.searchParams.get("created_at");

    const inputDefIdsByType = inputType
      ? inputDefinitions
          .filter((def) => def.inputType === inputType)
          .map((def) => String(def.id))
      : [];

    const results = runResultReferences.filter((row) => {
      if (inputType && !inputDefIdsByType.includes(String(row.inputDefId))) {
        return false;
      }
      if (inputDefId && row.inputDefId !== inputDefId) {
        return false;
      }
      if (createdAt && !row.createdAt.startsWith(createdAt)) {
        return false;
      }
      return true;
    });

    return HttpResponse.json({
      success: true,
      results,
      issues: [],
    });
  }),

  http.get(`${mockApiPath(API_PATHS.runResultReference.detail)}:runId/`, ({ params }) => {
    const runId = String(params.runId);
    const detail = runResultDetails[runId as keyof typeof runResultDetails];

    if (!detail) {
      return HttpResponse.json(
        {
          success: false,
          runResult: null,
          issues: [],
          issuesForError: [
            {
              severity: "ERROR",
              phase: "RUN_RESULT_REFERENCE_DETAIL.GET",
              code: "RUN_RESULT_REFERENCE_DETAIL.NOT_FOUND",
              row: null,
              message: "Run result was not found.",
              skip: "ALL",
              context: { run_id: runId },
            },
          ],
        },
        { status: 404 },
      );
    }

    return HttpResponse.json(detail);
  }),
];
