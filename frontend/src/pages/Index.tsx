import { apiFetch } from '../auth'
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

interface PageMeta {
  title: string
  summary: string
  links: string[]
  size: number
}

function WikiSummary({ text, navigate }: { text: string; navigate: (p: string) => void }) {
  const parts = text.split(/(\[\[[^\]]+\]\])/g)
  return (
    <p className="text-sm text-gray-500 line-clamp-2">
      {parts.map((part, i) => {
        const m = part.match(/^\[\[([^\]|]+)(?:\|([^\]]+))?\]\]$/)
        if (m) {
          const [, title, label] = m
          return (
            <button
              key={i}
              onClick={e => { e.stopPropagation(); navigate(`/page/${encodeURIComponent(title)}`) }}
              className="text-blue-500 hover:underline"
            >
              {label ?? title}
            </button>
          )
        }
        return <span key={i}>{part}</span>
      })}
    </p>
  )
}

export default function IndexPage() {
  const [pages, setPages] = useState<PageMeta[]>([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    apiFetch('/api/pages')
      .then(r => r.json())
      .then(data => { setPages(data); setLoading(false) })
  }, [])

  if (loading) return <p className="text-gray-400">Loading…</p>
  if (!pages.length) return <p className="text-gray-400">No pages yet. Use Ingest to add content.</p>

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Wiki Index</h1>

      {/* Card grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-10">
        {pages.map(p => (
          <button
            key={p.title}
            onClick={() => navigate(`/page/${encodeURIComponent(p.title)}`)}
            className="text-left border border-gray-200 rounded-xl p-4 hover:border-blue-400 hover:shadow-sm transition-all bg-white"
          >
            <h2 className="font-semibold text-gray-900 mb-1">{p.title}</h2>
            <WikiSummary text={p.summary} navigate={navigate} />
            {p.links.length > 0 && (
              <p className="text-xs text-blue-400 mt-2 truncate">
                → {p.links.slice(0, 3).join(', ')}{p.links.length > 3 ? '…' : ''}
              </p>
            )}
          </button>
        ))}
      </div>

      {/* Alphabetical list */}
      <div className="border-t border-gray-200 pt-6">
        <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">
          All pages ({pages.length})
        </h2>
        <ul className="columns-2 sm:columns-3 gap-x-8 space-y-1">
          {pages.map(p => (
            <li key={p.title}>
              <button
                onClick={() => navigate(`/page/${encodeURIComponent(p.title)}`)}
                className="text-sm text-blue-600 hover:underline"
              >
                {p.title}
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
