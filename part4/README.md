# HBNB Frontend - Part 4

Complete front-end implementation for the HBNB (HolbertonBnB) project with HTML, CSS, and JavaScript.

## Project Overview

This front-end application provides a complete user interface for browsing places, authenticating users, and submitting reviews. It integrates with the HBNB API backend.

## Pages Included

### 1. **Login Page** (login.html)
- User authentication form with email and password fields
- JWT token storage in cookies after successful login
- Error message display for failed login attempts
- Redirect to home page after successful login

### 2. **Index Page** (index.html)
- List of all available places displayed as cards
- Dynamic content loading from API
- Client-side price filtering (up to $10, $50, $100, or All)
- Login link visibility based on authentication status
- "View Details" button for each place

### 3. **Place Details Page** (place.html)
- Detailed information about a specific place
- Display of place features: name, host, price, description, and amenities
- Review section with existing reviews displayed as cards
- Inline review form for authenticated users
- Star rating system for reviews

### 4. **Add Review Page** (add_review.html)
- Dedicated page for adding reviews to a place
- Authentication check with redirect to index if not logged in
- Rating dropdown (1-5 stars)
- Comment textarea
- Success/error message display

## Files Structure

```
part4/
├── index.html          # Main places listing page
├── login.html          # User login page
├── place.html          # Place details page
├── add_review.html     # Add review page
├── styles.css          # All styles for the application
├── scripts.js          # All JavaScript functionality
├── logo.png            # Application logo (to be added)
├── icon.png            # Favicon (to be added)
└── README.md           # This file
```

## Features

### Authentication
- Login form with JWT token management
- Cookie-based session storage
- Automatic token inclusion in API requests
- Logout through cookie deletion

### Places Browsing
- Dynamic place card display
- Place information: name, location, price, description
- View Details button linking to place details page
- Responsive grid layout

### Place Details
- Comprehensive place information display
- Host information
- Price per night
- Description
- Amenities list with checkmarks
- Room details (max guests, bedrooms, bathrooms)

### Reviews System
- Display existing reviews with user names and ratings
- Star rating visualization (★ symbols)
- Add review functionality for authenticated users
- Form validation and submission handling
- Success/error feedback

### Client-Side Filtering
- Real-time price filtering without page reload
- Multiple price range options
- Maintains all place data for seamless filtering

## Setup Instructions

### 1. Add Images
Place the following images in the `part4/` directory:
- `logo.png` - Application logo (recommended size: 200x40px)
- `icon.png` - Favicon (recommended size: 32x32px)

### 2. Update API URL
The default API URL is set to `http://127.0.0.1:5000`. If your API runs on a different URL, update the `API_URL` constant in `scripts.js`:

```javascript
const API_URL = 'http://your-api-url:port';
```

### 3. Serve the Application
You can serve these files using any web server:

#### Using Python
```bash
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000
```

#### Using Node.js (http-server)
```bash
npm install -g http-server
http-server
```

#### Using Live Server in VS Code
Install the "Live Server" extension and right-click on `index.html` to open with Live Server.

## Testing Instructions

### Login Functionality
1. Navigate to `login.html`
2. Enter valid email and password
3. Verify JWT token is stored in cookies (check browser DevTools > Application > Cookies)
4. Verify redirect to `index.html` occurs
5. Test with invalid credentials to verify error message display

### Index Page
1. Navigate to `index.html`
2. Verify places load from API
3. Test price filter dropdown (select different price ranges)
4. Verify login link visibility changes based on authentication
5. Verify "View Details" buttons link correctly

### Place Details
1. Click "View Details" on any place from index page
2. Verify place information loads correctly
3. Check amenities display
4. Verify reviews load and display correctly
5. If authenticated, verify review form appears
6. Submit a test review and verify it appears in the reviews list

### Add Review Page
1. Navigate to `add_review.html?id=<place-id>` directly (replace with actual place ID)
2. Be redirected to `index.html` if not logged in
3. If logged in, verify place name displays
4. Test form validation (try submitting empty form)
5. Submit a review and verify success message
6. Verify redirect to place details page

## W3C Validation

All HTML files are structured following W3C standards:
- ✓ Valid HTML5 document structure
- ✓ Semantic HTML elements (header, main, section, footer)
- ✓ Proper form structure with labels
- ✓ Alt text for images
- ✓ Proper heading hierarchy

To validate each page:
1. Visit https://validator.w3.org/
2. Upload or paste the HTML content
3. Fix any warnings or errors

## API Endpoints Used

The application expects the following API endpoints:

### Authentication
- `POST /api/v1/auth/login` - User login
  - Request: `{ email, password }`
  - Response: `{ access_token }`

### Places
- `GET /api/v1/places` - Get all places
  - Response: `[{ id, name, description, price_per_night, ... }]`
- `GET /api/v1/places/{id}` - Get place details
  - Response: `{ id, name, description, price_per_night, host_name, amenities, ... }`

### Reviews
- `GET /api/v1/places/{id}/reviews` - Get place reviews
  - Response: `[{ rating, comment, user_name, ... }]`
- `POST /api/v1/places/{id}/reviews` - Add a review
  - Headers: `Authorization: Bearer {token}`
  - Request: `{ rating, comment }`
  - Response: `{ success: true }`

## Styling

The CSS follows a modern, responsive design with:
- **Color Palette**: Professional dark blue primary with red accents
- **Typography**: Clean sans-serif fonts
- **Responsive Layout**: Mobile-first approach with breakpoints at 768px and 480px
- **Components**: Cards, forms, buttons with hover effects
- **Fixed Parameters**: 
  - Card margins: 20px
  - Card padding: 10px
  - Card border: 1px solid #ddd
  - Card border radius: 10px

## Browser Compatibility

The application is compatible with:
- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Cookie Management

- **Token Storage**: JWT tokens are stored in browser cookies with 7-day expiration
- **Cookie Path**: Set to `/` for site-wide access
- **Secure Cookies**: For production, consider using `Secure` and `SameSite` flags

## Security Notes

1. **HTTPS**: For production, ensure all communications are over HTTPS
2. **CORS**: Verify CORS headers are properly configured on the API
3. **Token Expiration**: Implement token refresh mechanism for long sessions
4. **XSS Protection**: The application doesn't execute user content as HTML

## Troubleshooting

### API Connection Issues
- Verify the API server is running
- Check CORS headers in API response
- Verify correct API URL in `scripts.js`
- Check browser console for error messages

### Login Issues
- Verify API endpoint returns proper JWT token format
- Check token is stored correctly in cookies
- Verify email/password validation on backend

### Places Not Loading
- Verify API returns correct data format
- Check API response in browser Network tab
- Verify API authentication if required

### Review Submission Fails
- Verify user is authenticated (check cookie)
- Check form validation requirements
- Verify API endpoint for review submission
- Check API request/response format

## Future Enhancements

- User profile page
- Wishlist functionality
- Advanced search and filtering
- Booking system
- Payment integration
- Real-time notifications
- Image upload for reviews
- User ratings and reputation system

## Author

Holberton School HBNB Project - Part 4 (Frontend)

## License

This project is part of the Holberton School curriculum.
