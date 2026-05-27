import { useEffect, useState } from "react";
import { fetchInputDefinitions } from "../api";
import type { InputDefinition } from "../types/inputDefTypes";

/**
 * 入力データ定義ID、名称リスト取得API呼出hook
 *
 * @param inputType: string（入力データ種別）
 *
 * @returns
 */
export function useInputDefinitions(inputType: string) {
  /* state: 入力データ定義リスト */
  const [inputDefinitions, setInputDefinitions] = useState<InputDefinition[]>(
    [],
  );
  /* state: 処理中ローディング */
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
