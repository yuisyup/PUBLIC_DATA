import { Form } from "react-bootstrap";
import type { FieldError, UseFormRegisterReturn } from "react-hook-form";
import { useInputDefinitions } from "../hooks/useInputDefinitions";

type Props = {
  inputType: string;
  registration: UseFormRegisterReturn;
  error?: FieldError;
};

/**
 * 入力データ定義ID（定義名）選択プルダウン
 *
 * @param inputType: string（入力データ種別）
 * @param registration: UseFormRegisterReturn（react-hook-form）
 * @param error: FieldError（react-hook-form）
 *
 * @returns
 */
export function InputDefSelect({ inputType, registration, error }: Props) {
  const { inputDefinitions, isLoading } = useInputDefinitions(inputType);

  return (
    <Form.Group>
      <Form.Label>入力データ定義</Form.Label>
      <Form.Select
        {...registration}
        disabled={!inputType || isLoading}
        isInvalid={!!error}
      >
        <option value="">選択してください</option>
        {inputDefinitions.map((def) => (
          <option key={def.id} value={String(def.id)}>
            {def.displayName}
          </option>
        ))}
      </Form.Select>
      <Form.Control.Feedback type="invalid">
        {error?.message}
      </Form.Control.Feedback>
    </Form.Group>
  );
}
