CREATE TABLE IF NOT EXISTS iss_locations (
    id SERIAL PRIMARY KEY,
    latitude DECIMAL(10, 6) NOT NULL,
    longitude DECIMAL(10, 6) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    recorded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_timestamp ON iss_locations(timestamp);
CREATE INDEX idx_recorded_at ON iss_locations(recorded_at);
