import { useEffect, useState } from "react";
import { useForm, useWatch } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Alert, Button, Card, Col, Form, Row } from "react-bootstrap";
import { InputDefSelect } from "../../inputdef/components/InputDefSelect";
import { InputTypeSelect } from "../../inputdef/components/InputTypeSelect";
import { runResultReferenceSchema } from "../schemas/runResultReferenceSchema";
import { useRunResultReference } from "../hooks/useRunResultReference";
import { RunResultReferenceResult } from "./RunResultReferenceResult";

type FormValues = z.infer<typeof runResultReferenceSchema>;

export function RunResultReferenceForm() {
  const { search, clear, result, isLoading } = useRunResultReference();
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    control,
    setValue,
    reset,
    formState: { errors },
  } = useForm<FormValues>({
    resolver: zodResolver(runResultReferenceSchema),
    defaultValues: {
      inputType: "",
      inputDefinitionId: "",
      createdAt: "",
    },
  });

  const selectedInputType = useWatch({ control, name: "inputType" }) || "";

  useEffect(() => {
    setValue("inputDefinitionId", "");
  }, [selectedInputType, setValue]);

  async function onSubmit(values: FormValues) {
    try {
      setErrorMessage(null);
      await search({
        inputType: values.inputType,
        inputDefId: values.inputDefinitionId,
        createdAt: values.createdAt,
      });
    } catch (error) {
      console.error(error);
      setErrorMessage("検索処理でエラーが発生しました。");
    }
  }

  function onReset() {
    reset();
    clear();
    setErrorMessage(null);
  }

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <Card className="mb-3 border-dark">
        <Card.Body>
          <Row className="g-3">
            <Col md={4}>
              <InputTypeSelect registration={register("inputType")} error={errors.inputType} />
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
                <Form.Label>登録日</Form.Label>
                <Form.Control type="date" {...register("createdAt")} />
              </Form.Group>
            </Col>
          </Row>
        </Card.Body>
      </Card>

      <div className="d-flex justify-content-center gap-2">
        <Button type="submit" variant="primary" disabled={isLoading}>
          検索
        </Button>
        <Button type="button" variant="outline-secondary" onClick={onReset}>
          リセット
        </Button>
      </div>

      <div className="mt-3">
        {errorMessage && (
          <Alert variant="danger" className="mb-0">
            {errorMessage}
          </Alert>
        )}
        {result && <RunResultReferenceResult result={result} />}
      </div>
    </Form>
  );
}
