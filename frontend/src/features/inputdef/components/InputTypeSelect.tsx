import { Form } from "react-bootstrap";
import type { FieldError, UseFormRegisterReturn } from "react-hook-form";
import { useInputTypes } from "../hooks/useInputTypes";

type Props = {
  registration: UseFormRegisterReturn;
  error?: FieldError;
};

export function InputTypeSelect({ registration, error }: Props) {
  const { inputTypes, isLoading } = useInputTypes();

  return (
    <Form.Group>
      <Form.Label>入力データ種別</Form.Label>
      <Form.Select {...registration} disabled={isLoading} isInvalid={!!error}>
        <option value="">選択してください</option>
        {inputTypes.map((type) => (
          <option key={type.code} value={type.code}>
            {type.displayName}
          </option>
        ))}
      </Form.Select>
      <Form.Control.Feedback type="invalid">
        {error?.message}
      </Form.Control.Feedback>
    </Form.Group>
  );
}
