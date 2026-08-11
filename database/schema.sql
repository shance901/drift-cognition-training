-- Small Business Grants & Funding Database
-- Covers: cybersecurity grants, cybersecurity protection/compliance grants,
-- and general small business grants & funding programs.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS grant_tags;
DROP TABLE IF EXISTS grants;

CREATE TABLE grants (
    id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    name                 TEXT NOT NULL,
    provider             TEXT NOT NULL,          -- issuing agency / organization
    provider_type        TEXT NOT NULL CHECK (provider_type IN
                            ('federal', 'state', 'private', 'nonprofit', 'portal')),
    primary_category      TEXT NOT NULL CHECK (primary_category IN
                            ('cybersecurity', 'cybersecurity_protection', 'small_business_general')),
    description          TEXT NOT NULL,
    eligibility          TEXT,
    funding_amount_text  TEXT,                    -- human-readable amount / range
    funding_amount_min   INTEGER,                 -- USD, nullable
    funding_amount_max   INTEGER,                 -- USD, nullable
    geographic_scope     TEXT,                    -- e.g. "National", "Massachusetts", "California"
    application_status   TEXT,                    -- e.g. "Rolling", "Annual cycle", "Pass-through only"
    how_to_apply          TEXT,
    application_url       TEXT,
    source_url            TEXT,                    -- citation used to populate this record
    last_verified         TEXT,                    -- YYYY-MM-DD, when info was last checked
    notes                 TEXT
);

CREATE TABLE grant_tags (
    grant_id  INTEGER NOT NULL REFERENCES grants(id) ON DELETE CASCADE,
    tag       TEXT NOT NULL,
    PRIMARY KEY (grant_id, tag)
);

CREATE INDEX idx_grants_category ON grants(primary_category);
CREATE INDEX idx_grants_provider_type ON grants(provider_type);
CREATE INDEX idx_grant_tags_tag ON grant_tags(tag);

CREATE VIEW grants_with_tags AS
SELECT g.*, GROUP_CONCAT(t.tag, ', ') AS tags
FROM grants g
LEFT JOIN grant_tags t ON t.grant_id = g.id
GROUP BY g.id;
