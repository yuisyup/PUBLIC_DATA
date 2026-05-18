import { z } from "zod";

/**
 * ファイル一括登録画面スキーマ
 *
 * @returns {z.ZodObject} ファイル一括登録画面スキーマ
 */
export const schema = z.object({
  inputDefinitionId: z.string().min(1, "入力データ定義を選択してください"),
  csvFile: z
    .instanceof(FileList)
    .refine((files) => files.length > 0, "CSVファイルを選択してください")
    .refine(
      (files) => files[0]?.name.toLowerCase().endsWith(".csv"),
      "CSVファイルを選択してください",
    ),
});
