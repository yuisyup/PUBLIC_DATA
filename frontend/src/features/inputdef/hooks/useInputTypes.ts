import { useEffect, useState } from "react";
import { fetchInputTypes } from "../api";
import type { InputType } from "../types/inputDefTypes";

export function useInputTypes() {
  const [inputTypes, setInputTypes] = useState<InputType[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    async function load() {
      setIsLoading(true);
      try {
        const data = await fetchInputTypes();
        setInputTypes(data);
      } finally {
        setIsLoading(false);
      }
    }

    load();
  }, []);

  return { inputTypes, isLoading };
}
