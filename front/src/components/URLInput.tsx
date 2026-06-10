import './URLInput.css'
import { useEffect, useState, type ChangeEvent, type FormEvent } from 'react'
import { Link2, LoaderCircle } from 'lucide-react'

type Props = {
  value?: string
  onChange?: (v: string) => void
  onSubmit?: (url: string) => void
  isLoading?: boolean
}

export function URLInput({ value = '', onChange, onSubmit, isLoading = false }: Props) {
  const [local, setLocal] = useState(value)

  useEffect(() => {
    setLocal(value)
  }, [value])

  function handleChange(e: ChangeEvent<HTMLInputElement>) {
    const v = e.target.value
    setLocal(v)
    onChange?.(v)
  }

  function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e?.preventDefault()
    if (!local) return
    onSubmit?.(local)
  }

  return (
    <form className="url-input" onSubmit={handleSubmit} aria-label="Verificar URL">
      <div className="url-input__field">
        <span className="url-input__icon" aria-hidden="true">
          <Link2 size={28} strokeWidth={2.4} />
        </span>
        <input
          className="url-input__text"
          type="url"
          inputMode="url"
          placeholder="Pega la URL aquí"
          value={local}
          onChange={handleChange}
          aria-label="URL a verificar"
        />
      </div>
      <button type="submit" className="url-input__btn" disabled={isLoading || !local} aria-live="polite">
        {isLoading ? <LoaderCircle className="url-input__spinner" size={22} aria-hidden="true" /> : 'Verificar URL'}
      </button>
    </form>
  )
}

export default URLInput

