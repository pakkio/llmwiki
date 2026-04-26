import { apiFetch } from '../auth'
import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { usePageSet } from '../hooks/usePageSet'

export default function PageView() {
  const { title } = useParams<{ title: string }>()
  const navigate = useNavigate()
  const pageSet = usePageSet()
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!title) return
    setLoading(true)
    apiFetch(`/api/pages/${encodeURIComponent(title)}`)
      .then(r => {
        if (!r.ok) throw new Error('Page not found')
        return r.json()
      })
      .then(d => { setContent(d.content); setLoading(false) })
      .catch(e => { setError(e.message); setLoading(false) })
  }, [title])

  const processed = content
    .replace(/\[\[([^\]|]+)\|([^\]]+)\]\]/g, (_, t, l) =>
      `[${l}](/page/${encodeURIComponent(t)})`)
    .replace(/\[\[([^\]]+)\]\]/g, (_, t) =>
      `[${t}](/page/${encodeURIComponent(t)})`)

  if (loading) return <p className="text-gray-400">Loading…</p>
  if (error)   return <p className="text-red-500">{error}</p>

  return (
    <div>
      <button onClick={() => navigate(-1)} className="text-sm text-gray-400 hover:text-gray-600 mb-4 block">
        ← Back
      </button>
      <article className="prose prose-slate max-w-3xl font-mono">
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          components={{
            a: ({ href, children }) => {
              if (href?.startsWith('/page/')) {
                const t = decodeURIComponent(href.slice(6))
                const exists = pageSet.size === 0 || pageSet.has(t)
                return (
                  <button
                    onClick={() => navigate(href!)}
                    title={exists ? undefined : 'Page not yet created'}
                    className={exists
                      ? 'text-blue-600 hover:underline'
                      : 'text-orange-400 hover:underline opacity-75'}
                  >
                    {children}
                  </button>
                )
              }
              return <a href={href} target="_blank" rel="noreferrer">{children}</a>
            }
          }}
        >
          {processed}
        </ReactMarkdown>
      </article>
    </div>
  )
}
