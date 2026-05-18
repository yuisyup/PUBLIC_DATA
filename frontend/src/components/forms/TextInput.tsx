// src/components/forms/TextInput.tsx
import { Form } from "react-bootstrap";
import type {
  FieldError,
  FieldValues,
  Path,
  UseFormRegister,
} from "react-hook-form";

type TextInputProps<T extends FieldValues> = {
  name: Path<T>;
  label: string;
  register: UseFormRegister<T>;
  error?: FieldError;
  type?: "text" | "number" | "email" | "password";
  placeholder?: string;
  required?: boolean;
};

export function TextInput<T extends FieldValues>({
  name,
  label,
  register,
  error,
  type = "text",
  placeholder,
  required = false,
}: TextInputProps<T>) {
  return (
    <Form.Group className="mb-3" controlId={name}>
      <Form.Label>
        {label}
        {required && <span className="text-danger ms-1">*</span>}
      </Form.Label>

      <Form.Control
        type={type}
        placeholder={placeholder}
        isInvalid={!!error}
        {...register(name)}
      />

      <Form.Control.Feedback type="invalid">
        {error?.message}
      </Form.Control.Feedback>
    </Form.Group>
  );
}
