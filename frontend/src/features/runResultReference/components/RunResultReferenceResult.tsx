import { Alert, Button, Card, Table } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import type { RunResultReferenceResponse } from "../types/runResultReferenceTypes";

type Props = {
  result: RunResultReferenceResponse;
};

export function RunResultReferenceResult({ result }: Props) {
  const navigate = useNavigate();

  if (!result.success) {
    return (
      <Card className="mt-4">
        <Card.Header>検索結果</Card.Header>
        <Card.Body>
          <Alert variant="danger">検索処理でエラーが発生しました。</Alert>
          {result.issues.length > 0 && (
            <Table responsive bordered hover size="sm" className="mb-0 align-middle">
              <thead className="table-light">
                <tr>
                  <th>severity</th>
                  <th>phase</th>
                  <th>code</th>
                  <th>message</th>
                </tr>
              </thead>
              <tbody>
                {result.issues.map((issue, index) => (
                  <tr key={`${issue.phase}-${issue.code}-${index}`}>
                    <td>{issue.severity}</td>
                    <td>{issue.phase}</td>
                    <td>{issue.code}</td>
                    <td>{issue.message}</td>
                  </tr>
                ))}
              </tbody>
            </Table>
          )}
        </Card.Body>
      </Card>
    );
  }

  return (
    <Card className="mt-4">
      <Card.Header>検索結果</Card.Header>
      <Card.Body>
        {result.results.length === 0 ? (
          <Alert variant="info" className="mb-0">
            条件に一致する処理結果はありません。
          </Alert>
        ) : (
          <Table responsive bordered hover size="sm" className="mb-0 align-middle">
            <thead className="table-light">
              <tr>
                <th>run_id</th>
                <th>入力定義名</th>
                <th>target_model</th>
                <th>created_at</th>
                <th>詳細</th>
              </tr>
            </thead>
            <tbody>
              {result.results.map((row) => (
                <tr key={row.runId}>
                  <td>{row.runId}</td>
                  <td>{row.inputDefName ?? "-"}</td>
                  <td>{row.targetModel ?? "-"}</td>
                  <td>{formatCreatedAt(row.createdAt)}</td>
                  <td>
                    <Button
                      type="button"
                      variant="outline-primary"
                      size="sm"
                      onClick={() =>
                        navigate(`/run-result-reference/detail/${row.runId}`)
                      }
                    >
                      詳細
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        )}
      </Card.Body>
    </Card>
  );
}

function formatCreatedAt(value: string) {
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

function pad(value: number) {
  return String(value).padStart(2, "0");
}
