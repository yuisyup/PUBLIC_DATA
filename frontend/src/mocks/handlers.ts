import { http, HttpResponse } from "msw";
import { API_PATHS } from "../lib/apiPaths";

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

  http.post(mockApiPath(API_PATHS.bulkRegister.register), async ({ request }) => {
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

    return HttpResponse.json({
      success: true,
      runId: `mock-run-${Date.now()}`,
      status: "SUCCESS",
      summary: {
        totalIssues: 0,
        errorCount: 0,
        warningCount: 0,
        infoCount: 0,
      },
      issues: [],
    });
  }),
];
