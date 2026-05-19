import { useCallback, useState } from 'react'
import { analyzeText, type AnalyzeRequest, type AnalyzeResponse } from '../services'

type AnalyzeState = {
  loading: boolean
  data: AnalyzeResponse | null
  error: string | null
}

export function useAnalyze() {
  const [state, setState] = useState<AnalyzeState>({
    loading: false,
    data: null,
    error: null,
  })

  const runAnalyze = useCallback(async (payload: AnalyzeRequest) => {
    setState({ loading: true, data: null, error: null })

    try {
      const data = await analyzeText(payload)
      setState({ loading: false, data, error: null })
      return data
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Analyze request failed'
      setState({ loading: false, data: null, error: message })
      return null
    }
  }, [])

  return { ...state, runAnalyze }
}

