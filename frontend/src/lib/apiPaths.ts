export const API_PATHS = {
  common: {
    health: "/api/common/health/",
  },
  inputDef: {
    inputTypes: "/api/common/input-types/",
    inputDefs: "/api/common/input-definitions/",
  },
  bulkRegister: {
    register: "/api/common/bulk-register/",
  },
  runResultReference: {
    search: "/api/common/run-result-reference/",
  },
} as const;
