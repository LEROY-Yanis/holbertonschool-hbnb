```mermaid
classDiagram
    class PresentationLayer {
      +UserService
      +PlaceService
      +APIEndpoint
    }
    
    class BusinessLogicLayer {
      +User
      +Place
      +Review
      +Amenity
    }
    
    class PersistenceLayer {
      +Database access
      +Repositories
    }
    
    PresentationLayer --> BusinessLogicLayer : Facade Pattern
    BusinessLogicLayer --> PersistenceLayer : Database Operations
```