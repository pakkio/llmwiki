import { apiFetch } from '../auth'
import { useEffect, useState } from 'react'

interface ParsedEntry {
  ts: string
  op: string
  description: string
  turns: string | null
  elapsed: string | null
  cost: string | null
  tokens: string | null
  raw: string
}

function parseEntry(line: string): ParsedEntry | null {
  const m = line.match(/^- `([^`]+)` \*\*([^*]+)\*\* — (.+)$/)
  if (!m) return null
  const [, ts, op, detail] = m
  const parts = detail.split(' · ')
  if (parts.length >= 4) {
    return {
      ts, op,
      description: parts[0],
      turns:       parts[1] ?? null,
      elapsed:     parts[2] ?? null,
      cost:        parts[3] ?? null,
      tokens:      parts[4] ?? null,
      raw: detail,
    }
  }
  // old format — show as-is
  return { ts, op, description: detail, turns: null, elapsed: null, cost: null, tokens: null, raw: detail }
}

export default function LogPage() {
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    apiFetch('/api/log')
      .then(r => r.json())
      .then(d => { setContent(d.content); setLoading(false) })
  }, [])

  if (loading) return <p className="text-gray-400">Loading…</p>

  const entries = content
    .split('\n')
    .filter(l => l.startsWith('- `'))
    .reverse()
    .map(parseEntry)
    .filter((e): e is ParsedEntry => e !== null)

  const totalCost = entries.reduce((sum, e) => {
    if (!e.cost) return sum
    const n = parseFloat(e.cost.replace('$', ''))
    return sum + (isNaN(n) ? 0 : n)
  }, 0)

  return (
    <div className="max-w-3xl">
      <div className="flex items-baseline gap-4 mb-6">
        <h1 className="text-2xl font-bold">Log</h1>
        {entries.length > 0 && totalCost > 0 && (
          <span className="text-sm text-gray-500">
            total spend: <span className="font-mono font-semibold text-green-600">${totalCost.toFixed(4)}</span>
          </span>
        )}
      </div>

      {!entries.length
        ? <p className="text-gray-400">No operations logged yet.</p>
        : (
          <ul className="space-y-3">
            {entries.map((e, i) => (
              <li key={i} className="rounded-lg border border-gray-200 bg-white px-4 py-3 shadow-sm">
                <div className="flex items-center gap-3 mb-1">
                  <span className="text-xs text-gray-400 font-mono shrink-0">{e.ts}</span>
                  <span className={`text-xs font-bold px-2 py-0.5 rounded-full shrink-0 ${
                    e.op === 'ingest'
                      ? 'bg-green-100 text-green-700'
                      : e.cost === '$0.0000'
                      ? 'bg-gray-100 text-gray-500'
                      : 'bg-blue-100 text-blue-700'
                  }`}>{e.op}{e.cost === '$0.0000' ? ' ⚡cached' : ''}</span>
                </div>
                <p className="text-sm text-gray-800 mb-2 break-words">{e.description}</p>
                {(e.turns || e.elapsed || e.cost || e.tokens) && (
                  <div className="flex flex-wrap gap-3 text-xs font-mono">
                    {e.turns   && <span className="text-gray-400">{e.turns}</span>}
                    {e.elapsed && <span className="text-blue-500">{e.elapsed}</span>}
                    {e.cost    && <span className="font-semibold text-green-600">{e.cost}</span>}
                    {e.tokens  && <span className="text-gray-400">{e.tokens}</span>}
                  </div>
                )}
              </li>
            ))}
          </ul>
        )
      }
    </div>
  )
}
