import { apiFetch } from '../auth'
import { useEffect, useState } from 'react'

interface RawFile {
  name: string
  size: number | null
  mtime: number | null
  exists: boolean
}

function formatSize(bytes: number) {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`
}

function parseName(name: string) {
  const m = name.match(/^(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})_?(.*)\.txt$/)
  if (!m) return { date: name, source: '' }
  const [, yr, mo, dy, hh, mm] = m
  const source = m[7] || ''
  return { date: `${yr}-${mo}-${dy} ${hh}:${mm} UTC`, source }
}

export default function RawPage() {
  const [files, setFiles] = useState<RawFile[]>([])
  const [loading, setLoading] = useState(true)
  const [expanded, setExpanded] = useState<string | null>(null)
  const [content, setContent] = useState<Record<string, string>>({})

  useEffect(() => {
    apiFetch('/api/raw').then(r => r.json()).then(d => { setFiles(d); setLoading(false) })
  }, [])

  function toggle(f: RawFile) {
    if (!f.exists) return
    if (expanded === f.name) { setExpanded(null); return }
    setExpanded(f.name)
    if (!content[f.name]) {
      apiFetch(`/api/raw/${encodeURIComponent(f.name)}`)
        .then(r => r.json())
        .then(d => setContent(prev => ({ ...prev, [f.name]: d.content })))
    }
  }

  if (loading) return <p className="text-gray-400">Loading…</p>

  return (
    <div className="max-w-3xl">
      <h1 className="text-2xl font-bold mb-6">Raw Documents</h1>
      {files.length === 0
        ? <p className="text-gray-400">No raw documents yet.</p>
        : (
          <ul className="space-y-3">
            {files.map(f => {
              const { date, source } = parseName(f.name)
              const isOpen = expanded === f.name
              const missing = !f.exists

              return (
                <li
                  key={f.name}
                  className={`rounded-lg border shadow-sm overflow-hidden ${
                    missing
                      ? 'border-gray-100 bg-gray-50 opacity-50'
                      : 'border-gray-200 bg-white'
                  }`}
                >
                  <div
                    onClick={() => toggle(f)}
                    className={`w-full text-left px-4 py-3 flex items-center gap-3 ${
                      missing ? 'cursor-default' : 'cursor-pointer hover:bg-gray-50 transition-colors'
                    }`}
                  >
                    <span className="text-gray-400 text-sm">
                      {missing ? '✕' : isOpen ? '▾' : '▸'}
                    </span>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className={`text-xs font-mono ${missing ? 'text-gray-300' : 'text-gray-400'}`}>
                          {date}
                        </span>
                        {source && (
                          <span className={`text-xs px-2 py-0.5 rounded font-medium truncate max-w-[240px] ${
                            missing ? 'bg-gray-100 text-gray-400' : 'bg-blue-50 text-blue-600'
                          }`}>
                            {source.replace(/_/g, ' ')}
                          </span>
                        )}
                        {missing && (
                          <span className="text-xs text-gray-300 italic">deleted</span>
                        )}
                      </div>
                    </div>
                    {f.size != null && (
                      <span className="text-xs text-gray-400 font-mono shrink-0">{formatSize(f.size)}</span>
                    )}
                  </div>
                  {isOpen && (
                    <div className="border-t border-gray-100 bg-gray-50 px-4 py-3">
                      {content[f.name] == null
                        ? <p className="text-gray-400 text-sm">Loading…</p>
                        : <pre className="text-xs text-gray-700 whitespace-pre-wrap font-mono leading-relaxed max-h-96 overflow-y-auto">
                            {content[f.name]}
                          </pre>
                      }
                    </div>
                  )}
                </li>
              )
            })}
          </ul>
        )
      }
    </div>
  )
}
