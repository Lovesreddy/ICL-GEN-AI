export type User = {
  id: number
  name: string
  email: string
  role: string
  created_at?: string
}

export type KnowledgeItem = {
  id: string
  title: string
  category: string
  summary: string
  description: string
  benefits: string[]
  steps: string[]
  materials: string[]
  examples: string[]
  related_crops: string[]
  precautions: string[]
  disclaimer?: string
}

export type CropItem = {
  id: number
  crop_name: string
  soil_type: string
  season: string
  description: string
  climate: string
  water_need: string
  suitable_soil: string
  sowing_season: string
  organic_fertilizers: string
  irrigation: string
  pest_management: string
  harvesting: string
}

export type CropCreatePayload = Omit<CropItem, 'id'>

export type ApiChatResponse = {
  answer?: string | null
  message: string
  llm_status: string
  sources: Array<{
    document_title: string
    page_number?: number | null
    excerpt: string
    category?: string | null
    score?: number | null
  }>
  follow_ups: string[]
  nlp: {
    cleaned: string
    keywords: string[]
    intent: string
    confidence: number
    normalized_query: string
  }
}
