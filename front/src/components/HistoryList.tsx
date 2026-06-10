import './HistoryList.css'
import { useEffect, useMemo, useState } from 'react'
import { AlertTriangle, CheckCircle2, History } from 'lucide-react'
import type { AnalyzeResponse } from '../types/analyze'

type HistoryItem = Pick<AnalyzeResponse, 'url' | 'is_safe' | 'risk_level'> & {
  checkedAt: number
}

const STORAGE_KEY = 'guardian-history'
export const HISTORY_UPDATED_EVENT = 'guardian-history-updated'

function readHistory(): HistoryItem[] {
  if (typeof window === 'undefined') return []

  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    const parsed = raw ? (JSON.parse(raw) as HistoryItem[]) : []
    return Array.isArray(parsed) ? parsed.slice(0, 5) : []
  } catch {
    return []
  }
}

export function saveHistoryItem(result: AnalyzeResponse) {
  if (typeof window === 'undefined') return

  const next: HistoryItem[] = [
    {
      url: result.url,
      is_safe: result.is_safe,
      risk_level: result.risk_level,
      checkedAt: Date.now(),
    },
    ...readHistory(),
  ].slice(0, 5)

  localStorage.setItem(STORAGE_KEY, JSON.stringify(next))
  window.dispatchEvent(new Event(HISTORY_UPDATED_EVENT))
}

function statusLabel(item: HistoryItem) {
  if (item.is_safe || item.risk_level === 'safe') return 'Seguro'
  if (item.risk_level === 'suspicious') return 'Precaución'
  return 'Peligro'
}

export function HistoryList() {
  const [items, setItems] = useState<HistoryItem[]>(readHistory())

  useEffect(() => {
    const sync = () => setItems(readHistory())
    window.addEventListener('storage', sync)
    window.addEventListener(HISTORY_UPDATED_EVENT, sync)
    sync()

    return () => {
      window.removeEventListener('storage', sync)
      window.removeEventListener(HISTORY_UPDATED_EVENT, sync)
    }
  }, [])

  const visibleItems = useMemo(() => items.slice(0, 5), [items])

  return (
    <section className="history-list" aria-labelledby="history-list-title">
      <div className="history-list__header">
        <History size={24} aria-hidden="true" />
        <h2 id="history-list-title" className="history-list__title">Últimas URL revisadas</h2>
      </div>

      {visibleItems.length === 0 ? (
        <p className="history-list__empty">Aquí aparecerán los últimos enlaces que verifiques.</p>
      ) : (
        <ul className="history-list__items">
          {visibleItems.map((item) => {
            const safe = item.is_safe || item.risk_level === 'safe'
            const Icon = safe ? CheckCircle2 : AlertTriangle

            return (
              <li key={`${item.url}-${item.checkedAt}`} className="history-list__item">
                <span className={`history-list__dot history-list__dot--${safe ? 'safe' : 'unsafe'}`} aria-hidden="true" />
                <Icon size={18} className="history-list__state-icon" aria-hidden="true" />
                <div className="history-list__body">
                  <p className="history-list__url">{item.url}</p>
                  <p className="history-list__status">{statusLabel(item)}</p>
                </div>
              </li>
            )
          })}
        </ul>
      )}
    </section>
  )
}

