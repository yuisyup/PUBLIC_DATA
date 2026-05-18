import { Form } from "react-bootstrap";
import type {
  FieldError,
  FieldValues,
  Path,
  UseFormRegister,
} from "react-hook-form";

type SelectOption = {
  value: string;
  label: string;
};

type SelectInputProps<T extends FieldValues> = {
  name: Path<T>;
  label: string;
  register: UseFormRegister<T>;
  options: SelectOption[];
  error?: FieldError;
  placeholder?: string;
  required?: boolean;
};

export function SelectInput<T extends FieldValues>({
  name,
  label,
  register,
  options,
  error,
  placeholder = "選択してください",
  required = false,
}: SelectInputProps<T>) {
  return (
    <Form.Group className="mb-3" controlId={name}>
      <Form.Label>
        {label}
        {required && <span className="text-danger ms-1">*</span>}
      </Form.Label>

      <Form.Select isInvalid={!!error} {...register(name)}>
        <option value="">{placeholder}</option>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </Form.Select>

      <Form.Control.Feedback type="invalid">
        {error?.message}
      </Form.Control.Feedback>
    </Form.Group>
  );
}
