import { apiClient } from "./client";

export type HealthResponse = {
    status: string;
    message: string;
};

export async function fetchHealth(): Promise<HealthResponse> {
    const response = await apiClient.get<HealthResponse>("/common/health/");
    return response.data;
}