import './RiskTrafficLight.css'
import type { AnalyzeResponse } from '../types/analyze'
import { ShieldCheck, TriangleAlert, ShieldAlert } from 'lucide-react'

type Props = {
  result: AnalyzeResponse | null
}

export function RiskTrafficLight({ result }: Props) {
  if (!result) return null

  const level = result.risk_level
  const safe = result.is_safe

  let color = 'green'
  let Icon = ShieldCheck
  let title = 'Enlace Seguro'
  let message = 'Puedes abrir este enlace con tranquilidad.'

  if (!safe || level === 'suspicious') {
    color = 'yellow'
    Icon = TriangleAlert
    title = 'Precaución'
    message = 'Este enlace puede ser sospechoso. Ten cuidado y no ingreses datos personales.'
  }

  if (!safe && (level === 'malicious' || level === 'phishing')) {
    color = 'red'
    Icon = ShieldAlert
    title = 'Peligro: Intento de Estafa'
    message = 'Cierra este mensaje inmediatamente, no ingreses tus datos.'
  }

  return (
    <article className={`risk-card risk-card--${color}`} role="status" aria-live="polite">
      <div className="risk-card__icon" aria-hidden="true">
        <Icon size={56} strokeWidth={2.2} />
      </div>
      <div className="risk-card__content">
        <h2 className="risk-card__title">{title}</h2>
        <p className="risk-card__message">{message}</p>
      </div>
    </article>
  )
}


