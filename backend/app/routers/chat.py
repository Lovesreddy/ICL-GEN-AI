"""Chat routes backed by the RAG pipeline."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.deps import get_current_user, get_optional_user
from app.models import ChatMessage, ChatSession, ChatSource, User
from app.schemas import ChatAskRequest, ChatAskResponse, ChatMessageOut, ChatSessionOut, SourceOut
from app.services.rag import answer_question

router = APIRouter(prefix="/api/chat", tags=["chat"])


def _store_exchange(db: Session, user: User, payload: ChatAskRequest, result: dict) -> int:
    session = None
    if payload.session_id:
        session = db.scalar(
            select(ChatSession).where(ChatSession.id == payload.session_id, ChatSession.user_id == user.id)
        )
        if session is None:
            raise HTTPException(status_code=404, detail="Chat session not found.")
    if session is None:
        title = payload.question.strip()[:80]
        session = ChatSession(user_id=user.id, title=title)
        db.add(session)
        db.flush()
    db.add(ChatMessage(session_id=session.id, role="user", message=payload.question.strip()))
    assistant = ChatMessage(
        session_id=session.id,
        role="assistant",
        message=result["answer"] or result["message"],
        llm_status=result["llm_status"],
    )
    db.add(assistant)
    db.flush()
    for source in result["sources"]:
        db.add(
            ChatSource(
                message_id=assistant.id,
                document_id=source["document_id"],
                chunk_id=source["chunk_id"],
                page_number=source["page_number"],
                excerpt=source["excerpt"],
                score=source["score"],
                document_title=source["document_title"],
            )
        )
    db.commit()
    return session.id


@router.post("/ask", response_model=ChatAskResponse)
def ask(
    payload: ChatAskRequest,
    db: Session = Depends(get_db),
    user: User | None = Depends(get_optional_user),
) -> ChatAskResponse:
    result = answer_question(db, payload.question)
    session_id = _store_exchange(db, user, payload, result) if user else None
    return ChatAskResponse(session_id=session_id, **result)


@router.get("/sessions", response_model=list[ChatSessionOut])
def sessions(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[ChatSession]:
    return list(
        db.scalars(select(ChatSession).where(ChatSession.user_id == user.id).order_by(ChatSession.created_at.desc())).all()
    )


@router.get("/history", response_model=list[ChatMessageOut])
def history(
    session_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[ChatMessageOut]:
    session = db.scalar(select(ChatSession).where(ChatSession.id == session_id, ChatSession.user_id == user.id))
    if session is None:
        raise HTTPException(status_code=404, detail="Chat session not found.")
    messages = db.scalars(
        select(ChatMessage)
        .where(ChatMessage.session_id == session.id)
        .options(selectinload(ChatMessage.sources))
        .order_by(ChatMessage.created_at.asc())
    ).all()
    output = []
    for message in messages:
        sources = [
            SourceOut(
                document_id=source.document_id,
                document_title=source.document_title,
                page_number=source.page_number,
                chunk_id=source.chunk_id,
                excerpt=source.excerpt,
                score=source.score,
            )
            for source in message.sources
        ]
        output.append(
            ChatMessageOut(
                id=message.id,
                role=message.role,
                message=message.message,
                llm_status=message.llm_status,
                created_at=message.created_at,
                sources=sources,
            )
        )
    return output


@router.delete("/sessions/{session_id}", status_code=204)
def delete_session(session_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> None:
    session = db.scalar(select(ChatSession).where(ChatSession.id == session_id, ChatSession.user_id == user.id))
    if session is None:
        raise HTTPException(status_code=404, detail="Chat session not found.")
    db.delete(session)
    db.commit()
