import { Form } from "react-bootstrap";
import type {
  FieldError,
  FieldErrorsImpl,
  FieldValues,
  Merge,
  Path,
  UseFormRegister,
} from "react-hook-form";

type FileInputError = FieldError | Merge<FieldError, FieldErrorsImpl<any>>;

type Props<T extends FieldValues> = {
  name: Path<T>;
  label: string;
  register: UseFormRegister<T>;
  error?: FileInputError;
  disabled?: boolean;
};

export function FileInput<T extends FieldValues>({
  name,
  label,
  register,
  error,
  disabled = false,
}: Props<T>) {
  const message =
    typeof error?.message === "string" ? error.message : undefined;

  return (
    <Form.Group className="mb-3">
      <Form.Label>{label}</Form.Label>

      <Form.Control
        type="file"
        isInvalid={!!error}
        disabled={disabled}
        {...register(name)}
      />

      <Form.Control.Feedback type="invalid">
        {message}
      </Form.Control.Feedback>
    </Form.Group>
  );
}
