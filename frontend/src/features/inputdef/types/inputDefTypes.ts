/**
 * 入力データ種別レスポンス
 */
export type InputType = {
  code: string; // CSV / XLSX / API
  displayName: string; // CSV / Excel / API など
};

/**
 * 入力データ定義レスポンス
 */
export type InputDefinition = {
  id: number;
  inputType: string;
  inputCode: string;
  displayName: string;
  accept?: string; // ".csv,text/csv" など。持たせられるなら便利
};
