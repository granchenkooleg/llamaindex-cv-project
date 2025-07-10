
-- Enable the pgvector extension if it's not already installed
CREATE EXTENSION IF NOT EXISTS vector;

-- Create the resumes table with appropriate columns
CREATE TABLE IF NOT EXISTS resumes (
    id SERIAL PRIMARY KEY,
    doc_id TEXT,
    content TEXT,
    metadata JSONB,
    embedding VECTOR(384)
);
