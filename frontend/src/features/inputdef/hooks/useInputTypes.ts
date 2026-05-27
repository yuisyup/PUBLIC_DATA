import { useEffect, useState } from "react";
import { fetchInputTypes } from "../api";
import type { InputType } from "../types/inputDefTypes";

/**
 * 入力データ定義種別リスト取得API呼出hook
 *
 * @returns
 */
export function useInputTypes() {
  /* state: 入力データ定義種別リスト */
  const [inputTypes, setInputTypes] = useState<InputType[]>([]);
  /* state: 処理中ローディング */
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
