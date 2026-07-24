import { useEffect, useRef, useState } from 'react'
import { TabulatorFull as Tabulator } from 'tabulator-tables'
import 'tabulator-tables/dist/css/tabulator.min.css'

type Item = {
  id: number
  paciente: string
  cpfPaciente: string
  medico: string
  cpfMedico: string
  data_hora: string
  status: string
  tipo: string
}

const apiBaseUrl = '/api/v1'
const authEndpoint = `${apiBaseUrl}/auth/login`
const schedulesEndpoint = `${apiBaseUrl}/schedule/`
const scheduleFilterEndpoint = `${apiBaseUrl}/schedule`
const sessionStorageKey = 'agenda-medica-session'
const sessionTokenStorageKey = 'agenda-medica-session-token'

const normalizeSchedule = (item: any): Item => ({
  id: item.id ?? 0,
  paciente: item.paciente?.nome ?? item.paciente?.email ?? item.paciente_name ?? item.patient_name ?? item.paciente ?? '-',
  cpfPaciente: item.paciente?.cpf ?? item.cpfPaciente ?? item.cpf ?? '-',
  medico: item.medico?.nome ?? item.medico?.email ?? item.medico_name ?? item.doctor_name ?? item.medico ?? '-',
  cpfMedico: item.medico?.cpf ?? item.cpfMedico ?? '-',
  data_hora: item.data_hora ?? item.data ?? item.date ?? '-',
  status: item.status ?? item.state ?? '-',
  tipo: item.tipo ?? item.paciente?.tipo ?? item.medico?.tipo ?? '-',
})

function App() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [sessionToken, setSessionToken] = useState<string | null>(() => {
    if (typeof window === 'undefined') {
      return null
    }

    return window.localStorage.getItem(sessionTokenStorageKey)
  })
  const [loggedIn, setLoggedIn] = useState(() => {
    if (typeof window === 'undefined') {
      return false
    }

    return Boolean(window.localStorage.getItem(sessionTokenStorageKey))
  })
  const [search, setSearch] = useState('')
  const [items, setItems] = useState<Item[]>([])
  const [loading, setLoading] = useState(false)
  const tableRef = useRef<HTMLDivElement | null>(null)
  const tableInstance = useRef<any | null>(null)

  const handleLogin = async (event: React.SyntheticEvent<HTMLFormElement>) => {
    event.preventDefault()
    setLoading(true)
    setError('')

    try {
      const payload = {
        email,
        senha: password,
      }

      const response = await fetch(authEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      })

      const data = await response.json().catch(() => null)

      if (!response.ok || data?.message === 'erro') {
        setError('E-mail ou senha inválidos.')
        setLoading(false)
        return
      }

      const token = data?.token

      if (!token) {
        setError('Sessão inválida retornada pelo servidor.')
        setLoading(false)
        return
      }

      window.localStorage.setItem(sessionTokenStorageKey, token)
      window.localStorage.setItem(sessionStorageKey, 'true')
      setSessionToken(token)
      setLoggedIn(true)
      setLoading(false)
    } catch {
      setError('Não foi possível conectar ao servidor.')
      setLoading(false)
    }
  }

  useEffect(() => {
    if (!loggedIn) {
      return
    }

    const loadSchedules = async () => {
      setLoading(true)
      try {
        const endpoint = search
          ? `${scheduleFilterEndpoint}/${encodeURIComponent(search)}`
          : schedulesEndpoint

        const response = await fetch(endpoint, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${sessionToken}`,
          },
        })

        const data = await response.json().catch(() => [])

        if (Array.isArray(data)) {
          setItems(data.map(normalizeSchedule))
        } else if (Array.isArray(data?.schedules)) {
          setItems(data.schedules.map(normalizeSchedule))
        } else {
          setItems([])
        }
      } catch {
        setItems([])
      } finally {
        setLoading(false)
      }
    }

    loadSchedules()
  }, [loggedIn, search, sessionToken])

  useEffect(() => {
    if (!loggedIn || !tableRef.current) {
      return
    }

    if (tableInstance.current) {
      tableInstance.current.replaceData(items)
      return
    }

    tableInstance.current = new Tabulator(tableRef.current, {
      data: items,
      layout: 'fitColumns',
      responsiveLayout: 'collapse',
      placeholder: 'Nenhum item encontrado.',
      columns: [
        { title: 'Paciente', field: 'paciente', sorter: 'string' },
        { title: 'CPF Paciente', field: 'cpfPaciente', sorter: 'string' },
        { title: 'Médico', field: 'medico', sorter: 'string' },
        { title: 'CPF Médico', field: 'cpfMedico', sorter: 'string' },
        { title: 'Data/Hora', field: 'data_hora', sorter: 'string' },
        { title: 'Status', field: 'status', sorter: 'string' },
        { title: 'Tipo', field: 'tipo', sorter: 'string' },
      ],
    })

    return () => {
      tableInstance.current?.destroy()
      tableInstance.current = null
    }
  }, [items, loggedIn])

  return (
    <div className="min-h-screen bg-gradient-to-br from-sky-50 via-white to-blue-50 p-4 sm:p-6 lg:p-8">
      {!loggedIn ? (
        <div className="flex min-h-[calc(100vh-2rem)] items-center justify-center">
          <form
            className="w-full max-w-md rounded-3xl border border-slate-200 bg-white/90 p-8 shadow-2xl shadow-slate-200 backdrop-blur"
            onSubmit={handleLogin}
          >
            <div className="mb-6 text-center">
              <p className="mb-2 text-sm font-semibold uppercase tracking-[0.3em] text-sky-600">Agenda Médica</p>
              <h1 className="text-3xl font-semibold text-slate-900">Entre para visualizar os atendimentos</h1>
            </div>

            <label className="mb-4 block text-sm font-medium text-slate-700">
              <span className="mb-2 block">E-mail</span>
              <input
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                placeholder="usuario@teste.com"
                required
                className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 outline-none transition focus:border-sky-500 focus:bg-white focus:ring-4 focus:ring-sky-100"
              />
            </label>

            <label className="mb-4 block text-sm font-medium text-slate-700">
              <span className="mb-2 block">Senha</span>
              <input
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                placeholder="123456"
                required
                className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 outline-none transition focus:border-sky-500 focus:bg-white focus:ring-4 focus:ring-sky-100"
              />
            </label>

            {error ? <p className="mb-4 text-sm text-rose-600">{error}</p> : null}

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-2xl bg-sky-600 px-4 py-3 font-semibold text-white transition hover:bg-sky-700 disabled:cursor-not-allowed disabled:opacity-70"
            >
              {loading ? 'Entrando...' : 'Entrar'}
            </button>
          </form>
        </div>
      ) : (
        <section className="mx-auto max-w-6xl rounded-3xl border border-slate-200 bg-white/90 p-6 shadow-2xl shadow-slate-200 backdrop-blur">
          <div className="mb-6 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.3em] text-sky-600">Painel</p>
              <h2 className="text-2xl font-semibold text-slate-900">Atendimentos agendados</h2>
            </div>
            <button
              type="button"
              className="rounded-2xl border border-slate-200 bg-slate-100 px-4 py-2 font-medium text-slate-700 transition hover:bg-slate-200"
              onClick={() => {
                window.localStorage.removeItem(sessionStorageKey)
                window.localStorage.removeItem(sessionTokenStorageKey)
                setSessionToken(null)
                setLoggedIn(false)
              }}
            >
              Sair
            </button>
          </div>

          <label className="mb-4 block">
            <span className="mb-2 block text-sm font-medium text-slate-700">Buscar</span>
            <input
              type="search"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Buscar por paciente, médico, status ou data"
              className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 outline-none transition focus:border-sky-500 focus:bg-white focus:ring-4 focus:ring-sky-100"
            />
          </label>

          {loading ? <p className="text-sm text-slate-500">Carregando agendamentos...</p> : null}
          <div ref={tableRef} className="min-h-[240px]" />
        </section>
      )}
    </div>
  )
}

export default App
