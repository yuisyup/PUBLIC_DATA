import type { bulkRegisterResponse } from "../types/bulkRegisterTypes";

type Props = {
  result: bulkRegisterResponse;
};

export function BulkRegisterResult({ result }: Props) {
  const { summary, issues } = result;

  return (
    <div className="mt-4">
      <div
        className={
          result.success ? "alert alert-success" : "alert alert-danger"
        }
      >
        <div>ステータス: {result.status}</div>
        <div>Run ID: {result.runId}</div>
      </div>

      <div className="row mb-3">
        <div className="col">Total: {summary.totalIssues}</div>
        <div className="col text-danger">Error: {summary.errorCount}</div>
        <div className="col text-warning">Warning: {summary.warningCount}</div>
        <div className="col text-info">Info: {summary.infoCount}</div>
      </div>

      {issues.length > 0 && (
        <table className="table table-sm table-bordered">
          <thead>
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
                <td>{issue.skip}</td>
                <td>{issue.message}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
