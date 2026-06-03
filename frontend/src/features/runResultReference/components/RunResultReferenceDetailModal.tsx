import { Alert, Modal, Spinner, Table } from "react-bootstrap";
import { useRunResultDetail } from "../hooks/useRunResultDetail";
import type {
  IssueContextDetailRecord,
  IssueDetailRecord,
  RunResultDetailRecord,
} from "../types/runResultReferenceTypes";

type Props = {
  runId?: string;
  show: boolean;
  onHide: () => void;
};

export function RunResultReferenceDetailModal({ runId, show, onHide }: Props) {
  const { detail, isLoading } = useRunResultDetail(show ? runId : undefined);

  return (
    <Modal show={show} onHide={onHide} size="xl" centered scrollable>
      <Modal.Header closeButton>
        <Modal.Title>処理結果詳細</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {isLoading && (
          <div className="d-flex align-items-center gap-2">
            <Spinner size="sm" />
            <span>読み込み中</span>
          </div>
        )}

        {!isLoading && detail && !detail.success && (
          <Alert variant="danger" className="mb-0">
            {detail.issuesForError[0]?.message ?? "詳細取得でエラーが発生しました。"}
          </Alert>
        )}

        {!isLoading && detail?.success && detail.runResult && (
          <div className="d-flex flex-column gap-4">
            <RunResultSection runResult={detail.runResult} />
            <IssueSection issues={detail.issues} />
          </div>
        )}
      </Modal.Body>
    </Modal>
  );
}

function RunResultSection({ runResult }: { runResult: RunResultDetailRecord }) {
  const rows = [
    ["run_id", runResult.runId],
    ["mode", runResult.mode],
    ["source", runResult.source],
    ["input_def_id", runResult.inputDefId],
    ["csv_def_id", runResult.csvDefId],
    ["target_model", runResult.targetModel],
    ["executed_by", runResult.executedBy],
    ["invoked_by", runResult.invokedBy],
    ["input_name", runResult.inputName],
    ["input_fingerprint", runResult.inputFingerprint],
    ["tags_json", stringifyValue(runResult.tagsJson)],
    ["started_at", formatDateTime(runResult.startedAt)],
    ["finished_at", formatDateTime(runResult.finishedAt)],
    ["duration_ms", runResult.durationMs],
    ["status", runResult.status],
    ["total_rows", runResult.totalRows],
    ["parsed_rows", runResult.parsedRows],
    ["fk_resolved_rows", runResult.fkResolvedRows],
    ["processed_rows", runResult.processedRows],
    ["inserted_rows", runResult.insertedRows],
    ["updated_rows", runResult.updatedRows],
    ["skipped_rows", runResult.skippedRows],
    ["error_rows", runResult.errorRows],
    ["info_count", runResult.infoCount],
    ["warn_count", runResult.warnCount],
    ["error_count", runResult.errorCount],
    ["summary_message", runResult.summaryMessage],
    ["exception_type", runResult.exceptionType],
    ["exception_message", runResult.exceptionMessage],
    ["created_at", formatDateTime(runResult.createdAt)],
  ];

  return (
    <section>
      <h5>RunResultRecord</h5>
      <Table responsive bordered size="sm" className="mb-0 align-middle">
        <tbody>
          {rows.map(([label, value]) => (
            <tr key={label}>
              <th className="table-light w-25">{label}</th>
              <td>{formatValue(value)}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </section>
  );
}

function IssueSection({ issues }: { issues: IssueDetailRecord[] }) {
  return (
    <section>
      <h5>IssueRecord</h5>
      {issues.length === 0 ? (
        <Alert variant="info" className="mb-0">
          Issue はありません。
        </Alert>
      ) : (
        <div className="d-flex flex-column gap-3">
          {issues.map((issue) => (
            <div key={issue.id}>
              <Table responsive bordered size="sm" className="mb-2 align-middle">
                <thead className="table-light">
                  <tr>
                    <th>id</th>
                    <th>run_id</th>
                    <th>domain</th>
                    <th>phase</th>
                    <th>severity</th>
                    <th>code</th>
                    <th>row_index</th>
                    <th>message</th>
                    <th>skip_scope</th>
                    <th>created_at</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>{issue.id}</td>
                    <td>{issue.runId}</td>
                    <td>{issue.domain}</td>
                    <td>{issue.phase}</td>
                    <td>{issue.severity}</td>
                    <td>{issue.code}</td>
                    <td>{formatValue(issue.rowIndex)}</td>
                    <td>{formatValue(issue.message)}</td>
                    <td>{issue.skipScope}</td>
                    <td>{formatDateTime(issue.createdAt)}</td>
                  </tr>
                </tbody>
              </Table>
              <IssueContextSection contexts={issue.contexts} />
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

function IssueContextSection({
  contexts,
}: {
  contexts: IssueContextDetailRecord[];
}) {
  return (
    <div>
      <div className="fw-semibold mb-1">IssueContextRecord</div>
      {contexts.length === 0 ? (
        <Alert variant="secondary" className="mb-0 py-2">
          context はありません。
        </Alert>
      ) : (
        <Table responsive bordered size="sm" className="mb-0 align-middle">
          <thead className="table-light">
            <tr>
              <th>id</th>
              <th>issue_id</th>
              <th>key</th>
              <th>value_text</th>
              <th>value_json</th>
              <th>created_at</th>
            </tr>
          </thead>
          <tbody>
            {contexts.map((context) => (
              <tr key={context.id}>
                <td>{context.id}</td>
                <td>{context.issueId}</td>
                <td>{context.key}</td>
                <td>{formatValue(context.valueText)}</td>
                <td>{stringifyValue(context.valueJson)}</td>
                <td>{formatDateTime(context.createdAt)}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
    </div>
  );
}

function formatDateTime(value: string | null) {
  if (!value) {
    return "-";
  }

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }

  const year = date.getFullYear();
  const month = pad(date.getMonth() + 1);
  const day = pad(date.getDate());
  const hours = pad(date.getHours());
  const minutes = pad(date.getMinutes());
  const seconds = pad(date.getSeconds());

  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

function formatValue(value: unknown) {
  if (value === null || value === undefined || value === "") {
    return "-";
  }
  return String(value);
}

function stringifyValue(value: unknown) {
  if (value === null || value === undefined) {
    return "-";
  }
  return JSON.stringify(value);
}

function pad(value: number) {
  return String(value).padStart(2, "0");
}
