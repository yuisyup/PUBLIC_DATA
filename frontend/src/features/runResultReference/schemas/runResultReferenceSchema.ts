import { z } from "zod";

export const runResultReferenceSchema = z.object({
  inputType: z.string().optional(),
  inputDefinitionId: z.string().optional(),
  createdAt: z.string().optional(),
});
