export type AnalyzeRequest = {
  text: string
  language?: 'es' | 'en'
}

export type RiskItem = {
  label: string
  score: number
}

export type AnalyzeResponse = {
  verdict: 'safe' | 'warning' | 'danger'
  score: number
  risks: RiskItem[]
  summary: string
}

