import axios from "axios";

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true,
});

// レスポンス共通処理
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Django想定のエラー整形
    if (error.response) {
      const status = error.response.status;
      const data = error.response.data;

      console.error("API Error:", status, data);

      // 必要ならここで共通メッセージ変換
      // 例：Issue形式に寄せるとか
    } else {
      console.error("Network Error:", error);
    }

    return Promise.reject(error);
  },
);
