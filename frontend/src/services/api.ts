import axios from 'axios'

import type {
  ApiChatResponse,
  CropCreatePayload,
  CropItem,
  KnowledgeItem,
  User,
} from '../types'

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000').replace(/\/$/, '')

export const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
})

const authHeaders = (token?: string | null) => {
  if (!token) return {}
  return { Authorization: `Bearer ${token}` }
}

export async function getKnowledgeItems(query?: string): Promise<KnowledgeItem[]> {
  const { data } = await api.get('/knowledge', {
    params: query ? { q: query } : {},
  })
  return data as KnowledgeItem[]
}

export async function getFertilizers(): Promise<KnowledgeItem[]> {
  const { data } = await api.get('/fertilizers')
  return data as KnowledgeItem[]
}

export async function getPests(): Promise<KnowledgeItem[]> {
  const { data } = await api.get('/pests')
  return data as KnowledgeItem[]
}

export async function getCrops(): Promise<CropItem[]> {
  const { data } = await api.get('/crops')
  return data as CropItem[]
}

export async function getCropDetail(cropId: string): Promise<CropItem> {
  const { data } = await api.get(`/crops/${encodeURIComponent(cropId)}`)
  return data as CropItem
}

export async function createCrop(payload: CropCreatePayload, token: string): Promise<CropItem> {
  const { data } = await api.post('/crops', payload, { headers: authHeaders(token) })
  return data as CropItem
}

export async function getKnowledgeDetail(articleId: string): Promise<KnowledgeItem | null> {
  for (const collection of ['/knowledge', '/fertilizers', '/pests']) {
    try {
      const { data } = await api.get(`${collection}/${encodeURIComponent(articleId)}`)
      return data as KnowledgeItem
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.status === 404) continue
      throw error
    }
  }
  return null
}

export async function getCurrentUser(token?: string | null): Promise<User | null> {
  try {
    const { data } = await api.get('/auth/me', { headers: authHeaders(token) })
    return data as User
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.status === 401) return null
    throw error
  }
}

export async function sendChatMessage(question: string, token?: string | null): Promise<ApiChatResponse> {
  const { data } = await api.post(
    '/chat/ask',
    { question, session_id: null },
    { headers: authHeaders(token) },
  )
  return data as ApiChatResponse
}

export async function analyzePhoto(
  image: File,
  cropName: string,
  subjectType: 'crop' | 'soil' | 'fertilizer',
  notes: string,
): Promise<{ answer: string; model: string }> {
  const formData = new FormData()
  formData.append('image', image)
  formData.append('crop_name', cropName)
  formData.append('subject_type', subjectType)
  formData.append('notes', notes)
  formData.append('consent_to_provider', 'true')

  const { data } = await api.post('/photo-guide/analyze', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data as { answer: string; model: string }
}

export async function analyzeText(text: string, compareTo?: string) {
  const { data } = await api.post('/nlp/analyze', { text, compare_to: compareTo || null })
  return data
}
