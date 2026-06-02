import { Stack } from "react-bootstrap";
import { RunResultReferenceForm } from "../features/runResultReference/components/RunResultReferenceForm";

export function RunResultReferencePage() {
  return (
    <Stack gap={4}>
      <div className="bg-primary text-white p-3 mb-4">
        <h3 className="text-white">処理結果照会</h3>
      </div>
      <RunResultReferenceForm />
    </Stack>
  );
}
