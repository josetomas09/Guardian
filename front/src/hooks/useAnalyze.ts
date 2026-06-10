import { useCallback, useState } from 'react'
import { analyzeText } from '../services'
import type { AnalyzeRequest, AnalyzeResponse } from '../types/analyze'

type AnalyzeState = {
  loading: boolean
  data: AnalyzeResponse | null
  error: boolean
}

export function useAnalyze() {
  const [state, setState] = useState<AnalyzeState>({
    loading: false,
    data: null,
    error: false,
  })

  const runAnalyze = useCallback(async (payload: AnalyzeRequest) => {
    setState({ loading: true, data: null, error: false })

    try {
      const data = await analyzeText(payload)
      setState({ loading: false, data, error: false })
      return data
    } catch {
      setState({ loading: false, data: null, error: true })
      return null
    }
  }, [])

  return { ...state, runAnalyze }
}

