CREATE TABLE IF NOT EXISTS "secret-santa".stations (
    id SERIAL PRIMARY KEY,
    station_name VARCHAR(255) NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    selected_by_user_id INT,
    selected_at TIMESTAMP
);