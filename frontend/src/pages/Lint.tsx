import { apiFetch } from '../auth'
import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

interface ToolEvent {
  name: string
  args: Record<string, string>
  result: string
}

const TOOL_COLORS: Record<string, string> = {
  read_page:    'text-cyan-400',
  list_pages:   'text-blue-400',
  search_pages: 'text-yellow-400',
}

export default function LintPage() {
  const [running, setRunning] = useState(false)
  const [events, setEvents] = useState<ToolEvent[]>([])
  const [report, setReport] = useState('')
  const [error, setError] = useState('')

  async function run() {
    if (running) return
    setRunning(true)
    setEvents([])
    setReport('')
    setError('')

    try {
      const res = await apiFetch('/api/lint')
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
          if (evt.type === 'done')  setReport(evt.result)
          if (evt.type === 'error') setError(evt.message)
        }
      }
    } catch (e: unknown) {
      setError(String(e))
    } finally {
      setRunning(false)
    }
  }

  return (
    <div className="max-w-2xl">
      <h1 className="text-2xl font-bold mb-2">Lint</h1>
      <p className="text-sm text-gray-500 mb-6">
        Health-check the wiki — orphan pages, contradictions, missing cross-references, gaps.
      </p>

      <button
        onClick={run}
        disabled={running}
        className="px-5 py-2 bg-purple-600 text-white rounded-lg text-sm font-medium hover:bg-purple-700 disabled:opacity-50 mb-6"
      >
        {running ? 'Checking…' : 'Run Lint'}
      </button>

      {events.length > 0 && (
        <div className="mb-6 bg-gray-900 text-gray-100 rounded-lg p-4 font-mono text-xs space-y-1">
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

      {report && (
        <div className="prose prose-slate max-w-none">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{report}</ReactMarkdown>
        </div>
      )}
    </div>
  )
}
