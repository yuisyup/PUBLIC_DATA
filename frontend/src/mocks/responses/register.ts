export const mockRegisterSuccess = {
  success: true,
  runId: "mock-run-001",
  issues: [],
};

export const mockRegisterWarn = {
  success: true,
  runId: "mock-run-002",
  issues: [
    {
      severity: "WARN",
      phase: "VALIDATE",
      code: "COLUMN_DEF_NOT_FOUND",
      message: "CSVカラム定義が見つかりません",
      skipScope: "COLUMN",
      context: {
        columnName: "player_name",
      },
    },
  ],
};
