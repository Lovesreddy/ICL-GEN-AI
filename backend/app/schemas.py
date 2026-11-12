"""Pydantic request and response models."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=72)


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class SourceOut(BaseModel):
    document_id: int | None = None
    document_title: str
    page_number: int | None = None
    chunk_id: int | None = None
    excerpt: str
    score: float | None = None
    category: str | None = None


class NlpOut(BaseModel):
    cleaned: str
    keywords: list[str]
    intent: str
    confidence: float
    normalized_query: str


class ChatAskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    session_id: int | None = None


class ChatAskResponse(BaseModel):
    session_id: int | None = None
    answer: str | None = None
    message: str
    llm_status: str
    sources: list[SourceOut]
    follow_ups: list[str]
    nlp: NlpOut


class PhotoGuideAnalysisResponse(BaseModel):
    answer: str
    model: str


class ChatSessionOut(BaseModel):
    id: int
    title: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatMessageOut(BaseModel):
    id: int
    role: str
    message: str
    llm_status: str | None = None
    created_at: datetime
    sources: list[SourceOut] = []


class NlpRequest(BaseModel):
    text: str = Field(min_length=1, max_length=4000)
    compare_to: str | None = Field(default=None, max_length=4000)


class NlpResponse(BaseModel):
    original: str
    cleaned: str
    tokens: list[str]
    tokens_without_stopwords: list[str]
    lemmas: list[str]
    keywords: list[str]
    intent: str
    confidence: float
    intent_scores: dict[str, float]
    normalized_query: str
    semantic_similarity: float | None = None
    lemmatizer: str


class CropOut(BaseModel):
    id: int
    crop_name: str
    soil_type: str
    season: str
    description: str
    climate: str
    water_need: str
    suitable_soil: str
    sowing_season: str
    organic_fertilizers: str
    irrigation: str
    pest_management: str
    harvesting: str


class CropCreateRequest(BaseModel):
    crop_name: str = Field(min_length=2, max_length=80)
    soil_type: str = Field(min_length=2, max_length=200)
    season: str = Field(min_length=2, max_length=80)
    description: str = Field(min_length=10, max_length=1200)
    climate: str = Field(min_length=2, max_length=200)
    water_need: str = Field(min_length=2, max_length=80)
    suitable_soil: str = Field(min_length=10, max_length=1200)
    sowing_season: str = Field(min_length=10, max_length=1200)
    organic_fertilizers: str = Field(min_length=10, max_length=1200)
    irrigation: str = Field(min_length=10, max_length=1200)
    pest_management: str = Field(min_length=10, max_length=1200)
    harvesting: str = Field(min_length=10, max_length=1200)


class RecommendRequest(BaseModel):
    soil_type: str = Field(min_length=2, max_length=80)
    season: str = Field(min_length=2, max_length=40)
    water_availability: str = Field(min_length=2, max_length=40)
    location: str = Field(default="", max_length=120)
    climate: str = Field(default="", max_length=80)


class CropSuggestion(BaseModel):
    crop_name: str
    score: int
    explanation: str
    guidance: str


class RecommendResponse(BaseModel):
    disclaimer: str
    location_note: str | None = None
    suggestions: list[CropSuggestion]


class FertilizerRequest(BaseModel):
    crop: str = Field(min_length=2, max_length=80)
    land_area: float = Field(gt=0, le=10000)
    area_unit: str = Field(pattern="^(acre|hectare)$")
    fertilizer_type: str = Field(min_length=2, max_length=80)


class FertilizerResponse(BaseModel):
    crop: str
    fertilizer_type: str
    land_area_acres: float
    land_area_hectares: float
    quantity: float
    unit: str
    per_acre: float
    per_hectare: float
    guidance: str
    disclaimer: str


class DocumentOut(BaseModel):
    id: int
    filename: str
    title: str
    category: str
    upload_date: datetime
    processing_status: str
    chunk_count: int
    error_message: str | None = None
    source_type: str

    model_config = {"from_attributes": True}


class DashboardOut(BaseModel):
    users: int
    documents: int
    chunks: int
    queries: int
    recent_documents: list[DocumentOut]
    documents_by_category: list[dict]
    health: dict


class FaqOut(BaseModel):
    id: int
    category: str
    question: str
    answer: str


class ArticleOut(BaseModel):
    id: str
    title: str
    category: str
    summary: str
    description: str
    benefits: list[str]
    steps: list[str]
    materials: list[str]
    examples: list[str]
    related_crops: list[str]
    precautions: list[str] = []
