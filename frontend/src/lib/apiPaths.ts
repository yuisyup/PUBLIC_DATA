export const API_PATHS = {
  common: {
    health: "/api/common/health/",
  },
  inputDef: {
    inputTypes: "/api/input-types/",
    inputDefs: "/api/input-definitions/",
  },
  bulkRegister: {
    register: "/api/common/bulk-register/",
  },
} as const;
