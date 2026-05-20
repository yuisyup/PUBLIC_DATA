export type InputType = {
  code: string; // CSV / XLSX / API
  displayName: string; // CSV / Excel / API など
};

export type InputDefinition = {
  id: number;
  inputType: string;
  inputCode: string;
  displayName: string;
  accept?: string; // ".csv,text/csv" など。持たせられるなら便利
};
