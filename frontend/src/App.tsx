import { useEffect, useState, type FormEvent, type ReactNode } from 'react'
import { BrowserRouter, Link, Navigate, NavLink, Route, Routes, useLocation, useParams } from 'react-router-dom'
import { isAxiosError } from 'axios'
import {
  ArrowRight,
  BookOpen,
  ChevronRight,
  Droplets,
  Leaf,
  MessageSquareText,
  Search,
  ShieldCheck,
  Sprout,
  SunMedium,
  Tractor,
} from 'lucide-react'

import './App.css'
import PhotoGuidePage from './PhotoGuidePage'
import {
  analyzeText,
  createCrop,
  getCurrentUser,
  getCropDetail,
  getCrops,
  getKnowledgeDetail,
  getFertilizers,
  getKnowledgeItems,
  getPests,
  sendChatMessage,
} from './services/api'
import type { ApiChatResponse, CropCreatePayload, CropItem, KnowledgeItem, User } from './types'

const navItems = [
  { label: 'Home', to: '/' },
  { label: 'Crops', to: '/crops' },
  { label: 'Knowledge', to: '/knowledge' },
  { label: 'Photo Guide', to: '/photo-guide' },
  { label: 'Fertilizer', to: '/fertilizer' },
  { label: 'Pest Management', to: '/pest-management' },
]

const featureCards = [
  {
    title: 'Organic crop planning',
    text: 'Match seasonal conditions, soil type, and water availability to the best crop decision.',
    icon: Sprout,
    image: '/images/farm-fields.jpg',
    imageAlt: 'Golden crop fields at sunrise',
  },
  {
    title: 'Fertility guidance',
    text: 'Learn how compost, bio-inputs, and green manure support steady soil health.',
    icon: Leaf,
    image: '/images/healthy-seedlings.jpg',
    imageAlt: 'A scoop of dark compost and garden soil',
  },
  {
    title: 'Pest intelligence',
    text: 'Scout before spraying and use a proven sequence of prevention, monitoring, and intervention.',
    icon: ShieldCheck,
    image: '/images/garden-harvest.jpg',
    imageAlt: 'Wheat heads growing in a field',
  },
]

const quickStats = [
  { label: 'Crops covered', value: '18+' },
  { label: 'Knowledge guides', value: '27+' },
  { label: 'Support model', value: 'Organic-first' },
  { label: 'Field readiness', value: 'Seasonal' },
]

const emptyCropForm: CropCreatePayload = {
  crop_name: '',
  soil_type: '',
  season: '',
  description: '',
  climate: '',
  water_need: '',
  suitable_soil: '',
  sowing_season: '',
  organic_fertilizers: '',
  irrigation: '',
  pest_management: '',
  harvesting: '',
}

const cropSymbols: Record<string, string> = {
  banana: '🍌',
  brinjal: '🍆',
  cabbage: '🥬',
  chilli: '🌶️',
  cotton: '☁️',
  groundnut: '🥜',
  lentil: '🫘',
  maize: '🌽',
  mango: '🥭',
  okra: '🫛',
  onion: '🧅',
  potato: '🥔',
  rice: '🍚',
  soybean: '🌱',
  sugarcane: '🎋',
  tomato: '🍅',
  turmeric: '🫚',
  wheat: '🌾',
}

function getCropSymbol(cropName: string) {
  const fallback = cropName.trim().slice(0, 2).toUpperCase()
  return cropSymbols[cropName.trim().toLowerCase()] ?? (fallback || '🌱')
}

const cropFormFields: Array<{ key: keyof CropCreatePayload; label: string; placeholder: string; multiline?: boolean }> = [
  { key: 'crop_name', label: 'Crop name', placeholder: 'For example, chickpea' },
  { key: 'soil_type', label: 'Suitable soil types', placeholder: 'For example, loam or sandy loam' },
  { key: 'season', label: 'Growing season', placeholder: 'For example, rabi or year-round' },
  { key: 'description', label: 'Short description', placeholder: 'Describe the crop and its main growing needs', multiline: true },
  { key: 'climate', label: 'Climate', placeholder: 'For example, cool and dry' },
  { key: 'water_need', label: 'Water need', placeholder: 'For example, low, medium, or high' },
  { key: 'suitable_soil', label: 'Soil preparation', placeholder: 'Describe suitable soil and drainage', multiline: true },
  { key: 'sowing_season', label: 'Sowing and planting', placeholder: 'Describe when and how to plant', multiline: true },
  { key: 'organic_fertilizers', label: 'Organic fertility', placeholder: 'Describe suitable organic inputs', multiline: true },
  { key: 'irrigation', label: 'Irrigation', placeholder: 'Describe water needs at important crop stages', multiline: true },
  { key: 'pest_management', label: 'Pest management', placeholder: 'Describe prevention and monitoring practices', multiline: true },
  { key: 'harvesting', label: 'Harvesting and storage', placeholder: 'Describe harvest signs and safe storage', multiline: true },
]

function requestError(error: unknown): string {
  if (isAxiosError<{ detail?: string }>(error)) {
    if (typeof error.response?.data?.detail === 'string') return error.response.data.detail
    if (!error.response) {
      return 'Cannot reach the backend. Start it at http://localhost:8000 and check that this frontend origin is allowed.'
    }
    return `The backend request failed (HTTP ${error.response.status}).`
  }
  return error instanceof Error ? error.message : 'The request could not be completed. Please try again.'
}

type AnswerBlock =
  | { kind: 'heading'; text: string }
  | { kind: 'paragraph'; text: string }
  | { kind: 'list'; ordered: boolean; items: string[] }

function AssistantAnswer({ text }: { text: string }) {
  const blocks: AnswerBlock[] = []
  let paragraph: string[] = []
  const flushParagraph = () => {
    if (paragraph.length > 0) {
      blocks.push({ kind: 'paragraph', text: paragraph.join(' ') })
      paragraph = []
    }
  }

  for (const rawLine of text.split(/\r?\n/)) {
    const line = rawLine.trim()
    if (!line) {
      flushParagraph()
      continue
    }

    const heading = line.match(/^(?:#{1,3}\s+|\*\*)(.+?)(?:\*\*)?:?$/) ?? line.match(/^([^:]{2,50}):$/)
    if (heading) {
      flushParagraph()
      blocks.push({ kind: 'heading', text: heading[1].replace(/\*\*/g, '').trim() })
      continue
    }

    const bullet = line.match(/^[-*•]\s+(.+)$/)
    const numbered = line.match(/^\d+[.)]\s+(.+)$/)
    if (bullet || numbered) {
      flushParagraph()
      const ordered = Boolean(numbered)
      const previous = blocks.at(-1)
      if (previous?.kind === 'list' && previous.ordered === ordered) {
        previous.items.push((bullet ?? numbered)![1])
      } else {
        blocks.push({ kind: 'list', ordered, items: [(bullet ?? numbered)![1]] })
      }
      continue
    }

    paragraph.push(line)
  }
  flushParagraph()

  return (
    <div className="answer-content">
      {blocks.map((block, index) => {
        if (block.kind === 'heading') return <h3 key={index}>{block.text}</h3>
        if (block.kind === 'paragraph') return <p key={index}>{block.text}</p>
        const List = block.ordered ? 'ol' : 'ul'
        return (
          <List key={index}>
            {block.items.map((item, itemIndex) => <li key={`${index}-${itemIndex}`}>{item}</li>)}
          </List>
        )
      })}
    </div>
  )
}

const assistantTopics: Record<string, string> = {
  crop_information: 'Crop guidance',
  soil_management: 'Soil management',
  organic_fertilizers: 'Organic fertilizers',
  pest_management: 'Pest management',
  irrigation: 'Water and irrigation',
  disease_management: 'Crop diseases',
  general_organic_farming: 'Organic farming',
}

const assistantStatuses: Record<string, string> = {
  answered: 'Knowledge-based answer',
  general_answer: 'General farming guidance',
  knowledge_fallback: 'Knowledge guide (AI unavailable)',
  no_context: 'No matching guide found',
  not_configured: 'AI service is not configured',
  embeddings_unavailable: 'Knowledge search is unavailable',
  refused: 'Outside farming guidance',
  error: 'AI service error',
}

function App() {
  return (
    <BrowserRouter>
      <Layout />
    </BrowserRouter>
  )
}

function Layout() {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('token'))
  const [authReady, setAuthReady] = useState(() => !localStorage.getItem('token'))
  const [authError, setAuthError] = useState('')
  const [authRetry, setAuthRetry] = useState(0)
  const location = useLocation()

  useEffect(() => {
    let active = true
    const loadUser = async () => {
      if (!token) {
        setUser(null)
        setAuthError('')
        setAuthReady(true)
        return
      }

      setAuthReady(false)
      setAuthError('')
      try {
        const currentUser = await getCurrentUser(token)
        if (!active) return
        setUser(currentUser)
        if (!currentUser) {
          localStorage.removeItem('token')
          setToken(null)
        }
      } catch (error: unknown) {
        if (!active) return
        setUser(null)
        setAuthError(requestError(error))
      } finally {
        if (active) setAuthReady(true)
      }
    }

    void loadUser()
    return () => {
      active = false
    }
  }, [token, authRetry])

  return (
    <div className="app-shell">
      {authError && (
        <div className="backend-error-banner" role="alert">
          <span>{authError} Your saved sign-in was kept.</span>
          <button type="button" className="secondary-button" onClick={() => setAuthRetry((attempt) => attempt + 1)}>
            Retry connection
          </button>
        </div>
      )}
      <header className="site-header">
          <div className="brand-wrap">
            <div className="brand-mark">
              <Leaf size={20} />
            </div>
            <div>
              <p className="eyebrow">Organic Farming Guide</p>
              <h2>AgriBloom</h2>
            </div>
          </div>

          <nav className="main-nav" aria-label="Main navigation">
            {navItems.map(({ label, to }) => (
              <NavLink key={label} to={to} className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                {label}
              </NavLink>
            ))}
          </nav>
      </header>

      <main className="page-content">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/knowledge" element={<KnowledgePage />} />
          <Route path="/knowledge/:articleId" element={<KnowledgeDetailPage />} />
          <Route path="/crops" element={<CropsPage token={token} />} />
          <Route path="/crops/:cropId" element={<CropDetailPage />} />
          <Route path="/photo-guide" element={<PhotoGuidePage />} />
          <Route path="/fertilizer" element={<FertilizerPage />} />
          <Route path="/pest-management" element={<PestPage />} />
          <Route path="/ai-assistant" element={<AiAssistantPage token={token} />} />
          <Route path="/sign-in" element={<Navigate to="/" replace />} />
          <Route path="/login" element={<Navigate to="/" replace />} />
          <Route path="/register" element={<Navigate to="/" replace />} />
          <Route path="/dashboard" element={<Navigate to="/" replace />} />
          <Route path="/admin" element={<RequireAuth user={user} authReady={authReady}>{user?.role === 'administrator' ? <AdminPage /> : <Navigate to="/" replace />}</RequireAuth>} />
          <Route path="/nlp" element={<RequireAuth user={user} authReady={authReady}><NlpTestingPage /></RequireAuth>} />
        </Routes>
      </main>

      <footer className="site-footer">
          <div>
            <p className="eyebrow">AgriBloom</p>
            <h3>Organic guidance for resilient farms</h3>
          </div>
          <div className="footer-links">
            <Link to="/knowledge">Resources</Link>
            <Link to="/crops">Crop guide</Link>
            <Link to="/photo-guide">Photo guide</Link>
            <Link to="/about">About</Link>
          </div>
      </footer>
      {location.pathname !== '/ai-assistant' && (
        <Link
          to="/ai-assistant"
          className="assistant-fab"
          aria-label="Open AI assistant"
          title="Open AI assistant"
        >
          <MessageSquareText size={22} />
        </Link>
      )}
    </div>
  )
}

function RequireAuth({
  user,
  authReady,
  children,
}: {
  user: User | null
  authReady: boolean
  children: ReactNode
}) {
  if (!authReady) {
    return <p className="auth-loading" role="status">Checking your sign-in…</p>
  }
  return user ? <>{children}</> : <Navigate to="/" replace />
}

function HomePage() {
  const [crops, setCrops] = useState<CropItem[]>([])
  const [cropError, setCropError] = useState('')

  useEffect(() => {
    let active = true
    getCrops()
      .then((items) => {
        if (active) setCrops(items.slice(0, 3))
      })
      .catch((loadError: unknown) => {
        if (active) setCropError(requestError(loadError))
      })
    return () => {
      active = false
    }
  }, [])

  return (
    <>
      <section className="hero-section">
        <div className="hero-copy">
          <p className="eyebrow accent">Practical organic farming systems</p>
          <h1>Grow healthier soil and stronger harvests.</h1>
          <p className="hero-description">
            Learn how to build resilient fields with compost, crop rotation, water-saving methods, and crop-specific guidance designed for organic farmers.
          </p>
          <div className="hero-actions">
            <Link to="/crops" className="primary-button">
              Explore crops
              <ArrowRight size={16} />
            </Link>
          </div>

          <div className="stats-grid">
            {quickStats.map((stat) => (
              <div key={stat.label} className="stat-card">
                <strong>{stat.value}</strong>
                <span>{stat.label}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="hero-visual">
          <img
            className="hero-landscape"
            src="/images/farm-fields.jpg"
            alt="Golden crop fields at sunrise"
            fetchPriority="high"
          />
          <div className="hero-visual-shade" />
          <div className="hero-visual-content">
            <div className="panel-content">
              <div className="rain-card">
                <SunMedium size={18} />
                <div>
                  <p>Thoughtful farming, season by season</p>
                  <strong>Better soil. Healthier harvests.</strong>
                </div>
              </div>
              <div className="mini-grid">
                <div>
                  <Tractor size={18} />
                  <span>Soil prep</span>
                </div>
                <div>
                  <Droplets size={18} />
                  <span>Water plan</span>
                </div>
                <div>
                  <ShieldCheck size={18} />
                  <span>Pest strategy</span>
                </div>
                <div>
                  <BookOpen size={18} />
                  <span>Guided learning</span>
                </div>
              </div>
            </div>
          </div>
          <div className="hero-photo-note">
            <span className="hero-note-icon"><Sprout size={19} /></span>
            <div>
              <strong>Rooted in good practice</strong>
              <span>Soil · crops · water · nature</span>
            </div>
          </div>
        </div>
      </section>

      <section className="info-section">
        <div className="section-header">
          <p className="eyebrow">Why this platform</p>
          <h2>Built for farmers, agronomists, and curious growers</h2>
        </div>

        <div className="feature-grid">
          {featureCards.map(({ title, text, icon: Icon, image, imageAlt }) => (
            <article key={title} className="feature-card">
              <img className="feature-image" src={image} alt={imageAlt} loading="lazy" />
              <div className="icon-wrap">
                <Icon size={18} />
              </div>
              <h3>{title}</h3>
              <p>{text}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="spotlight-section">
        <div className="section-header inline-header">
          <div>
            <p className="eyebrow">Popular crop guidance</p>
            <h2>Start with the crops you are likely to plant this season</h2>
          </div>
          <Link to="/crops" className="text-link">
            See all crops <ChevronRight size={16} />
          </Link>
        </div>

        <div className="crop-card-grid">
          {crops.map((crop) => (
            <article key={crop.id} className="crop-tile">
              <span className="chip">{crop.season}</span>
              <h3>{crop.crop_name}</h3>
              <p>{crop.description}</p>
              <ul>
                <li>Soil: {crop.soil_type}</li>
                <li>Water: {crop.water_need}</li>
              </ul>
              <Link to={`/crops/${crop.id}`} className="inline-action">
                Open guide <ChevronRight size={14} />
              </Link>
            </article>
          ))}
        </div>
        {cropError && <p className="error-text" role="alert">{cropError}</p>}
      </section>
    </>
  )
}

function AboutPage() {
  return (
    <section className="content-page">
      <div className="page-heading">
        <p className="eyebrow">About</p>
        <h1>Organic farming with practical decision support</h1>
      </div>

      <div className="two-column-layout">
        <div className="text-panel">
          <p>
            AgriBloom helps farmers turn broad agricultural principles into day-to-day action. Instead of relying on generic advice, the platform connects soil preparation, crop selection, fertiliser planning, and pest management into one simple route.
          </p>
          <p>
            The project blends educational content, recommendation logic, and AI-powered query support so users can ask questions about crops, soil, and farm management without losing the context of organic practice.
          </p>
        </div>

        <div className="check-panel">
          <h3>Core principles</h3>
          <ul>
            <li>Healthy soil before high-yield goals.</li>
            <li>Season-aware decision making.</li>
            <li>Integrated pest and nutrient planning.</li>
            <li>Local verification and agronomy judgment.</li>
          </ul>
        </div>
      </div>
    </section>
  )
}

function formatLabel(value: string) {
  return value.replaceAll('_', ' ').replace(/\b\w/g, (letter) => letter.toUpperCase())
}

function GuideCategoryIcon({ category }: { category: string }) {
  if (category === 'soil' || category === 'seeds') return <Sprout size={22} />
  if (category === 'water') return <Droplets size={22} />
  if (category === 'pest') return <ShieldCheck size={22} />
  if (category === 'fertilizer' || category === 'compost') return <Leaf size={22} />
  return <BookOpen size={22} />
}

function KnowledgePage() {
  const [items, setItems] = useState<KnowledgeItem[]>([])
  const [query, setQuery] = useState('')
  const [category, setCategory] = useState('all')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let active = true
    getKnowledgeItems()
      .then((data) => {
        if (active) setItems(data)
      })
      .catch((loadError: unknown) => {
        if (active) setError(requestError(loadError))
      })
      .finally(() => {
        if (active) setLoading(false)
      })
    return () => {
      active = false
    }
  }, [])

  const categories = Array.from(new Set(items.map((item) => item.category))).sort()
  const normalizedQuery = query.trim().toLowerCase()
  const filteredItems = items.filter((item) => {
    const matchesCategory = category === 'all' || item.category === category
    const searchableText = [item.title, item.summary, item.description, item.category, ...item.related_crops]
      .join(' ')
      .toLowerCase()
    return matchesCategory && (!normalizedQuery || searchableText.includes(normalizedQuery))
  })

  return (
    <section className="content-page catalog-page">
      <header className="catalog-hero knowledge-hero">
        <div className="catalog-hero-copy">
          <p className="eyebrow accent">The knowledge garden</p>
          <h1>Good ideas for healthier fields.</h1>
          <p className="catalog-hero-description">
            Browse practical, field-ready guides for soil, crops, water, compost, and more. Find a useful next step and grow from there.
          </p>
          <div className="catalog-hero-stats">
            <div><strong>{loading ? '—' : items.length}</strong><span>Practical guides</span></div>
            <div><strong>{loading ? '—' : categories.length}</strong><span>Topics to explore</span></div>
            <div><strong>Field-first</strong><span>Clear, useful advice</span></div>
          </div>
        </div>
        <div className="catalog-hero-image">
          <img src="/images/healthy-seedlings.jpg" alt="A scoop of dark compost and garden soil" />
          <div className="catalog-image-caption">
            <span className="catalog-caption-icon"><Leaf size={18} /></span>
            <div><span>From soil to harvest</span><strong>Knowledge that grows with you</strong></div>
          </div>
        </div>
      </header>

      <div className="catalog-section-heading">
        <div>
          <p className="eyebrow">Explore the library</p>
          <h2>Find your next field guide</h2>
        </div>
        <span className="catalog-count">{filteredItems.length} {filteredItems.length === 1 ? 'guide' : 'guides'}</span>
      </div>

      <div className="catalog-tools">
        <label className="catalog-search">
          <Search size={19} aria-hidden="true" />
          <span className="visually-hidden">Search guides</span>
          <input value={query} onChange={(event) => setQuery(event.target.value)} type="search" placeholder="Search soil, compost, a crop…" />
        </label>
        <div className="catalog-filters" role="group" aria-label="Filter guides by topic">
          <button type="button" className={`filter-chip ${category === 'all' ? 'selected' : ''}`} onClick={() => setCategory('all')}>
            All guides <span>{items.length}</span>
          </button>
          {categories.map((item) => (
            <button
              key={item}
              type="button"
              className={`filter-chip ${category === item ? 'selected' : ''}`}
              onClick={() => setCategory(item)}
            >
              {formatLabel(item)}
            </button>
          ))}
        </div>
      </div>

      {loading && <p className="status-text">Loading knowledge guides…</p>}
      {error && <p className="error-text" role="alert">{error}</p>}
      <div className="catalog-grid knowledge-grid">
        {filteredItems.map((article, index) => (
          <article key={article.id} className="knowledge-card">
            <div className={`knowledge-art knowledge-art-${index % 4}`} aria-hidden="true">
              <span className="knowledge-art-icon"><GuideCategoryIcon category={article.category} /></span>
              <span className="knowledge-art-number">{String(index + 1).padStart(2, '0')}</span>
              <span className="knowledge-art-label">FIELD NOTES</span>
            </div>
            <div className="knowledge-card-body">
              <span className="chip">{formatLabel(article.category)}</span>
              <h3>{article.title}</h3>
              <p>{article.summary}</p>
              <Link to={`/knowledge/${article.id}`} className="knowledge-card-link">
                Explore guide <ArrowRight size={16} />
              </Link>
            </div>
          </article>
        ))}
      </div>
      {!loading && !error && filteredItems.length === 0 && (
        <div className="catalog-empty">
          <BookOpen size={25} />
          <h3>No field guides found</h3>
          <p>Try a different search or choose another topic.</p>
        </div>
      )}
    </section>
  )
}

function KnowledgeDetailPage() {
  const { articleId } = useParams()
  const [article, setArticle] = useState<KnowledgeItem | null>(null)
  const [loading, setLoading] = useState(Boolean(articleId))
  const [error, setError] = useState('')

  useEffect(() => {
    if (!articleId) return
    let active = true
    getKnowledgeDetail(articleId)
      .then((item) => {
        if (active) setArticle(item)
      })
      .catch((loadError: unknown) => {
        if (active) setError(requestError(loadError))
      })
      .finally(() => {
        if (active) setLoading(false)
      })
    return () => {
      active = false
    }
  }, [articleId])

  if (loading) {
    return <section className="content-page"><p className="status-text">Loading guide…</p></section>
  }

  if (error) {
    return (
      <section className="content-page">
        <p className="error-text" role="alert">{error}</p>
        <Link to="/knowledge">Return to knowledge hub</Link>
      </section>
    )
  }

  if (!article) {
    return (
      <section className="content-page">
        <h1>Guide not found</h1>
        <Link to="/knowledge">Return to knowledge hub</Link>
      </section>
    )
  }

  return (
    <section className="content-page article-detail">
      <Link to="/knowledge" className="back-link">← Back to knowledge</Link>
      <span className="chip">{article.category}</span>
      <h1>{article.title}</h1>
      <p className="lead-text">{article.summary}</p>
      <div className="article-layout">
        <div className="text-panel">
          <h3>Description</h3>
          <p>{article.description}</p>
          <h3>Key steps</h3>
          <ol>
            {article.steps.map((step) => (
              <li key={step}>{step}</li>
            ))}
          </ol>
        </div>
        <aside className="info-panel">
          <h3>Benefits</h3>
          <ul>
            {article.benefits.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
          <h3>Materials</h3>
          <ul>
            {article.materials.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
          {article.precautions.length > 0 && (
            <>
              <h3>Precautions</h3>
              <ul>
                {article.precautions.map((item) => <li key={item}>{item}</li>)}
              </ul>
            </>
          )}
        </aside>
      </div>
      {article.examples.length > 0 && (
        <div className="text-panel article-examples">
          <h3>Field examples</h3>
          <ul>{article.examples.map((item) => <li key={item}>{item}</li>)}</ul>
        </div>
      )}
      {article.disclaimer && <p className="small-note">{article.disclaimer}</p>}
    </section>
  )
}

function CropsPage({ token }: { token: string | null }) {
  const [crops, setCrops] = useState<CropItem[]>([])
  const [cropForm, setCropForm] = useState<CropCreatePayload>(emptyCropForm)
  const [query, setQuery] = useState('')
  const [season, setSeason] = useState('all')
  const [showForm, setShowForm] = useState(false)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => {
    let active = true
    getCrops()
      .then((data) => {
        if (active) setCrops(data)
      })
      .catch((loadError: unknown) => {
        if (active) setError(requestError(loadError))
      })
      .finally(() => {
        if (active) setLoading(false)
      })
    return () => {
      active = false
    }
  }, [])

  const normalizedQuery = query.trim().toLowerCase()
  const seasons = Array.from(new Set(crops.map((crop) => crop.season))).sort()
  const filteredCrops = crops.filter((crop) => {
    const matchesSeason = season === 'all' || crop.season === season
    const searchableText = `${crop.crop_name} ${crop.description} ${crop.season} ${crop.soil_type} ${crop.water_need}`
      .toLowerCase()
    return matchesSeason && (!normalizedQuery || searchableText.includes(normalizedQuery))
  })

  const handleCreateCrop = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!token) {
      setError('Your session has expired. Reload the page; public crop guides remain available.')
      return
    }
    setSaving(true)
    setError('')
    setSuccess('')
    try {
      const createdCrop = await createCrop(cropForm, token)
      setCrops((current) => [...current, createdCrop].sort((a, b) => a.crop_name.localeCompare(b.crop_name)))
      setCropForm(emptyCropForm)
      setShowForm(false)
      setSuccess(`${createdCrop.crop_name} was added to the shared crop catalogue.`)
    } catch (createError) {
      setError(requestError(createError))
    } finally {
      setSaving(false)
    }
  }

  return (
    <section className="content-page catalog-page">
      <header className="catalog-hero crops-hero">
        <div className="catalog-hero-copy">
          <p className="eyebrow accent">Choose what grows well</p>
          <h1>Find the right crop for your field.</h1>
          <p className="catalog-hero-description">
            Compare seasonal growing profiles, soil preferences, and water needs to make confident choices for your farm.
          </p>
          <div className="catalog-hero-stats">
            <div><strong>{loading ? '—' : crops.length}</strong><span>Crop profiles</span></div>
            <div><strong>{loading ? '—' : seasons.length}</strong><span>Growing seasons</span></div>
            <div><strong>Soil + water</strong><span>At-a-glance details</span></div>
          </div>
        </div>
        <div className="catalog-hero-image">
          <img src="/images/farm-fields.jpg" alt="Rows of crops growing in a sunlit farm field" />
          <div className="catalog-image-caption">
            <span className="catalog-caption-icon"><Sprout size={18} /></span>
            <div><span>Plan with the season</span><strong>Better choices start here</strong></div>
          </div>
        </div>
      </header>

      <div className="catalog-section-heading">
        <div>
          <p className="eyebrow">The crop catalogue</p>
          <h2>Explore crops for your conditions</h2>
        </div>
        <span className="catalog-count">{filteredCrops.length} {filteredCrops.length === 1 ? 'crop' : 'crops'}</span>
      </div>

      <div className="catalog-tools crop-tools">
        <label className="catalog-search">
          <Search size={19} aria-hidden="true" />
          <span className="visually-hidden">Search crops</span>
          <input value={query} onChange={(event) => setQuery(event.target.value)} type="search" placeholder="Search by crop, season, soil, or water…" />
        </label>
        {token && (
          <button type="button" className="primary-button" onClick={() => { setShowForm((visible) => !visible); setError(''); setSuccess('') }}>
            {showForm ? 'Close crop form' : '+ Add a crop'}
          </button>
        )}
        <div className="catalog-filters" role="group" aria-label="Filter crops by growing season">
          <button type="button" className={`filter-chip ${season === 'all' ? 'selected' : ''}`} onClick={() => setSeason('all')}>
            All seasons <span>{crops.length}</span>
          </button>
          {seasons.map((item) => (
            <button key={item} type="button" className={`filter-chip ${season === item ? 'selected' : ''}`} onClick={() => setSeason(item)}>
              {formatLabel(item)}
            </button>
          ))}
        </div>
      </div>

      {showForm && token && (
        <form className="crop-create-form" onSubmit={handleCreateCrop}>
          <div className="section-header">
            <p className="eyebrow">Shared crop catalogue</p>
            <h2>Add a crop profile</h2>
            <p>All signed-in users can contribute. Include practical, locally checked guidance so others can use it safely.</p>
          </div>
          <div className="crop-create-grid">
            {cropFormFields.map((field) => (
              <label key={field.key}>
                {field.label}
                {field.multiline ? (
                  <textarea
                    required
                    minLength={10}
                    maxLength={1200}
                    value={cropForm[field.key]}
                    onChange={(event) => setCropForm((current) => ({ ...current, [field.key]: event.target.value }))}
                    placeholder={field.placeholder}
                    rows={3}
                  />
                ) : (
                  <input
                    required
                    minLength={2}
                    maxLength={field.key === 'crop_name' ? 80 : 200}
                    value={cropForm[field.key]}
                    onChange={(event) => setCropForm((current) => ({ ...current, [field.key]: event.target.value }))}
                    placeholder={field.placeholder}
                  />
                )}
              </label>
            ))}
          </div>
          {error && <p className="error-text" role="alert">{error}</p>}
          <button type="submit" className="primary-button" disabled={saving}>
            {saving ? 'Adding crop…' : 'Add to shared catalogue'}
          </button>
        </form>
      )}

      {success && <p className="success-text" role="status">{success}</p>}
      {error && !showForm && <p className="error-text" role="alert">{error}</p>}
      {loading && <p className="status-text">Loading crop profiles…</p>}
      <div className="catalog-grid crop-grid">
        {filteredCrops.map((crop, index) => (
          <article key={crop.id} className="crop-card">
            <div className={`crop-art crop-art-${index % 4}`} aria-hidden="true">
              <span className="crop-art-icon"><span className="crop-symbol">{getCropSymbol(crop.crop_name)}</span></span>
              <span className="crop-art-label">{formatLabel(crop.season)} season</span>
            </div>
            <div className="crop-card-body">
              <div className="crop-card-meta">
                <span className="chip">{formatLabel(crop.season)}</span>
                <span className="crop-water"><Droplets size={14} /> {crop.water_need}</span>
              </div>
              <h3>{crop.crop_name}</h3>
              <p className="crop-description">{crop.description}</p>
              <div className="crop-soil"><span><Leaf size={14} /> Suitable soil</span><strong>{crop.soil_type}</strong></div>
              <Link to={`/crops/${crop.id}`} className="knowledge-card-link">
                Open crop guide <ArrowRight size={16} />
              </Link>
            </div>
          </article>
        ))}
      </div>
      {!loading && !error && filteredCrops.length === 0 && (
        <div className="catalog-empty">
          <Sprout size={25} />
          <h3>{crops.length ? 'No crops match those filters' : 'Crop profiles are on their way'}</h3>
          <p>{crops.length ? 'Try another search or choose a different growing season.' : 'Check back soon for practical, locally minded crop guides.'}</p>
        </div>
      )}
    </section>
  )
}

function CropDetailPage() {
  const { cropId } = useParams()
  const [crop, setCrop] = useState<CropItem | null>(null)
  const [loading, setLoading] = useState(Boolean(cropId))
  const [error, setError] = useState('')

  useEffect(() => {
    if (!cropId) return
    let active = true
    getCropDetail(cropId)
      .then((item) => {
        if (active) setCrop(item)
      })
      .catch((loadError: unknown) => {
        if (active) setError(requestError(loadError))
      })
      .finally(() => {
        if (active) setLoading(false)
      })
    return () => {
      active = false
    }
  }, [cropId])

  if (loading) {
    return <section className="content-page"><p className="status-text">Loading crop guide…</p></section>
  }

  if (error || !crop) {
    return (
      <section className="content-page">
        <h1>{error ? 'Unable to load crop' : 'Crop not found'}</h1>
        {error && <p className="error-text" role="alert">{error}</p>}
        <Link to="/crops">Back to crops</Link>
      </section>
    )
  }

  return (
    <section className="content-page article-detail">
      <Link to="/crops" className="back-link">← Back to crops</Link>
      <span className="chip">{crop.season}</span>
      <h1>{crop.crop_name}</h1>

      <div className="article-layout">
        <div className="text-panel">
          <p>{crop.description}</p>
          <table className="detail-table">
            <tbody>
              <tr><td>Climate</td><td>{crop.climate}</td></tr>
              <tr><td>Water need</td><td>{crop.water_need}</td></tr>
              <tr><td>Soil type</td><td>{crop.soil_type}</td></tr>
              <tr><td>Suitable soil</td><td>{crop.suitable_soil}</td></tr>
              <tr><td>Sowing</td><td>{crop.sowing_season}</td></tr>
            </tbody>
          </table>
        </div>

        <aside className="info-panel">
          <h3>Organic fertility</h3>
          <p>{crop.organic_fertilizers}</p>
          <h3>Irrigation</h3>
          <p>{crop.irrigation}</p>
          <h3>Pest management</h3>
          <p>{crop.pest_management}</p>
          <h3>Harvesting</h3>
          <p>{crop.harvesting}</p>
        </aside>
      </div>
    </section>
  )
}

function FertilizerPage() {
  const [items, setItems] = useState<KnowledgeItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let active = true
    getFertilizers()
      .then((data) => {
        if (active) setItems(data)
      })
      .catch((loadError: unknown) => {
        if (active) setError(requestError(loadError))
      })
      .finally(() => {
        if (active) setLoading(false)
      })
    return () => {
      active = false
    }
  }, [])

  return (
    <section className="content-page">
      <div className="page-heading">
        <p className="eyebrow">Fertilizer plan</p>
        <h1>Choose nutrient sources that match the crop and soil</h1>
      </div>
      {loading && <p className="status-text">Loading fertilizer guides…</p>}
      {error && <p className="error-text" role="alert">{error}</p>}
      <div className="card-grid">
        {items.map((article) => (
          <article key={article.id} className="resource-card">
            <span className="chip">{article.category}</span>
            <h3>{article.title}</h3>
            <p>{article.summary}</p>
            <Link to={`/knowledge/${article.id}`} className="inline-action">
              Review details <ChevronRight size={14} />
            </Link>
          </article>
        ))}
      </div>
      {!loading && !error && items.length === 0 && <p className="status-text">No fertilizer guides are available yet.</p>}
    </section>
  )
}

function PestPage() {
  const [items, setItems] = useState<KnowledgeItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let active = true
    getPests()
      .then((data) => {
        if (active) setItems(data)
      })
      .catch((loadError: unknown) => {
        if (active) setError(requestError(loadError))
      })
      .finally(() => {
        if (active) setLoading(false)
      })
    return () => {
      active = false
    }
  }, [])

  return (
    <section className="content-page">
      <div className="page-heading">
        <p className="eyebrow">Pest management</p>
        <h1>Prevent, scout, and intervene with careful thresholds</h1>
      </div>
      {loading && <p className="status-text">Loading pest guides…</p>}
      {error && <p className="error-text" role="alert">{error}</p>}
      <div className="card-grid">
        {items.map((article) => (
          <article key={article.id} className="resource-card">
            <span className="chip">{article.category}</span>
            <h3>{article.title}</h3>
            <p>{article.summary}</p>
            <Link to={`/knowledge/${article.id}`} className="inline-action">
              Read approach <ChevronRight size={14} />
            </Link>
          </article>
        ))}
      </div>
      {!loading && !error && items.length === 0 && <p className="status-text">No pest guides are available yet.</p>}
    </section>
  )
}

function AiAssistantPage({ token }: { token: string | null }) {
  const [question, setQuestion] = useState('')
  const [askedQuestion, setAskedQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [response, setResponse] = useState<ApiChatResponse | null>(null)
  const [requestError, setRequestError] = useState<string | null>(null)

  const askQuestion = async () => {
    const submittedQuestion = question.trim()
    if (!submittedQuestion) return

    setLoading(true)
    setRequestError(null)
    setAskedQuestion(submittedQuestion)
    try {
      const result = await sendChatMessage(submittedQuestion, token)
      setResponse(result)
      setQuestion('')
    } catch (error: unknown) {
      if (isAxiosError<{ detail?: string }>(error)) {
        const detail = error.response?.data?.detail
        setRequestError(
          detail ??
            (error.response
              ? `Chat request failed (HTTP ${error.response.status}).`
              : 'Unable to reach the chat API. Check that the backend is running and its CORS settings allow this frontend origin.'),
        )
      } else {
        setRequestError(error instanceof Error ? error.message : 'An unexpected chat error occurred.')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="content-page">
      <div className="page-heading">
        <p className="eyebrow">AI farmer assistant</p>
        <h1>Ask about soil, crop strategy, or farm decisions</h1>
      </div>

      <div className="assistant-layout">
        <div className="chat-panel">
          <textarea
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Ask: Which organic fertilizers suit tomato in loamy soil?"
            rows={5}
          />
          <button type="button" className="primary-button" onClick={askQuestion} disabled={loading}>
            {loading ? 'Thinking...' : 'Ask assistant'}
          </button>

          {requestError && <p className="error-text" role="alert">{requestError}</p>}

          {response && (
            <div className={`chat-response ${response.answer ? 'has-answer' : 'has-notice'}`}>
              <div className="assistant-result-heading">
                <div>
                  <p className="response-label">{response.answer ? 'Your farming answer' : 'Assistant update'}</p>
                  <span className="assistant-topic">
                    {assistantTopics[response.nlp.intent] ?? response.nlp.intent.replaceAll('_', ' ')}
                  </span>
                </div>
                <span className="assistant-status">{assistantStatuses[response.llm_status] ?? response.llm_status}</span>
              </div>
              {askedQuestion && <p className="asked-question"><strong>You asked:</strong> {askedQuestion}</p>}
              {response.answer ? <AssistantAnswer text={response.answer} /> : <p>{response.message}</p>}
              {(response.llm_status === 'knowledge_fallback' || response.llm_status === 'general_answer') && (
                <p className="assistant-fallback-note">{response.message}</p>
              )}
              {response.sources.length > 0 && (
                <details className="source-box">
                  <summary>Knowledge sources ({response.sources.length})</summary>
                  {response.sources.map((source, index) => (
                    <div key={`${source.document_title}-${index}`} className="source-item">
                      <strong>{source.document_title}</strong>
                      <p>{source.excerpt}</p>
                    </div>
                  ))}
                </details>
              )}
              {response.follow_ups.length > 0 && (
                <div className="follow-up-group">
                  <p className="response-label">You could also ask</p>
                  <div className="follow-up-list">
                    {response.follow_ups.map((followUp) => (
                      <button
                        key={followUp}
                        type="button"
                        className="follow-up-button"
                        onClick={() => setQuestion(followUp)}
                      >
                        {followUp}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        <aside className="info-panel">
          <h3>Suggested prompts</h3>
          <ul>
            <li>How should I prepare soil before rice planting?</li>
            <li>What compost mix works best for tomato beds?</li>
            <li>What is the best organic pest plan for chilli?</li>
          </ul>
          <div className="icon-pill">
            <MessageSquareText size={16} />
            Real answers are enabled when the backend AI service is configured.
          </div>
        </aside>
      </div>
    </section>
  )
}

function AdminPage() {
  const metrics = [
    { label: 'Users', value: '128' },
    { label: 'Document uploads', value: '314' },
    { label: 'Indexed chunks', value: '2.4k' },
    { label: 'Queries today', value: '894' },
  ]

  return (
    <section className="content-page">
      <div className="page-heading">
        <p className="eyebrow">Admin</p>
        <h1>Operational overview</h1>
      </div>

      <div className="stats-grid wide-grid">
        {metrics.map((item) => (
          <div key={item.label} className="stat-card">
            <strong>{item.value}</strong>
            <span>{item.label}</span>
          </div>
        ))}
      </div>

      <div className="two-column-layout">
        <div className="text-panel">
          <h3>Recent health checks</h3>
          <ul>
            <li>Knowledge index healthy and searchable.</li>
            <li>Compost guidance has been updated for the season.</li>
            <li>AI fallback is active when no external model key exists.</li>
          </ul>
        </div>
        <div className="text-panel">
          <h3>Management notes</h3>
          <ul>
            <li>Review new farmland documents during intake.</li>
            <li>Validate user login rates after release.</li>
            <li>Monitor seasonal crop recommendation quality.</li>
          </ul>
        </div>
      </div>
    </section>
  )
}

function NlpTestingPage() {
  const [text, setText] = useState('')
  const [compareTo, setCompareTo] = useState('')
  const [result, setResult] = useState<any>(null)

  const runAnalysis = async () => {
    if (!text.trim()) return
    const response = await analyzeText(text, compareTo)
    setResult(response)
  }

  return (
    <section className="content-page">
      <div className="page-heading">
        <p className="eyebrow">NLP testing</p>
        <h1>Inspect text preprocessing and semantic intent</h1>
      </div>

      <div className="assistant-layout">
        <div className="chat-panel">
          <textarea value={text} onChange={(event) => setText(event.target.value)} rows={5} placeholder="Enter text to analyze" />
          <input
            type="text"
            value={compareTo}
            onChange={(event) => setCompareTo(event.target.value)}
            placeholder="Optional comparison text"
            className="nlp-input"
          />
          <button type="button" className="primary-button" onClick={runAnalysis}>
            Analyze text
          </button>
        </div>

        <aside className="info-panel">
          {result ? (
            <>
              <h3>Summary</h3>
              <ul>
                <li>Intent: {result.intent}</li>
                <li>Confidence: {result.confidence}</li>
                <li>Keywords: {result.keywords?.join(', ') || 'None'}</li>
              </ul>
            </>
          ) : (
            <p>Run a quick NLP check to view cleaned text, lemmas, and intent summary.</p>
          )}
        </aside>
      </div>
    </section>
  )
}

export default App
