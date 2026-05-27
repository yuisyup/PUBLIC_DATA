import { Alert, Badge, Card, Col, Row, Table } from "react-bootstrap";
import type { bulkRegisterResponse } from "../types/bulkRegisterTypes";

type Props = {
  result: bulkRegisterResponse;
};

/**
 * データ一括登録結果サマリー表示
 *
 * @param result: bulkRegisterResponse
 * @returns
 */
export function BulkRegisterResult({ result }: Props) {
  const { summary, issues } = result;

  return (
    <Card className="mt-4">
      <Card.Header>登録結果</Card.Header>
      <Card.Body>
        <Alert variant={result.success ? "success" : "danger"}>
          <div>ステータス: {result.status}</div>
          <div>Run ID: {result.runId}</div>
        </Alert>

        <Row className="g-3 mb-3">
          <Col md={3}>
            <div className="border rounded p-2">
              <div className="text-muted small">Total</div>
              <div className="fs-5">{summary.totalIssues}</div>
            </div>
          </Col>
          <Col md={3}>
            <div className="border rounded p-2">
              <div className="text-muted small">Error</div>
              <div className="fs-5 text-danger">{summary.errorCount}</div>
            </div>
          </Col>
          <Col md={3}>
            <div className="border rounded p-2">
              <div className="text-muted small">Warning</div>
              <div className="fs-5 text-warning">{summary.warningCount}</div>
            </div>
          </Col>
          <Col md={3}>
            <div className="border rounded p-2">
              <div className="text-muted small">Info</div>
              <div className="fs-5 text-info">{summary.infoCount}</div>
            </div>
          </Col>
        </Row>

        {issues.length > 0 && (
          <Table
            responsive
            bordered
            hover
            size="sm"
            className="mb-0 align-middle"
          >
            <thead className="table-light">
              <tr>
                <th>severity</th>
                <th>phase</th>
                <th>code</th>
                <th>row</th>
                <th>skip</th>
                <th>message</th>
              </tr>
            </thead>
            <tbody>
              {issues.map((issue, index) => (
                <tr
                  key={`${issue.phase}-${issue.code}-${issue.row ?? "none"}-${index}`}
                >
                  <td>{issue.severity}</td>
                  <td>{issue.phase}</td>
                  <td>{issue.code}</td>
                  <td>{issue.row ?? "-"}</td>
                  <td>
                    <Badge
                      bg={issue.skip ? "secondary" : "light"}
                      text={issue.skip ? undefined : "dark"}
                    >
                      {String(issue.skip)}
                    </Badge>
                  </td>
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
