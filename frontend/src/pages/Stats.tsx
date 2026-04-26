import { apiFetch } from '../auth'
import { useEffect, useState } from 'react'

interface Stats {
  total_cost: number
  ingest_count: number
  ingest_cost: number
  ingest_tokens_in: number
  ingest_tokens_out: number
  query_count: number
  query_cost: number
  query_tokens_in: number
  query_tokens_out: number
  cached_count: number
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 shadow-sm px-5 py-4">
      <div className="text-xs text-gray-400 mb-1">{label}</div>
      <div className="text-xl font-mono font-semibold text-gray-900">{value}</div>
    </div>
  )
}

function fmt(n: number) { return n.toLocaleString() }
function cost(n: number) { return `$${n.toFixed(4)}` }

export default function StatsPage() {
  const [s, setS] = useState<Stats | null>(null)

  useEffect(() => {
    apiFetch('/api/stats').then(r => r.json()).then(setS)
  }, [])

  if (!s) return <p className="text-gray-400">Loading…</p>

  const totalOps = s.ingest_count + s.query_count + s.cached_count

  return (
    <div className="max-w-2xl">
      <h1 className="text-2xl font-bold mb-6">Cost &amp; Usage</h1>

      <div className="grid grid-cols-2 gap-4 mb-8">
        <div className="col-span-2 bg-green-50 border border-green-200 rounded-lg px-5 py-4">
          <div className="text-xs text-green-600 mb-1">Total spend</div>
          <div className="text-3xl font-mono font-bold text-green-700">{cost(s.total_cost)}</div>
          <div className="text-xs text-gray-400 mt-1">{fmt(totalOps)} operations total</div>
        </div>
      </div>

      <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Ingest</h2>
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-8">
        <Stat label="runs"       value={fmt(s.ingest_count)} />
        <Stat label="cost"       value={cost(s.ingest_cost)} />
        <Stat label="tokens in"  value={fmt(s.ingest_tokens_in)} />
        <Stat label="tokens out" value={fmt(s.ingest_tokens_out)} />
      </div>

      <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Query</h2>
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-8">
        <Stat label="runs (live)"   value={fmt(s.query_count)} />
        <Stat label="cost"          value={cost(s.query_cost)} />
        <Stat label="tokens in"     value={fmt(s.query_tokens_in)} />
        <Stat label="tokens out"    value={fmt(s.query_tokens_out)} />
      </div>

      <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Cache</h2>
      <div className="grid grid-cols-2 gap-3">
        <Stat label="cache hits" value={fmt(s.cached_count)} />
        <Stat label="cache rate" value={
          totalOps > 0
            ? `${Math.round(s.cached_count / (s.query_count + s.cached_count || 1) * 100)}%`
            : '—'
        } />
      </div>
    </div>
  )
}
