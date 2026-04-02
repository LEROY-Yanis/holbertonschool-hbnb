-- HBnB Initial Data
-- SQLite compatible SQL script for seeding initial data

-- ===========================================
-- ADMIN USER
-- ===========================================
-- Note: Password hash is for 'admin1234'
-- Generated using: bcrypt.hashpw('admin1234'.encode('utf-8'), bcrypt.gensalt())
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.HYF.L5PQHWsQGe',
    1,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- ===========================================
-- INITIAL AMENITIES
-- ===========================================
INSERT INTO amenities (id, name, description, created_at, updated_at) VALUES
    ('a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d', 'WiFi', 'High-speed wireless internet', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('b2c3d4e5-f6a7-5b6c-9d0e-1f2a3b4c5d6e', 'Swimming Pool', 'Outdoor swimming pool', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('c3d4e5f6-a7b8-6c7d-0e1f-2a3b4c5d6e7f', 'Air Conditioning', 'Central air conditioning', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('d4e5f6a7-b8c9-7d8e-1f2a-3b4c5d6e7f8a', 'Kitchen', 'Fully equipped kitchen', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('e5f6a7b8-c9d0-8e9f-2a3b-4c5d6e7f8a9b', 'Parking', 'Free parking on premises', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('f6a7b8c9-d0e1-9f0a-3b4c-5d6e7f8a9b0c', 'Washing Machine', 'In-unit washer and dryer', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('a7b8c9d0-e1f2-0a1b-4c5d-6e7f8a9b0c1d', 'TV', 'Smart TV with streaming', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('b8c9d0e1-f2a3-1b2c-5d6e-7f8a9b0c1d2e', 'Heating', 'Central heating system', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
