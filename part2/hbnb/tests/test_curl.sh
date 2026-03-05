#!/bin/bash
# HBnB API Testing Script
# Run with: bash tests/test_curl.sh

BASE_URL="http://localhost:5000/api/v1"
PASS=0
FAIL=0

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "=============================================="
echo "HBnB API cURL Testing Script"
echo "=============================================="
echo ""

# Function to test an endpoint
test_endpoint() {
    local description="$1"
    local expected_code="$2"
    local method="$3"
    local endpoint="$4"
    local data="$5"
    
    if [ -z "$data" ]; then
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$BASE_URL$endpoint")
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" -H "Content-Type: application/json" -d "$data" "$BASE_URL$endpoint")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" == "$expected_code" ]; then
        echo -e "${GREEN}✓ PASS${NC}: $description (HTTP $http_code)"
        ((PASS++))
    else
        echo -e "${RED}✗ FAIL${NC}: $description (Expected $expected_code, got $http_code)"
        echo "  Response: $body"
        ((FAIL++))
    fi
    
    echo "$body"
}

echo "=== USER TESTS ==="
echo ""

# Test 1: Create user - Success
echo "--- Create User Tests ---"
USER_RESPONSE=$(curl -s -X POST "$BASE_URL/users/" -H "Content-Type: application/json" \
    -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@hbnb.io"}')
USER_ID=$(echo $USER_RESPONSE | grep -o '"id": "[^"]*"' | head -1 | cut -d'"' -f4)

if [ -n "$USER_ID" ]; then
    echo -e "${GREEN}✓ PASS${NC}: Create user - Success"
    echo "  Created user ID: $USER_ID"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC}: Create user - Success"
    echo "  Response: $USER_RESPONSE"
    ((FAIL++))
fi

# Test 2: Create user - Invalid email
echo ""
RESPONSE=$(curl -s -X POST "$BASE_URL/users/" -H "Content-Type: application/json" \
    -d '{"first_name": "Jane", "last_name": "Doe", "email": "invalid-email"}')
if echo "$RESPONSE" | grep -q "error"; then
    echo -e "${GREEN}✓ PASS${NC}: Create user - Invalid email rejected"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC}: Create user - Invalid email should be rejected"
    ((FAIL++))
fi

# Test 3: Create user - Duplicate email
echo ""
RESPONSE=$(curl -s -X POST "$BASE_URL/users/" -H "Content-Type: application/json" \
    -d '{"first_name": "Jane", "last_name": "Doe", "email": "john.doe@hbnb.io"}')
if echo "$RESPONSE" | grep -q "already registered"; then
    echo -e "${GREEN}✓ PASS${NC}: Create user - Duplicate email rejected"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC}: Create user - Duplicate email should be rejected"
    ((FAIL++))
fi

# Test 4: Get all users
echo ""
echo "--- Get User Tests ---"
RESPONSE=$(curl -s "$BASE_URL/users/")
if echo "$RESPONSE" | grep -q "John"; then
    echo -e "${GREEN}✓ PASS${NC}: Get all users"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC}: Get all users"
    ((FAIL++))
fi

# Test 5: Get user by ID
echo ""
RESPONSE=$(curl -s "$BASE_URL/users/$USER_ID")
if echo "$RESPONSE" | grep -q "John"; then
    echo -e "${GREEN}✓ PASS${NC}: Get user by ID"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC}: Get user by ID"
    ((FAIL++))
fi

# Test 6: Get non-existent user
echo ""
RESPONSE=$(curl -s "$BASE_URL/users/nonexistent-id")
if echo "$RESPONSE" | grep -q "not found"; then
    echo -e "${GREEN}✓ PASS${NC}: Get non-existent user returns 404"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC}: Get non-existent user should return 404"
    ((FAIL++))
fi

# Test 7: Update user
echo ""
echo "--- Update User Tests ---"
RESPONSE=$(curl -s -X PUT "$BASE_URL/users/$USER_ID" -H "Content-Type: application/json" \
    -d '{"first_name": "Johnny", "last_name": "Doe", "email": "johnny.doe@hbnb.io"}')
if echo "$RESPONSE" | grep -q "Johnny"; then
    echo -e "${GREEN}✓ PASS${NC}: Update user"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC}: Update user"
    ((FAIL++))
fi

echo ""
echo "=== AMENITY TESTS ==="
echo ""

# Test 8: Create amenity
echo "--- Create Amenity Tests ---"
AMENITY_RESPONSE=$(curl -s -X POST "$BASE_URL/amenities/" -H "Content-Type: application/json" \
    -d '{"name": "Wi-Fi", "description": "High-speed internet"}')
AMENITY_ID=$(echo $AMENITY_RESPONSE | grep -o '"id": "[^"]*"' | head -1 | cut -d'"' -f4)

if [ -n "$AMENITY_ID" ]; then
    echo -e "${GREEN}✓ PASS${NC}: Create amenity"
    echo "  Created amenity ID: $AMENITY_ID"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC}: Create amenity"
    ((FAIL++))
fi

# Test 9: Create amenity - Empty name
echo ""
RESPONSE=$(curl -s -X POST "$BASE_URL/amenities/" -H "Content-Type: application/json" \
    -d '{"name": ""}')
if echo "$RESPONSE" | grep -q "error"; then
    echo -e "${GREEN}✓ PASS${NC}: Create amenity - Empty name rejected"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC}: Create amenity - Empty name should be rejected"
    ((FAIL++))
fi

# Test 10: Get all amenities
echo ""
echo "--- Get Amenity Tests ---"
RESPONSE=$(curl -s "$BASE_URL/amenities/")
if echo "$RESPONSE" | grep -q "Wi-Fi"; then
    echo -e "${GREEN}✓ PASS${NC}: Get all amenities"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC}: Get all amenities"
    ((FAIL++))
fi

# Test 11: Update amenity
echo ""
echo "--- Update Amenity Tests ---"
RESPONSE=$(curl -s -X PUT "$BASE_URL/amenities/$AMENITY_ID" -H "Content-Type: application/json" \
    -d '{"name": "Fast Wi-Fi", "description": "Very fast internet"}')
if echo "$RESPONSE" | grep -q "Fast Wi-Fi"; then
    echo -e "${GREEN}✓ PASS${NC}: Update amenity"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC}: Update amenity"
    ((FAIL++))
fi

echo ""
echo "=== PLACE TESTS ==="
echo ""

# Test 12: Create place
echo "--- Create Place Tests ---"
PLACE_RESPONSE=$(curl -s -X POST "$BASE_URL/places/" -H "Content-Type: application/json" \
    -d "{\"title\": \"Cozy Apartment\", \"description\": \"A nice place\", \"price\": 100.0, \"latitude\": 37.7749, \"longitude\": -122.4194, \"owner_id\": \"$USER_ID\", \"amenities\": [\"$AMENITY_ID\"]}")
PLACE_ID=$(echo $PLACE_RESPONSE | grep -o '"id": "[^"]*"' | head -1 | cut -d'"' -f4)

if [ -n "$PLACE_ID" ]; then
    echo -e "${GREEN}✓ PASS${NC}: Create place"
    echo "  Created place ID: $PLACE_ID"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC}: Create place"
    echo "  Response: $PLACE_RESPONSE"
    ((FAIL++))
fi

# Test 13: Create place - Invalid price
echo ""
RESPONSE=$(curl -s -X POST "$BASE_URL/places/" -H "Content-Type: application/json" \
    -d "{\"title\": \"Test\", \"description\": \"\", \"price\": -100.0, \"latitude\": 0, \"longitude\": 0, \"owner_id\": \"$USER_ID\"}")
if echo "$RESPONSE" | grep -q "error"; then
    echo -e "${GREEN}✓ PASS${NC}: Create place - Negative price rejected"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC}: Create place - Negative price should be rejected"
    ((FAIL++))
fi

# Test 14: Create place - Invalid latitude
echo ""
RESPONSE=$(curl -s -X POST "$BASE_URL/places/" -H "Content-Type: application/json" \
    -d "{\"title\": \"Test\", \"description\": \"\", \"price\": 100.0, \"latitude\": 100, \"longitude\": 0, \"owner_id\": \"$USER_ID\"}")
if echo "$RESPONSE" | grep -q "error"; then
    echo -e "${GREEN}✓ PASS${NC}: Create place - Invalid latitude rejected"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC}: Create place - Invalid latitude should be rejected"
    ((FAIL++))
fi

# Test 15: Get all places
echo ""
echo "--- Get Place Tests ---"
RESPONSE=$(curl -s "$BASE_URL/places/")
if echo "$RESPONSE" | grep -q "Cozy Apartment"; then
    echo -e "${GREEN}✓ PASS${NC}: Get all places"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC}: Get all places"
    ((FAIL++))
fi

# Test 16: Get place by ID
echo ""
RESPONSE=$(curl -s "$BASE_URL/places/$PLACE_ID")
if echo "$RESPONSE" | grep -q "owner"; then
    echo -e "${GREEN}✓ PASS${NC}: Get place by ID (includes owner details)"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC}: Get place by ID"
    ((FAIL++))
fi

echo ""
echo "=== REVIEW TESTS ==="
echo ""

# Test 17: Create review
echo "--- Create Review Tests ---"
REVIEW_RESPONSE=$(curl -s -X POST "$BASE_URL/reviews/" -H "Content-Type: application/json" \
    -d "{\"text\": \"Great place!\", \"rating\": 5, \"user_id\": \"$USER_ID\", \"place_id\": \"$PLACE_ID\"}")
REVIEW_ID=$(echo $REVIEW_RESPONSE | grep -o '"id": "[^"]*"' | head -1 | cut -d'"' -f4)

if [ -n "$REVIEW_ID" ]; then
    echo -e "${GREEN}✓ PASS${NC}: Create review"
    echo "  Created review ID: $REVIEW_ID"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC}: Create review"
    echo "  Response: $REVIEW_RESPONSE"
    ((FAIL++))
fi

# Test 18: Create review - Invalid rating
echo ""
RESPONSE=$(curl -s -X POST "$BASE_URL/reviews/" -H "Content-Type: application/json" \
    -d "{\"text\": \"Bad review\", \"rating\": 0, \"user_id\": \"$USER_ID\", \"place_id\": \"$PLACE_ID\"}")
if echo "$RESPONSE" | grep -q "error"; then
    echo -e "${GREEN}✓ PASS${NC}: Create review - Rating 0 rejected"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC}: Create review - Rating 0 should be rejected"
    ((FAIL++))
fi

# Test 19: Create review - Rating too high
echo ""
RESPONSE=$(curl -s -X POST "$BASE_URL/reviews/" -H "Content-Type: application/json" \
    -d "{\"text\": \"Amazing\", \"rating\": 6, \"user_id\": \"$USER_ID\", \"place_id\": \"$PLACE_ID\"}")
if echo "$RESPONSE" | grep -q "error"; then
    echo -e "${GREEN}✓ PASS${NC}: Create review - Rating 6 rejected"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC}: Create review - Rating 6 should be rejected"
    ((FAIL++))
fi

# Test 20: Get reviews for place
echo ""
echo "--- Get Review Tests ---"
RESPONSE=$(curl -s "$BASE_URL/places/$PLACE_ID/reviews")
if echo "$RESPONSE" | grep -q "Great place"; then
    echo -e "${GREEN}✓ PASS${NC}: Get reviews for place"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC}: Get reviews for place"
    ((FAIL++))
fi

# Test 21: Update review
echo ""
echo "--- Update Review Tests ---"
RESPONSE=$(curl -s -X PUT "$BASE_URL/reviews/$REVIEW_ID" -H "Content-Type: application/json" \
    -d '{"text": "Updated review", "rating": 4}')
if echo "$RESPONSE" | grep -q "Updated review"; then
    echo -e "${GREEN}✓ PASS${NC}: Update review"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC}: Update review"
    ((FAIL++))
fi

# Test 22: Delete review
echo ""
echo "--- Delete Review Tests ---"
RESPONSE=$(curl -s -X DELETE "$BASE_URL/reviews/$REVIEW_ID")
if echo "$RESPONSE" | grep -q "deleted"; then
    echo -e "${GREEN}✓ PASS${NC}: Delete review"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC}: Delete review"
    ((FAIL++))
fi

# Test 23: Verify review deleted
echo ""
RESPONSE=$(curl -s "$BASE_URL/reviews/$REVIEW_ID")
if echo "$RESPONSE" | grep -q "not found"; then
    echo -e "${GREEN}✓ PASS${NC}: Verify review deleted"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC}: Review should not exist"
    ((FAIL++))
fi

echo ""
echo "=============================================="
echo "Test Results: ${GREEN}$PASS PASSED${NC}, ${RED}$FAIL FAILED${NC}"
echo "=============================================="
