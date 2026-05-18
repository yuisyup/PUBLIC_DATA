import { Form } from "react-bootstrap";
import type {
  FieldError,
  FieldValues,
  Path,
  UseFormRegister,
} from "react-hook-form";

type Option = {
  value: string;
  label: string;
};

type Props<T extends FieldValues> = {
  name: Path<T>;
  label: string;
  register: UseFormRegister<T>;
  options: Option[];
  error?: FieldError;
};

export function RadioGroup<T extends FieldValues>({
  name,
  label,
  register,
  options,
  error,
}: Props<T>) {
  return (
    <Form.Group className="mb-3">
      <Form.Label>{label}</Form.Label>

      {options.map((opt) => (
        <Form.Check
          key={opt.value}
          type="radio"
          label={opt.label}
          value={opt.value}
          {...register(name)}
        />
      ))}

      <Form.Control.Feedback type="invalid" style={{ display: "block" }}>
        {error?.message}
      </Form.Control.Feedback>
    </Form.Group>
  );
}
