# Sequence Diagrams for API Calls

# 1 - User Registration

```mermaid
sequenceDiagram
    participant User as Frontend
    participant API as HBnB API
    participant Logic as Business Logic Layer
    participant Storage as Database (Backend)

    User->>API: POST /users/register
    activate API
    Note right of API: User registration request

    alt Invalid form data
        User-->>User: Show "Invalid input" message
    else Valid data
        API->>Logic: registerUser(userData)
        activate Logic

        alt Validation error
            Logic-->>API: Validation failed
            API-->>User: HTTP 400 Bad Request
            Note left of User: Display validation error
        else Valid request
            Logic->>Storage: saveUser(userData)
            activate Storage

            alt Database unreachable
                Storage-->>Logic: error "Connection timeout"
                Logic-->>API: HTTP 500 Internal Server Error
                API-->>User: Show "Service unavailable"
            else Duplicate user
                Storage-->>Logic: error "Duplicate entry"
                Logic-->>API: HTTP 422 Conflict
                API-->>User: Show "User already exists"
            else Success
                Storage-->>Logic: new user record
                Logic-->>API: success response
                API-->>User: HTTP 201 Created
            end
            deactivate Storage
        end
    end

    deactivate Logic
    deactivate API
```

# 2 - Place Creation

```mermaid
sequenceDiagram
    participant User as Frontend
    participant API as HBnB API
    participant Logic as Business Logic Layer
    participant Storage as Database (Backend)

    User->>API: POST /users/login
    activate API
    Note right of API: User login request

    API->>Logic: authenticateUser(credentials)
    activate Logic

    alt User not found
        Logic-->>API: User not found
        API-->>User: HTTP 404 Not Found
    else Incorrect password
        Logic-->>API: Incorrect password
        API-->>User: HTTP 401 Unauthorized
    else Success
        Logic->>Storage: get User Session(userId)
        activate Storage
        Storage-->>Logic: session data
        Logic-->>API: success response
        API-->>User: HTTP 200 OK
    end

    deactivate Storage
    deactivate Logic
    deactivate API
```

# 3 - Review Submission

```mermaid
sequenceDiagram
    participant User as Frontend
    participant API as HBnB API
    participant Logic as Business Logic Layer
    participant Storage as Database (Backend)

    User->>API: GET /users/profile
    activate API
    Note right of API: Fetch user profile request

    API->>Logic: get User Profile(userId)
    activate Logic

    alt User not found
        Logic-->>API: User not found
        API-->>User: HTTP 404 Not Found
    else Success
        Logic->>Storage: retrieve User Profile(userId)
        activate Storage
        Storage-->>Logic: session data
        Logic-->>API: success response
        API-->>User: HTTP 200 OK
    end

    deactivate Storage
    deactivate Logic
    deactivate API
```

# 4 - Fetching a List of Places

```mermaid
sequenceDiagram
    participant User as Frontend
    participant API as HBnB API
    participant Logic as Business Logic Layer
    participant Storage as Database (Backend)

    User->>API: PUT /users/profile
    activate API
    Note right of API: Update user profile request

    API->>Logic: update User Profile(userId, profileData)
    activate Logic

    alt invalid data
        Logic-->>API: Validation failed
        API-->>User: HTTP 400 Bad Request
    else Success
        Logic->>Storage: save User Profile(userId, profileData)
        activate Storage
        Storage-->>Logic: session data
        Logic-->>API: success response
        API-->>User: HTTP 200 OK
    end

    deactivate API
    deactivate Logic
    deactivate Storage
```
