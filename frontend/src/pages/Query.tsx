import { apiFetch } from '../auth'
import { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { usePageSet } from '../hooks/usePageSet'

interface ToolEvent {
  name: string
  args: Record<string, string>
  result: string
}

const TOOL_COLORS: Record<string, string> = {
  read_page:    'text-cyan-400',
  write_page:   'text-green-400',
  list_pages:   'text-blue-400',
  search_pages: 'text-yellow-400',
}

export default function QueryPage() {
  const navigate = useNavigate()
  const pageSet = usePageSet()
  const [question, setQuestion] = useState('')
  const [running, setRunning] = useState(false)
  const [useCache, setUseCache] = useState(true)
  const [events, setEvents] = useState<ToolEvent[]>([])
  const [answer, setAnswer] = useState('')
  const [error, setError] = useState('')
  const abortRef = useRef<AbortController | null>(null)

  async function submit() {
    if (!question.trim() || running) return
    setRunning(true)
    setEvents([])
    setAnswer('')
    setError('')
    abortRef.current = new AbortController()

    try {
      const res = await apiFetch('/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, use_cache: useCache }),
        signal: abortRef.current.signal,
      })
      const reader = res.body!.getReader()
      const decoder = new TextDecoder()
      let buf = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        buf += decoder.decode(value, { stream: true })
        const parts = buf.split('\n\n')
        buf = parts.pop()!
        for (const part of parts) {
          if (!part.startsWith('data: ')) continue
          const evt = JSON.parse(part.slice(6))
          if (evt.type === 'tool')  setEvents(e => [...e, evt])
          if (evt.type === 'done')  setAnswer(evt.result)
          if (evt.type === 'error') setError(evt.message)
        }
      }
    } catch (e: unknown) {
      if (e instanceof Error && e.name !== 'AbortError') setError(String(e))
    } finally {
      setRunning(false)
    }
  }

  return (
    <div className="max-w-2xl">
      <h1 className="text-2xl font-bold mb-6">Query</h1>

      <div className="flex gap-2 mb-3">
        <input
          value={question}
          onChange={e => setQuestion(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && submit()}
          placeholder="Ask a question grounded in the wiki…"
          className="flex-1 border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <button
          onClick={submit}
          disabled={running || !question.trim()}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50"
        >
          {running ? 'Thinking…' : 'Ask'}
        </button>
      </div>
      <label className="flex items-center gap-2 mb-6 cursor-pointer select-none w-fit">
        <input
          type="checkbox"
          checked={useCache}
          onChange={e => setUseCache(e.target.checked)}
          className="rounded"
        />
        <span className="text-xs text-gray-500">use cache</span>
      </label>

      {events.length > 0 && (
        <div className="mb-4 bg-gray-900 text-gray-100 rounded-lg p-4 font-mono text-xs space-y-1">
          {events.map((e, i) => (
            <div key={i}>
              <span className={TOOL_COLORS[e.name] ?? 'text-white'}>{e.name}</span>
              <span className="text-gray-400">
                ({Object.entries(e.args).map(([k, v]) => `${k}=${JSON.stringify(v)}`).join(', ')})
              </span>
              <span className="text-gray-500"> → {e.result.slice(0, 80)}</span>
            </div>
          ))}
          {running && <div className="text-gray-400 animate-pulse">…</div>}
        </div>
      )}

      {error && <p className="text-red-500 text-sm mb-4">{error}</p>}

      {answer && (
        <div className="prose prose-slate max-w-none">
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
            {answer
              .replace(/\[\[([^\]|]+)\|([^\]]+)\]\]/g, (_, t, l) => `[${l}](/page/${encodeURIComponent(t)})`)
              .replace(/\[\[([^\]]+)\]\]/g, (_, t) => `[${t}](/page/${encodeURIComponent(t)})`)}
          </ReactMarkdown>
        </div>
      )}
    </div>
  )
}
