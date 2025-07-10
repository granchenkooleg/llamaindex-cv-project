-- db/create_resumes_table.sql

DROP TABLE IF EXISTS resumes;

CREATE TABLE resumes (
    id SERIAL PRIMARY KEY,
    doc_id TEXT,
    content TEXT,
    metadata JSONB,
    embedding VECTOR(1536)
);