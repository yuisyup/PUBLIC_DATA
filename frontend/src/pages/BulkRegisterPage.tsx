import { Stack } from "react-bootstrap";
import { BulkRegisterForm } from "../features/bulkRegister/components/BulkRegisterForm";

/**
 * データ一括登録画面ページ
 * @returns
 */
export function BulkRegisterPage() {
  return (
    <Stack gap={4}>
      <div className="bg-primary text-white p-3 mb-4">
        <h3 className="text-white">データ一括登録</h3>
      </div>
      <BulkRegisterForm />
    </Stack>
  );
}
