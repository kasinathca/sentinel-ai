import { apiGet } from "./apiClient";

export async function getHealth() {
  const body = await apiGet("/health");

  if (!body?.data) {
    throw new Error("Invalid health response from backend");
  }

  return body.data;
}