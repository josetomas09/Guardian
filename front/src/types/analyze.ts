export type AnalyzeRequest = {
  url: string
}

export type AnalyzeResponse = {
  url: string
  score: number
  is_safe: boolean
  risk_level: string
  threat_type: string | null
  details: any
}

