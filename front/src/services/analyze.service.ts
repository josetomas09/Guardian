import type { AnalyzeRequest, AnalyzeResponse } from '../types/analyze'

const ANALYZE_ENDPOINT = '/api/v1/analyze'

export async function analyzeText(payload: AnalyzeRequest): Promise<AnalyzeResponse> {
  const response = await fetch(ANALYZE_ENDPOINT, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  })

  if (!response.ok) {
    throw new Error(`Analyze endpoint failed with status ${response.status}`)
  }

  return (await response.json()) as AnalyzeResponse
}

export type { AnalyzeRequest, AnalyzeResponse }

