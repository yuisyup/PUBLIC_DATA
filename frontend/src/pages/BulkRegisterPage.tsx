import { BulkRegisterForm } from "../features/bulkRegister/components/BulkRegisterForm";

export function BulkRegisterPage() {
  return (
    <div>
      <div className="bg-primary text-white p-3 mb-4">
        <h3 className="text-white">データ一括登録</h3>
      </div>
      <BulkRegisterForm />
    </div>
  );
}
