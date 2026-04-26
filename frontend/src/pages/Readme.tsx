import { apiFetch } from '../auth'
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { usePageSet } from '../hooks/usePageSet'

export default function ReadmePage() {
  const navigate = useNavigate()
  const pageSet = usePageSet()
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    apiFetch('/api/readme')
      .then(r => {
        if (!r.ok) throw new Error('README not found')
        return r.json()
      })
      .then(d => { setContent(d.content); setLoading(false) })
      .catch(e => { setError(String(e)); setLoading(false) })
  }, [])

  if (loading) return <p className="text-gray-400">Loading…</p>
  if (error) return <p className="text-red-500">{error}</p>

  return (
    <div className="max-w-3xl">
      <h1 className="text-2xl font-bold mb-6">README</h1>
      <article className="prose prose-slate max-w-none">
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          components={{
            a: ({ href, children }) => {
              if (href?.startsWith('/page/')) {
                const title = decodeURIComponent(href.slice(6))
                const exists = pageSet.size === 0 || pageSet.has(title)
                return (
                  <button
                    onClick={() => navigate(href)}
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
            },
          }}
        >
          {content}
        </ReactMarkdown>
      </article>
    </div>
  )
}
