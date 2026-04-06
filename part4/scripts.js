// ========================================
// CONFIGURATION
// ========================================

const API_URL = 'http://127.0.0.1:5000';

// ========================================
// UTILITY FUNCTIONS
// ========================================

/**
 * Get cookie value by name
 * @param {string} name - Cookie name
 * @returns {string|null} Cookie value or null
 */
function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i].trim();
        if (c.indexOf(nameEQ) === 0) {
            return decodeURIComponent(c.substring(nameEQ.length));
        }
    }
    return null;
}

/**
 * Set cookie with expiration
 * @param {string} name - Cookie name
 * @param {string} value - Cookie value
 * @param {number} days - Expiration days
 */
function setCookie(name, value, days = 7) {
    const expiration = new Date();
    expiration.setTime(expiration.getTime() + (days * 24 * 60 * 60 * 1000));
    const expires = "expires=" + expiration.toUTCString();
    document.cookie = name + "=" + encodeURIComponent(value) + ";" + expires + ";path=/";
}

/**
 * Extract query parameter from URL
 * @param {string} param - Parameter name
 * @returns {string|null} Parameter value or null
 */
function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

/**
 * Show message to user
 * @param {string} message - Message text
 * @param {string} type - 'success', 'error', or 'info'
 * @param {string} elementId - Element ID to display message
 */
function showMessage(message, type = 'info', elementId = 'error-message') {
    const messageElement = document.getElementById(elementId);
    if (messageElement) {
        messageElement.textContent = message;
        messageElement.className = `message ${type}`;
        messageElement.style.display = 'block';
    }
}

// ========================================
// LOGIN PAGE FUNCTIONALITY
// ========================================

/**
 * Handle login form submission
 */
function setupLoginForm() {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch(`${API_URL}/api/v1/auth/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    // Store token in cookie
                    setCookie('token', data.access_token, 7);
                    // Redirect to home page
                    window.location.href = 'index.html';
                } else {
                    const error = await response.json();
                    showMessage('Login failed: ' + (error.message || response.statusText), 'error', 'error-message');
                }
            } catch (error) {
                console.error('Login error:', error);
                showMessage('An error occurred during login. Please try again.', 'error', 'error-message');
            }
        });
    }
}

// ========================================
// INDEX PAGE FUNCTIONALITY
// ========================================

let allPlaces = [];

/**
 * Check if user is authenticated
 */
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (loginLink) {
        if (!token) {
            loginLink.style.display = 'block';
        } else {
            loginLink.style.display = 'none';
        }
    }

    return token;
}

/**
 * Fetch places from API
 */
async function fetchPlaces(token = null) {
    const placesList = document.getElementById('places-list');

    if (!placesList) return;

    try {
        const headers = {
            'Content-Type': 'application/json'
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_URL}/api/v1/places`, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const data = await response.json();
            allPlaces = Array.isArray(data) ? data : (data.places || []);
            displayPlaces(allPlaces);
        } else {
            placesList.innerHTML = '<p>Failed to load places. Please try again later.</p>';
            console.error('Failed to fetch places:', response.status);
        }
    } catch (error) {
        console.error('Error fetching places:', error);
        placesList.innerHTML = '<p>Error loading places. Please refresh the page.</p>';
    }
}

/**
 * Display places as cards
 * @param {Array} places - Array of place objects
 */
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');

    if (!placesList) return;

    if (!places || places.length === 0) {
        placesList.innerHTML = '<p>No places found.</p>';
        return;
    }

    placesList.innerHTML = '';

    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';

        const image = place.image_url || 'https://via.placeholder.com/280x200?text=Place+Image';
        const location = place.city || 'Unknown Location';
        const price = place.price_per_night || 'N/A';
        const name = place.name || 'Unknown Place';
        const description = place.description || '';
        const placeId = place.id;

        placeCard.innerHTML = `
            <img src="${image}" alt="${name}">
            <h3>${name}</h3>
            <p class="location">${location}</p>
            <p class="price">$${price} / night</p>
            <p class="description">${description.substring(0, 100)}${description.length > 100 ? '...' : ''}</p>
            <a href="place.html?id=${placeId}" class="details-button">View Details</a>
        `;

        placesList.appendChild(placeCard);
    });
}

/**
 * Setup price filter
 */
function setupPriceFilter() {
    const priceFilter = document.getElementById('price-filter');

    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            const maxPrice = event.target.value;

            if (!maxPrice) {
                displayPlaces(allPlaces);
            } else {
                const filteredPlaces = allPlaces.filter(place => {
                    return parseInt(place.price_per_night) <= parseInt(maxPrice);
                });
                displayPlaces(filteredPlaces);
            }
        });
    }
}

/**
 * Initialize index page
 */
function initIndexPage() {
    const placesList = document.getElementById('places-list');

    if (placesList) {
        checkAuthentication();
        const token = getCookie('token');
        fetchPlaces(token);
        setupPriceFilter();
    }
}

// ========================================
// PLACE DETAILS PAGE FUNCTIONALITY
// ========================================

/**
 * Fetch and display place details
 */
async function fetchPlaceDetails(token, placeId) {
    const placeDetails = document.getElementById('place-details');

    if (!placeDetails) return;

    try {
        const headers = {
            'Content-Type': 'application/json'
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_URL}/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
            fetchPlaceReviews(placeId);
        } else {
            placeDetails.innerHTML = '<p>Failed to load place details.</p>';
            console.error('Failed to fetch place:', response.status);
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
        placeDetails.innerHTML = '<p>Error loading place details.</p>';
    }
}

/**
 * Display place details
 * @param {Object} place - Place object
 */
function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');

    if (!placeDetails) return;

    const image = place.image_url || 'https://via.placeholder.com/400x300?text=Place';
    const amenitiesHtml = place.amenities && place.amenities.length > 0
        ? place.amenities.map(a => `<li>${a.name || a}</li>`).join('')
        : '<li>No amenities listed</li>';

    placeDetails.innerHTML = `
        <div class="place-info">
            <div class="place-info-left">
                <img src="${image}" alt="${place.name}">
                <h1>${place.name}</h1>
                <p class="host"><strong>Host:</strong> ${place.host_name || 'Unknown'}</p>
                <p class="price"><strong>$${place.price_per_night} / night</strong></p>
            </div>
            <div class="place-info-right">
                <p class="description">${place.description}</p>
                <div class="amenities">
                    <h3>Amenities</h3>
                    <ul>${amenitiesHtml}</ul>
                </div>
                <div>
                    <p><strong>Max Guests:</strong> ${place.max_guests || 'N/A'}</p>
                    <p><strong>Bedrooms:</strong> ${place.bedrooms || 'N/A'}</p>
                    <p><strong>Bathrooms:</strong> ${place.bathrooms || 'N/A'}</p>
                </div>
            </div>
        </div>
    `;
}

/**
 * Fetch and display place reviews
 */
async function fetchPlaceReviews(placeId) {
    const reviewsList = document.getElementById('reviews-list');

    if (!reviewsList) return;

    try {
        const response = await fetch(`${API_URL}/api/v1/places/${placeId}/reviews`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const reviews = await response.json();
            displayReviews(reviews);
        } else {
            console.error('Failed to fetch reviews:', response.status);
        }
    } catch (error) {
        console.error('Error fetching reviews:', error);
    }
}

/**
 * Display reviews
 * @param {Array} reviews - Array of review objects
 */
function displayReviews(reviews) {
    const reviewsList = document.getElementById('reviews-list');

    if (!reviewsList) return;

    if (!reviews || reviews.length === 0) {
        reviewsList.innerHTML = '<p>No reviews yet. Be the first to review!</p>';
        return;
    }

    reviewsList.innerHTML = '';

    reviews.forEach(review => {
        const reviewCard = document.createElement('div');
        reviewCard.className = 'review-card';

        const rating = review.rating || 0;
        const stars = '★'.repeat(rating) + '☆'.repeat(5 - rating);

        reviewCard.innerHTML = `
            <div class="user-info">
                <span class="user-name">${review.user_name || 'Anonymous'}</span>
                <span class="rating">${stars} (${rating}/5)</span>
            </div>
            <p class="comment">${review.comment}</p>
        `;

        reviewsList.appendChild(reviewCard);
    });
}

/**
 * Initialize place details page
 */
function initPlaceDetailsPage() {
    const placeDetails = document.getElementById('place-details');

    if (placeDetails) {
        checkAuthentication();
        const placeId = getQueryParam('id');

        if (!placeId) {
            placeDetails.innerHTML = '<p>No place selected. Please go back and select a place.</p>';
            return;
        }

        const token = getCookie('token');
        const addReviewSection = document.getElementById('add-review');

        // Show/hide add review section based on authentication
        if (addReviewSection) {
            if (!token) {
                addReviewSection.style.display = 'none';
            } else {
                addReviewSection.style.display = 'block';
                setupInlineReviewForm(token, placeId);
            }
        }

        fetchPlaceDetails(token, placeId);
    }
}

/**
 * Setup inline review form on place details page
 */
function setupInlineReviewForm(token, placeId) {
    const reviewForm = document.getElementById('review-form');

    if (!reviewForm) return;

    reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const rating = document.getElementById('rating').value;
        const comment = document.getElementById('comment').value;

        if (!rating || !comment) {
            showMessage('Please fill in all fields', 'error', 'review-message');
            return;
        }

        try {
            const response = await fetch(`${API_URL}/api/v1/places/${placeId}/reviews`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    rating: parseInt(rating),
                    comment: comment
                })
            });

            if (response.ok) {
                showMessage('Review submitted successfully!', 'success', 'review-message');
                reviewForm.reset();
                // Refresh reviews
                fetchPlaceReviews(placeId);
            } else {
                const error = await response.json();
                showMessage('Failed to submit review: ' + (error.message || 'Unknown error'), 'error', 'review-message');
            }
        } catch (error) {
            console.error('Error submitting review:', error);
            showMessage('An error occurred while submitting your review', 'error', 'review-message');
        }
    });
}

// ========================================
// ADD REVIEW PAGE FUNCTIONALITY
// ========================================

/**
 * Initialize add review page
 */
function initAddReviewPage() {
    const addReviewContainer = document.querySelector('.add-review-container');

    if (addReviewContainer) {
        const token = checkAuthenticationStrict();
        const placeId = getQueryParam('id');

        if (!placeId) {
            window.location.href = 'index.html';
            return;
        }

        fetchPlaceName(placeId);
        setupAddReviewForm(token, placeId);
    }
}

/**
 * Check authentication and redirect if not authenticated
 */
function checkAuthenticationStrict() {
    const token = getCookie('token');

    if (!token) {
        window.location.href = 'index.html';
        return null;
    }

    return token;
}

/**
 * Fetch and display place name
 */
async function fetchPlaceName(placeId) {
    try {
        const response = await fetch(`${API_URL}/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const place = await response.json();
            const placeInfo = document.getElementById('place-info');
            if (placeInfo) {
                placeInfo.textContent = `Adding review for: ${place.name}`;
            }
        }
    } catch (error) {
        console.error('Error fetching place name:', error);
    }
}

/**
 * Setup add review form
 */
function setupAddReviewForm(token, placeId) {
    const reviewForm = document.getElementById('review-form');

    if (!reviewForm) return;

    reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const rating = document.getElementById('rating').value;
        const comment = document.getElementById('comment').value;

        if (!rating || !comment) {
            showMessage('Please fill in all fields', 'error', 'message');
            return;
        }

        try {
            const response = await fetch(`${API_URL}/api/v1/places/${placeId}/reviews`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    rating: parseInt(rating),
                    comment: comment
                })
            });

            if (response.ok) {
                showMessage('Review submitted successfully! Redirecting...', 'success', 'message');
                // Redirect back to place details after 2 seconds
                setTimeout(() => {
                    window.location.href = `place.html?id=${placeId}`;
                }, 2000);
            } else {
                const error = await response.json();
                showMessage('Failed to submit review: ' + (error.message || 'Unknown error'), 'error', 'message');
            }
        } catch (error) {
            console.error('Error submitting review:', error);
            showMessage('An error occurred while submitting your review', 'error', 'message');
        }
    });
}

// ========================================
// PAGE INITIALIZATION
// ========================================

/**
 * Initialize based on current page
 */
document.addEventListener('DOMContentLoaded', () => {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';

    // Setup login form if on login page
    if (currentPage === 'login.html' || document.getElementById('login-form')) {
        setupLoginForm();
    }

    // Setup index page
    if (currentPage === 'index.html' || document.getElementById('places-list')) {
        initIndexPage();
    }

    // Setup place details page
    if (currentPage === 'place.html' || document.getElementById('place-details')) {
        initPlaceDetailsPage();
    }

    // Setup add review page
    if (currentPage === 'add_review.html' || document.querySelector('.add-review-container')) {
        initAddReviewPage();
    }
});
