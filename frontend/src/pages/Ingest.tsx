import { apiFetch } from '../auth'
import { useState } from 'react'

interface ToolEvent {
  name: string
  args: Record<string, string>
}

type Mode = 'text' | 'url'

export default function IngestPage() {
  const [mode, setMode] = useState<Mode>('text')
  const [text, setText] = useState('')
  const [url, setUrl] = useState('')
  const [running, setRunning] = useState(false)
  const [events, setEvents] = useState<ToolEvent[]>([])
  const [result, setResult] = useState('')
  const [error, setError] = useState('')

  function handleDrop(e: React.DragEvent) {
    e.preventDefault()
    const file = e.dataTransfer.files[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = ev => { setText(ev.target?.result as string); setMode('text') }
    reader.readAsText(file)
  }

  async function submit() {
    const ready = mode === 'url' ? url.trim() : text.trim()
    if (!ready || running) return
    setRunning(true)
    setEvents([])
    setResult('')
    setError('')

    try {
      const body = mode === 'url' ? { url: url.trim() } : { text }
      const res = await apiFetch('/api/ingest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
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
          if (evt.type === 'done')  setResult(evt.result)
          if (evt.type === 'error') setError(evt.message)
        }
      }
    } catch (e: unknown) {
      setError(String(e))
    } finally {
      setRunning(false)
    }
  }

  const writtenPages = events.filter(e => e.name === 'write_page').map(e => e.args.title)

  return (
    <div className="max-w-2xl">
      <h1 className="text-2xl font-bold mb-6">Ingest</h1>

      <div className="flex gap-2 mb-4">
        <button
          onClick={() => setMode('text')}
          className={`px-4 py-1.5 rounded-lg text-sm font-medium ${mode === 'text' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}
        >
          Text / File
        </button>
        <button
          onClick={() => setMode('url')}
          className={`px-4 py-1.5 rounded-lg text-sm font-medium ${mode === 'url' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}
        >
          URL
        </button>
      </div>

      {mode === 'url' ? (
        <input
          type="url"
          value={url}
          onChange={e => setUrl(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && submit()}
          placeholder="https://…"
          className="w-full border border-gray-300 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 mb-4"
        />
      ) : (
        <>
          <div
            onDrop={handleDrop}
            onDragOver={e => e.preventDefault()}
            className="mb-4 border-2 border-dashed border-gray-300 rounded-xl p-3 text-center text-sm text-gray-400 hover:border-blue-300 transition-colors"
          >
            Drop a text file here, or paste below
          </div>
          <textarea
            value={text}
            onChange={e => setText(e.target.value)}
            rows={10}
            placeholder="Paste document text here…"
            className="w-full border border-gray-300 rounded-lg px-4 py-3 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-blue-400 resize-y mb-4"
          />
        </>
      )}

      <button
        onClick={submit}
        disabled={running || !(mode === 'url' ? url.trim() : text.trim())}
        className="px-5 py-2 bg-green-600 text-white rounded-lg text-sm font-medium hover:bg-green-700 disabled:opacity-50"
      >
        {running ? 'Ingesting…' : 'Ingest'}
      </button>

      {events.length > 0 && (
        <div className="mt-4 bg-gray-900 text-gray-100 rounded-lg p-4 font-mono text-xs space-y-1">
          {events.map((e, i) => (
            <div key={i}>
              <span className={e.name === 'write_page' ? 'text-green-400' : 'text-cyan-400'}>
                {e.name}
              </span>
              {e.args.title && <span className="text-gray-300"> "{e.args.title}"</span>}
            </div>
          ))}
          {running && <div className="text-gray-400 animate-pulse">…</div>}
        </div>
      )}

      {writtenPages.length > 0 && !running && (
        <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
          <p className="text-sm font-semibold text-green-800 mb-1">Pages written:</p>
          <ul className="text-sm text-green-700 list-disc list-inside">
            {[...new Set(writtenPages)].map(t => <li key={t}>{t}</li>)}
          </ul>
        </div>
      )}

      {error && <p className="text-red-500 text-sm mt-4">{error}</p>}
      {result && !running && (
        <p className="text-sm text-gray-600 mt-4 italic">{result}</p>
      )}
    </div>
  )
}
