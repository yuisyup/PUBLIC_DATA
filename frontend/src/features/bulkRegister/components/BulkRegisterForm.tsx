import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Button, Card, Col, Form, Row } from "react-bootstrap";

import { InputDefSelect } from "../../inputdef/components/InputDefSelect";
import { InputTypeSelect } from "../../inputdef/components/InputTypeSelect";

import { useBulkRegister } from "../hooks/bulkRegister";
import { BulkRegisterResult } from "./BulkRegisterResult";
import { schema } from "../schemas/bulkRegisterScema";

type BulkRegisterFormValues = z.infer<typeof schema>;

export function BulkRegisterForm() {
  const { submit, result: bulkRegisterResult } = useBulkRegister();

  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<BulkRegisterFormValues>({
    resolver: zodResolver(schema),
  });
  const selectedInputType = watch("inputType");

  useEffect(() => {
    setValue("inputDefinitionId", "");
  }, [selectedInputType, setValue]);

  async function onSubmit(values: BulkRegisterFormValues) {
    const inputDefId = values.inputDefinitionId;
    const file = values.file;

    if (!inputDefId || !file) {
      setErrorMessage("ファイルを選択してください。");
      return;
    }

    try {
      setErrorMessage(null);
      await submit(file, Number(inputDefId));
    } catch (error) {
      console.error(error);
      setErrorMessage("登録処理でエラーが発生しました。");
    }
  }

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <h5 className="mb-3">入力項目</h5>

      <Card className="mb-3 border-dark">
        <Card.Body>
          <Row className="g-3">
            <Col md={4}>
              <InputTypeSelect
                registration={register("inputType")}
                error={errors.inputType}
              />
            </Col>

            <Col md={4}>
              <InputDefSelect
                inputType={selectedInputType}
                registration={register("inputDefinitionId")}
                error={errors.inputDefinitionId}
              />
            </Col>

            <Col md={4}>
              <Form.Group>
                <Form.Label>ファイル</Form.Label>
                <Form.Control
                  type="file"
                  {...register("file")}
                  disabled={!selectedInputType}
                  isInvalid={!!errors.file}
                />
                <Form.Control.Feedback type="invalid"></Form.Control.Feedback>
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

        {bulkRegisterResult && (
          <BulkRegisterResult result={bulkRegisterResult} />
        )}
      </div>
    </Form>
  );
}
