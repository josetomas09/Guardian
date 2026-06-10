import './BaseScreen.css'
import type { ReactNode } from 'react'

type Props = {
  children: ReactNode
}

export function BaseScreen({ children }: Props) {
  return (
    <main className="base-screen" role="main">
      <header className="base-screen__header">
        <p className="base-screen__eyebrow">Guardian</p>
        <h1 className="base-screen__title">Guardian - Verificador de Enlaces</h1>
        <p className="base-screen__subtitle">Revisa si un enlace es seguro antes de abrirlo.</p>
      </header>

      <section className="base-screen__content">
        {children}
      </section>
    </main>
  )
}

