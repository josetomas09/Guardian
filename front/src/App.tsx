import './App.css'
import {
  BaseScreen,
  HistoryList,
  RiskTrafficLight,
  saveHistoryItem,
  URLInput,
} from './components'
import { useAnalyze } from './hooks'

function App() {
  const { loading, error, data, runAnalyze } = useAnalyze()

  async function handleSubmit(url: string) {
    const result = await runAnalyze({ url })
    if (result) {
      saveHistoryItem(result)
    }
  }

  return (
    <BaseScreen>
      <URLInput onSubmit={handleSubmit} isLoading={loading} />

      {loading && (
        <p className="app-status" role="status" aria-live="polite">
          Analizando seguridad, por favor espera...
        </p>
      )}

      {error && (
        <p className="app-status app-status--error" role="alert">
          Ocurrió un error de conexión, intenta de nuevo
        </p>
      )}

      {data && !loading && <RiskTrafficLight result={data} />}

      <HistoryList />
    </BaseScreen>
  )
}

export default App
