import { apiFetch } from '../auth'
import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import * as d3 from 'd3'

interface RawData {
  nodes: { id: string }[]
  edges: { source: string; target: string }[]
}

interface GNode extends d3.SimulationNodeDatum {
  id: string
  exists: boolean
  degree: number
}

interface GLink extends d3.SimulationLinkDatum<GNode> {
  source: GNode | string
  target: GNode | string
}

function nodeR(d: GNode) {
  return Math.max(7, 5 + d.degree * 1.5)
}

export default function GraphPage() {
  const svgRef   = useRef<SVGSVGElement>(null)
  const navigate = useNavigate()
  const [info, setInfo]       = useState<{ pages: number; links: number } | null>(null)
  const [loading, setLoading] = useState(true)
  const [rawData, setRawData] = useState<RawData | null>(null)

  useEffect(() => {
    apiFetch('/api/graph')
      .then(r => r.json())
      .then((d: RawData) => { setLoading(false); setRawData(d) })
  }, [])

  useEffect(() => {
    if (!rawData || !svgRef.current) return
    draw(rawData)
  }, [rawData])

  function draw(raw: RawData) {
    const el = svgRef.current!
    const width  = el.clientWidth  || 900
    const height = el.clientHeight || 600

    const existingIds = new Set(raw.nodes.map(n => n.id))
    const allIds      = new Set<string>([...existingIds])
    raw.edges.forEach(e => { allIds.add(e.source); allIds.add(e.target) })

    const degree = new Map<string, number>()
    raw.edges.forEach(e => {
      degree.set(e.source, (degree.get(e.source) ?? 0) + 1)
      degree.set(e.target, (degree.get(e.target) ?? 0) + 1)
    })

    const nodes: GNode[] = [...allIds].map(id => ({
      id, exists: existingIds.has(id), degree: degree.get(id) ?? 0,
    }))
    const links: GLink[] = raw.edges.map(e => ({ source: e.source, target: e.target }))

    setInfo({ pages: nodes.filter(n => n.exists).length, links: raw.edges.length })

    const svg = d3.select(el)
    svg.selectAll('*').remove()

    svg.append('defs').append('marker')
      .attr('id', 'arrow')
      .attr('viewBox', '0 -4 8 8')
      .attr('refX', 8).attr('refY', 0)
      .attr('markerWidth', 5).attr('markerHeight', 5)
      .attr('orient', 'auto')
      .append('path').attr('d', 'M0,-4L8,0L0,4').attr('fill', '#cbd5e1')

    const g = svg.append('g')

    svg.call(
      d3.zoom<SVGSVGElement, unknown>()
        .scaleExtent([0.15, 6])
        .on('zoom', e => g.attr('transform', e.transform))
    )

    const sim = d3.forceSimulation<GNode>(nodes)
      .force('link', d3.forceLink<GNode, GLink>(links).id(d => d.id).distance(120))
      .force('charge', d3.forceManyBody().strength(-280))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collide', d3.forceCollide<GNode>(d => nodeR(d) + 10))

    const link = g.append('g')
      .selectAll<SVGLineElement, GLink>('line')
      .data(links)
      .join('line')
      .attr('stroke', '#e2e8f0')
      .attr('stroke-width', 1.5)
      .attr('marker-end', 'url(#arrow)')

    const node = g.append('g')
      .selectAll<SVGGElement, GNode>('g')
      .data(nodes)
      .join('g')
      .style('cursor', d => d.exists ? 'pointer' : 'default')
      .on('click', (_, d) => d.exists && navigate(`/page/${encodeURIComponent(d.id)}`))
      .call(
        d3.drag<SVGGElement, GNode>()
          .on('start', (e, d) => { if (!e.active) sim.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y })
          .on('drag',  (e, d) => { d.fx = e.x; d.fy = e.y })
          .on('end',   (e, d) => { if (!e.active) sim.alphaTarget(0); d.fx = null; d.fy = null })
      )

    node.append('title').text(d => d.id + (d.exists ? '' : ' (not yet created)'))

    node.append('circle')
      .attr('r', nodeR)
      .attr('fill',         d => d.exists ? '#3b82f6' : 'none')
      .attr('stroke',       d => d.exists ? '#1d4ed8' : '#94a3b8')
      .attr('stroke-width', 1.5)
      .attr('stroke-dasharray', d => d.exists ? '' : '4 3')

    node.append('text')
      .text(d => d.id.length > 24 ? d.id.slice(0, 22) + '…' : d.id)
      .attr('x', d => nodeR(d) + 5)
      .attr('y', 4)
      .attr('font-size', 11)
      .attr('font-family', 'sans-serif')
      .attr('fill', d => d.exists ? '#1e293b' : '#94a3b8')
      .style('pointer-events', 'none')
      .style('user-select', 'none')

    sim.on('tick', () => {
      link
        .attr('x1', d => {
          const s = d.source as GNode
          const t = d.target as GNode
          const dx = (t.x ?? 0) - (s.x ?? 0)
          const dy = (t.y ?? 0) - (s.y ?? 0)
          const len = Math.sqrt(dx * dx + dy * dy) || 1
          return (s.x ?? 0) + (dx / len) * nodeR(s)
        })
        .attr('y1', d => {
          const s = d.source as GNode
          const t = d.target as GNode
          const dx = (t.x ?? 0) - (s.x ?? 0)
          const dy = (t.y ?? 0) - (s.y ?? 0)
          const len = Math.sqrt(dx * dx + dy * dy) || 1
          return (s.y ?? 0) + (dy / len) * nodeR(s)
        })
        .attr('x2', d => {
          const s = d.source as GNode
          const t = d.target as GNode
          const dx = (t.x ?? 0) - (s.x ?? 0)
          const dy = (t.y ?? 0) - (s.y ?? 0)
          const len = Math.sqrt(dx * dx + dy * dy) || 1
          return (t.x ?? 0) - (dx / len) * (nodeR(t) + 6)
        })
        .attr('y2', d => {
          const s = d.source as GNode
          const t = d.target as GNode
          const dx = (t.x ?? 0) - (s.x ?? 0)
          const dy = (t.y ?? 0) - (s.y ?? 0)
          const len = Math.sqrt(dx * dx + dy * dy) || 1
          return (t.y ?? 0) - (dy / len) * (nodeR(t) + 6)
        })

      node.attr('transform', d => `translate(${d.x ?? 0},${d.y ?? 0})`)
    })
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center gap-4 mb-3 shrink-0">
        <h1 className="text-2xl font-bold">Graph</h1>
        {info && (
          <span className="text-sm text-gray-500">
            {info.pages} pages · {info.links} links
          </span>
        )}
        <span className="ml-auto text-xs text-gray-400">scroll to zoom · drag to pan · drag nodes</span>
      </div>

      {loading
        ? <p className="text-gray-400">Loading…</p>
        : (
          <>
            <div className="flex-1 min-h-0 rounded-xl border border-gray-200 bg-slate-50 overflow-hidden">
              <svg ref={svgRef} className="w-full h-full" />
            </div>
            <div className="flex gap-5 mt-2 text-xs text-gray-400 shrink-0">
              <span className="flex items-center gap-1.5">
                <svg width="14" height="14"><circle cx="7" cy="7" r="6" fill="#3b82f6" stroke="#1d4ed8" strokeWidth="1.5"/></svg>
                existing page — click to open
              </span>
              <span className="flex items-center gap-1.5">
                <svg width="14" height="14"><circle cx="7" cy="7" r="6" fill="none" stroke="#94a3b8" strokeWidth="1.5" strokeDasharray="4 3"/></svg>
                linked but not yet created
              </span>
            </div>
          </>
        )
      }
    </div>
  )
}
