-- PostgreSQL-compatible initial schema.
-- SQLite development uses SQLAlchemy metadata.create_all(), which mirrors this design.
-- Integer primary keys below map to SERIAL / IDENTITY on PostgreSQL.

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(32) NOT NULL DEFAULT 'farmer',
    created_at TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_users_email ON users (email);
CREATE INDEX IF NOT EXISTS ix_users_role ON users (role);

CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(64) NOT NULL,
    stored_path VARCHAR(500) NOT NULL,
    source_type VARCHAR(32) NOT NULL DEFAULT 'upload',
    upload_date TIMESTAMP NOT NULL,
    processing_status VARCHAR(32) NOT NULL DEFAULT 'pending',
    chunk_count INTEGER NOT NULL DEFAULT 0,
    error_message TEXT
);
CREATE INDEX IF NOT EXISTS ix_documents_category ON documents (category);
CREATE INDEX IF NOT EXISTS ix_documents_status ON documents (processing_status);

CREATE TABLE IF NOT EXISTS document_chunks (
    id INTEGER PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    page_number INTEGER,
    token_count INTEGER NOT NULL DEFAULT 0,
    category VARCHAR(64) NOT NULL,
    embedding BYTEA
);
CREATE INDEX IF NOT EXISTS ix_chunks_document ON document_chunks (document_id);
CREATE INDEX IF NOT EXISTS ix_chunks_category ON document_chunks (category);

CREATE TABLE IF NOT EXISTS chat_sessions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    created_at TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_sessions_user ON chat_sessions (user_id);

CREATE TABLE IF NOT EXISTS chat_messages (
    id INTEGER PRIMARY KEY,
    session_id INTEGER NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role VARCHAR(16) NOT NULL,
    message TEXT NOT NULL,
    llm_status VARCHAR(32),
    created_at TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_messages_session ON chat_messages (session_id);

CREATE TABLE IF NOT EXISTS chat_sources (
    id INTEGER PRIMARY KEY,
    message_id INTEGER NOT NULL REFERENCES chat_messages(id) ON DELETE CASCADE,
    document_id INTEGER REFERENCES documents(id) ON DELETE SET NULL,
    chunk_id INTEGER REFERENCES document_chunks(id) ON DELETE SET NULL,
    page_number INTEGER,
    excerpt TEXT NOT NULL,
    score DOUBLE PRECISION,
    document_title VARCHAR(255) NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS ix_sources_message ON chat_sources (message_id);

CREATE TABLE IF NOT EXISTS crop_information (
    id INTEGER PRIMARY KEY,
    crop_name VARCHAR(80) NOT NULL UNIQUE,
    soil_type VARCHAR(200) NOT NULL,
    season VARCHAR(120) NOT NULL,
    description TEXT NOT NULL,
    cultivation_details TEXT NOT NULL,
    climate VARCHAR(200) NOT NULL DEFAULT '',
    water_need VARCHAR(32) NOT NULL DEFAULT 'medium'
);
CREATE INDEX IF NOT EXISTS ix_crops_name ON crop_information (crop_name);
CREATE INDEX IF NOT EXISTS ix_crops_season ON crop_information (season);

CREATE TABLE IF NOT EXISTS schema_migrations (
    version VARCHAR(64) PRIMARY KEY,
    applied_at TIMESTAMP NOT NULL
);
