import { Stack } from "react-bootstrap";
import { useNavigate, useParams } from "react-router-dom";
import { RunResultReferenceDetailModal } from "../features/runResultReference/components/RunResultReferenceDetailModal";
import { RunResultReferenceForm } from "../features/runResultReference/components/RunResultReferenceForm";

export function RunResultReferencePage() {
  const { runId } = useParams();
  const navigate = useNavigate();

  return (
    <Stack gap={4}>
      <div className="bg-primary text-white p-3 mb-4">
        <h3 className="text-white">処理結果照会</h3>
      </div>
      <RunResultReferenceForm />
      <RunResultReferenceDetailModal
        runId={runId}
        show={!!runId}
        onHide={() => navigate("/run-result-reference")}
      />
    </Stack>
  );
}
