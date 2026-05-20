import { useEffect, useState } from "react";
import { fetchInputDefinitions } from "../api";
import type { InputDefinition } from "../types/inputDefTypes";

export function useInputDefinitions(inputType: string) {
  const [inputDefinitions, setInputDefinitions] = useState<InputDefinition[]>(
    [],
  );
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (!inputType) {
      setInputDefinitions([]);
      return;
    }

    let ignore = false;

    async function load() {
      setIsLoading(true);
      try {
        const data = await fetchInputDefinitions(inputType);
        if (!ignore) {
          setInputDefinitions(data);
        }
      } finally {
        if (!ignore) {
          setIsLoading(false);
        }
      }
    }

    load();

    return () => {
      ignore = true;
    };
  }, [inputType]);

  return { inputDefinitions, isLoading };
}
