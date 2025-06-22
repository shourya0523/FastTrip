/* eslint-disable @typescript-eslint/no-explicit-any */
const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

export async function getData(endpoint: string) {
  const res = await fetch(`${BASE_URL}/${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
    },
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error("Error fetching data from API");
  }

  return res.json();
}

export async function postData(endpoint: string, body: any) {
  const res = await fetch(`${BASE_URL}/${endpoint}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    cache: "no-store",
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    throw new Error("Erro ao enviar dados para a API");
  }

  return res.json();
}
