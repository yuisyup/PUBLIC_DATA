import { Form } from "react-bootstrap";
import type {
  FieldError,
  FieldValues,
  Path,
  UseFormRegister,
} from "react-hook-form";

type Props<T extends FieldValues> = {
  name: Path<T>;
  label: string;
  register: UseFormRegister<T>;
  error?: FieldError;
};

export function CheckboxInput<T extends FieldValues>({
  name,
  label,
  register,
  error,
}: Props<T>) {
  return (
    <Form.Group className="mb-3">
      <Form.Check
        type="checkbox"
        label={label}
        isInvalid={!!error}
        {...register(name)}
      />

      <Form.Control.Feedback type="invalid">
        {error?.message}
      </Form.Control.Feedback>
    </Form.Group>
  );
}
