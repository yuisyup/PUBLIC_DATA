import { useState } from "react";
import { Button, Card, Spinner } from "react-bootstrap";
import { fetchHealth, type HealthResponse } from "../api/healthApi";

/**
 * API疎通確認ページ
 * @returns
 */
export function HealthCheckPage() {
  const [data, setData] = useState<HealthResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  async function handleClick() {
    setLoading(true);
    setErrorMessage("");
    setData(null);

    try {
      const result = await fetchHealth();
      setData(result);
    } catch (error) {
      console.error(error);
      setErrorMessage("API呼び出しに失敗しました。");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h1>Health Check</h1>
      <p>Django APIとの疎通確認ページです。</p>

      <Button onClick={handleClick} disabled={loading}>
        {loading ? "確認中..." : "API疎通確認"}
      </Button>

      {loading && (
        <div className="mt-3">
          <Spinner animation="border" size="sm" /> 呼び出し中...
        </div>
      )}

      {errorMessage && (
        <Card className="mt-3 border-danger">
          <Card.Body>
            <Card.Title>エラー</Card.Title>
            <Card.Text>{errorMessage}</Card.Text>
          </Card.Body>
        </Card>
      )}

      {data && (
        <Card className="mt-3">
          <Card.Body>
            <Card.Title>レスポンス</Card.Title>
            <pre>{JSON.stringify(data, null, 2)}</pre>
          </Card.Body>
        </Card>
      )}
    </div>
  );
}
