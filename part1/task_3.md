# Sequence Diagrams for API Calls

# 1 - User Registration

```mermaid
sequenceDiagram
    participant User as Frontend
    participant Service as HBnB Service
    participant Logic as Business Logic Layer
    participant Storage as Database (Backend)

    User->>Service: POST /users/register
    activate Service
    Note right of Service: User registration request

    alt Invalid form data
        User-->>User: Show "Invalid input" message
    else Valid data
        Service->>Logic: registerUser(userData)
        activate Logic

        alt Validation error
            Logic-->>Service: Validation failed
            Service-->>User: HTTP 400 Bad Request
            Note left of User: Display validation error
        else Valid request
            Logic->>Storage: saveUser(userData)
            activate Storage

            alt Database unreachable
                Storage-->>Logic: error "Connection timeout"
                Logic-->>Service: HTTP 500 Internal Server Error
                Service-->>User: Show "Service unavailable"
            else Duplicate user
                Storage-->>Logic: error "Duplicate entry"
                Logic-->>Service: HTTP 422 Conflict
                Service-->>User: Show "User already exists"
            else Success
                Storage-->>Logic: new user record
                Logic-->>Service: success response
                Service-->>User: HTTP 201 Created
            end
            deactivate Storage
        end
    end

    deactivate Logic
    deactivate Service
```

# 2 - Place Creation

```mermaid
sequenceDiagram
    participant User as Frontend
    participant Service as HBnB Service
    participant Logic as Business Logic Layer
    participant Storage as Database (Backend)

    User->>Service: POST /users/login
    activate Service
    Note right of Service: User login request

    Service->>Logic: authenticateUser(credentials)
    activate Logic

    alt User not found
        Logic-->>Service: User not found
        Service-->>User: HTTP 404 Not Found
    else Incorrect password
        Logic-->>Service: Incorrect password
        Service-->>User: HTTP 401 Unauthorized
    else Success
        Logic->>Storage: getUserSession(userId)
        activate Storage
        Storage-->>Logic: session data
        Logic-->>Service: success response
        Service-->>User: HTTP 200 OK
    end

    deactivate Storage
    deactivate Logic
    deactivate Service
```

# 3 - Review Submission

# 4 - Fetching a List of Places
