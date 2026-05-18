import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Button, Card, Col, Form, Row } from "react-bootstrap";

import { fetchInputDefinitions } from "../hooks/inputDefApi";
import type { InputDefinition } from "../types/InputDef";
import { useBulkRegister } from "../hooks/bulkRegister";
import { BulkRegisterResult } from "./BulkRegisterResult";
import { schema } from "../schemas/bulkRegisterScema";

/**
 * ファイル一括登録SCHEMA
 */
type BulkReisterFormValues = z.infer<typeof schema>;

/**
 * hooks
 */
const { submit, result: bulkRegisteResult } = useBulkRegister();

/**
 *
 * @returns JSX.Element
 */
export function BulkRegisterForm() {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<BulkReisterFormValues>({
    // zodのvalidationをFORMに適用
    resolver: zodResolver(schema),
  });

  // state：入力データ定義（ID, 名前）リスト
  const [inputDefinitions, setInputDefinitions] = useState<InputDefinition[]>(
    [],
  );
  // state：入力データ定義取得ローディング
  const [loadingDefinitions, setLoadingDefinitions] = useState(true);

  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  async function loadInputDefinitions() {
    try {
      const inputDefs = await fetchInputDefinitions("CSV");
      setInputDefinitions(inputDefs);
    } catch (error) {
      console.error(error);
    } finally {
      setLoadingDefinitions(false);
    }
  }

  // 画面表示時、入力データ定義一覧取得
  useEffect(() => {
    loadInputDefinitions();
  }, []);

  // 登録ボタンアクション
  async function onSubmit(values: BulkReisterFormValues) {
    const inputDefId = values.inputDefinitionId;
    const file = values.csvFile[0];

    console.log({
      inputDefinitionId: values.inputDefinitionId,
      fileName: file.name,
    });

    if (!inputDefId || !file) {
      setErrorMessage("CSV種類とファイルを選択してください。");
      return;
    }

    // 登録処理を実行
    try {
      await submit(file, Number(inputDefId));
    } catch (error) {
      setErrorMessage("登録処理でエラー");
    }
  }

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <h5 className="mb-3">入力項目</h5>

      <Card className="mb-3 border-dark">
        <Card.Body>
          <Row className="g-3">
            <Col md={6}>
              <Form.Group>
                <Form.Label>入力データ定義</Form.Label>
                <Form.Select
                  {...register("inputDefinitionId")}
                  disabled={loadingDefinitions}
                >
                  <option value="">選択してください</option>
                  {inputDefinitions.map((def) => (
                    <option key={def.id} value={String(def.id)}>
                      {def.displayName}
                    </option>
                  ))}
                </Form.Select>
                <Form.Control.Feedback type="invalid">
                  {errors.inputDefinitionId?.message}
                </Form.Control.Feedback>
              </Form.Group>
            </Col>

            <Col md={6}>
              <Form.Group>
                <Form.Label>CSVファイル</Form.Label>
                <Form.Control
                  type="file"
                  accept=".csv,text/csv"
                  {...register("csvFile")}
                  isInvalid={!!errors.csvFile}
                />
                <Form.Control.Feedback type="invalid">
                  {errors.csvFile?.message}
                </Form.Control.Feedback>
              </Form.Group>
            </Col>
          </Row>
        </Card.Body>
      </Card>

      <div className="d-flex justify-content-center gap-2">
        <Button type="submit" variant="primary" disabled={isSubmitting}>
          登録
        </Button>
        <Button
          type="button"
          variant="outline-secondary"
          onClick={() => reset()}
        >
          クリア
        </Button>
      </div>
      <div className="d-flex justify-content-center gap-2">
        {errorMessage && (
          <div className="alert alert-danger mt-3" role="alert">
            {errorMessage}
          </div>
        )}
        {bulkRegisteResult && <BulkRegisterResult result={bulkRegisteResult} />}
      </div>
    </Form>
  );
}
