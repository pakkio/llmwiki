export const getToken = () => localStorage.getItem('llmwiki_token')
export const setToken = (t: string) => localStorage.setItem('llmwiki_token', t)
export const clearToken = () => localStorage.removeItem('llmwiki_token')

export async function apiFetch(url: string, init: RequestInit = {}): Promise<Response> {
  const token = getToken()
  const res = await fetch(url, {
    ...init,
    headers: {
      ...(init.headers as Record<string, string> ?? {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
  })
  if (res.status === 401) {
    clearToken()
    window.dispatchEvent(new Event('auth:logout'))
  }
  return res
}
