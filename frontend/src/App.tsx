import { useEffect, useState } from 'react'
import { BrowserRouter, NavLink, Routes, Route } from 'react-router-dom'
import IndexPage from './pages/Index'
import ReadmePage from './pages/Readme'
import PageView from './pages/Page'
import QueryPage from './pages/Query'
import IngestPage from './pages/Ingest'
import LogPage from './pages/Log'
import StatsPage from './pages/Stats'
import RawPage from './pages/Raw'
import GraphPage from './pages/Graph'
import LintPage from './pages/Lint'
import Login from './pages/Login'
import { getToken, clearToken } from './auth'

const nav = [
  { to: '/',       label: 'README' },
  { to: '/index',  label: 'Index'  },
  { to: '/graph',  label: 'Graph'  },
  { to: '/query',  label: 'Query'  },
  { to: '/ingest', label: 'Ingest' },
  { to: '/lint',   label: 'Lint'   },
  { to: '/log',    label: 'Log'    },
  { to: '/stats',  label: 'Stats'  },
  { to: '/raw',    label: 'Raw'    },
]

export default function App() {
  const [authed, setAuthed] = useState(!!getToken())

  useEffect(() => {
    const handler = () => setAuthed(false)
    window.addEventListener('auth:logout', handler)
    return () => window.removeEventListener('auth:logout', handler)
  }, [])

  if (!authed) return <Login onLogin={() => setAuthed(true)} />

  return (
    <BrowserRouter>
      <div className="flex h-screen bg-gray-50 text-gray-900">
        <aside className="w-48 bg-gray-900 text-gray-100 flex flex-col shrink-0">
          <div className="px-4 py-5 text-lg font-bold tracking-tight border-b border-gray-700">
            🧠 llmwiki
          </div>
          <nav className="flex flex-col gap-1 p-3 flex-1">
            {nav.map(({ to, label }) => (
              <NavLink
                key={to}
                to={to}
                end={to === '/'}
                className={({ isActive }) =>
                  `px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-gray-700 text-white'
                      : 'text-gray-400 hover:bg-gray-800 hover:text-white'
                  }`
                }
              >
                {label}
              </NavLink>
            ))}
          </nav>
          <button
            onClick={() => { clearToken(); setAuthed(false) }}
            className="m-3 px-3 py-2 rounded-md text-xs text-gray-500 hover:bg-gray-800 hover:text-white text-left"
          >
            Sign out
          </button>
        </aside>
        <main className="flex-1 overflow-auto p-8 flex flex-col">
          <Routes>
            <Route path="/"            element={<ReadmePage />} />
            <Route path="/index"       element={<IndexPage />} />
            <Route path="/graph"       element={<GraphPage />} />
            <Route path="/page/:title" element={<PageView />} />
            <Route path="/query"       element={<QueryPage />} />
            <Route path="/ingest"      element={<IngestPage />} />
            <Route path="/lint"        element={<LintPage />} />
            <Route path="/log"         element={<LogPage />} />
            <Route path="/stats"       element={<StatsPage />} />
            <Route path="/raw"         element={<RawPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}
