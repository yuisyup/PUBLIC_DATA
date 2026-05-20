import { z } from "zod";

export const schema = z.object({
  inputType: z.string().min(1, "入力データ種別を選択してください。"),
  inputDefinitionId: z.string().min(1, "入力データ定義を選択してください。"),
  file: z
    .any()
    .refine((files) => files?.length > 0, "ファイルを選択してください。"),
});
