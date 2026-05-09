import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Button, Card, Col, Form, Row } from "react-bootstrap";

// zodによるvalidation定義
const schema = z.object({
    inputDefinitionId: z.string().min(1, "入力データ定義を選択してください"),
    csvFile: z
        .instanceof(FileList)
        .refine((files) => files.length > 0, "CSVファイルを選択してください")
        .refine(
            (files) => files[0]?.name.toLowerCase().endsWith(".csv"),
            "CSVファイルを選択してください"
        ),
});

// zodのvalidationで定義したフィールドをform要素とする
type CsvUploadFormValues = z.infer<typeof schema>;

// テスト用モックデータ
const mockInputDefs = [
    {
        id: 1,
        inputSourceKey: "test_member_csv",
        displayName: "テスト用名簿CSV",
    },
];

// react-hook-formによるFORM定義
export function CsvUploadForm() {
    const {
        register,
        handleSubmit,
        reset,
        formState: { errors, isSubmitting },
    } = useForm<CsvUploadFormValues>({
        // zodのvalidationをFORMに適用
        resolver: zodResolver(schema),
    });

    // 登録ボタンアクション
    async function onSubmit(values: CsvUploadFormValues) {
        const file = values.csvFile[0];

        console.log({
            inputDefinitionId: values.inputDefinitionId,
            fileName: file.name,
        });

        alert("登録処理はまだ未接続です");
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
                                    isInvalid={!!errors.inputDefinitionId}
                                >
                                    <option value="">選択してください</option>
                                    {mockInputDefs.map((def) => (
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
                <Button type="button" variant="outline-secondary" onClick={() => reset()}>
                    クリア
                </Button>
            </div>
        </Form>
    );
}