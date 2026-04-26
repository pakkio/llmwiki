import { useEffect, useState } from 'react'
import { apiFetch } from '../auth'

export function usePageSet(): Set<string> {
  const [pages, setPages] = useState<Set<string>>(new Set())

  useEffect(() => {
    apiFetch('/api/pages')
      .then(r => r.json())
      .then((data: { title: string }[]) => setPages(new Set(data.map(p => p.title))))
      .catch(() => {})
  }, [])

  return pages
}
