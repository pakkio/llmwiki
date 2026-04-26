import { useNavigate } from 'react-router-dom'

interface Props {
  title: string
  label?: string
}

export default function WikiLink({ title, label }: Props) {
  const navigate = useNavigate()
  return (
    <button
      onClick={() => navigate(`/page/${encodeURIComponent(title)}`)}
      className="text-blue-600 hover:underline font-medium"
    >
      {label ?? title}
    </button>
  )
}
