-- HBnB Database Schema
-- SQLite compatible SQL script for table generation

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- ===========================================
-- DROP TABLES (in reverse order of dependencies)
-- ===========================================
DROP TABLE IF EXISTS place_amenity;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS amenities;
DROP TABLE IF EXISTS users;

-- ===========================================
-- USERS TABLE
-- ===========================================
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Index for email lookups (login)
CREATE INDEX idx_users_email ON users(email);

-- ===========================================
-- AMENITIES TABLE
-- ===========================================
CREATE TABLE amenities (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Index for name lookups
CREATE INDEX idx_amenities_name ON amenities(name);

-- ===========================================
-- PLACES TABLE
-- ===========================================
CREATE TABLE places (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL CHECK(price > 0),
    latitude DECIMAL(9, 6) CHECK(latitude >= -90.0 AND latitude <= 90.0),
    longitude DECIMAL(10, 6) CHECK(longitude >= -180.0 AND longitude <= 180.0),
    owner_id VARCHAR(36) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Index for owner lookups
CREATE INDEX idx_places_owner ON places(owner_id);

-- ===========================================
-- REVIEWS TABLE
-- ===========================================
CREATE TABLE reviews (
    id VARCHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
    place_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT unique_user_place_review UNIQUE (user_id, place_id)
);

-- Index for place reviews lookups
CREATE INDEX idx_reviews_place ON reviews(place_id);
-- Index for user reviews lookups
CREATE INDEX idx_reviews_user ON reviews(user_id);

-- ===========================================
-- PLACE_AMENITY TABLE (Many-to-Many)
-- ===========================================
CREATE TABLE place_amenity (
    place_id VARCHAR(36) NOT NULL,
    amenity_id VARCHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);

-- Index for amenity lookups
CREATE INDEX idx_place_amenity_place ON place_amenity(place_id);
CREATE INDEX idx_place_amenity_amenity ON place_amenity(amenity_id);
