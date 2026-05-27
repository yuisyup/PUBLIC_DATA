import { z } from "zod";

/**
 * データ一括登録FORMスキーマ
 */
export const schema = z.object({
  // 入力データ種別
  inputType: z.string().min(1, "入力データ種別を選択してください。"),
  // 入力データ定義ID
  inputDefinitionId: z.string().min(1, "入力データ定義を選択してください。"),
  // ファイル
  file: z
    .any()
    .refine((files) => files?.length > 0, "ファイルを選択してください。"),
});
