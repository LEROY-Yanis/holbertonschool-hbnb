```mermaid
classDiagram
    class PresentationLayer {
      +UserService
      +PPlaceService
      +APIEndpoint
    }
    
    class BusinessLogicLayer {
      +User
      +Place
      +Review
      +Amenity
    }
    
    class PersistenceLayer {
      +Database Access
      +Repositories
    }
    
    PresentationLayer --> BusinessLogicLayer : FacadePattern
    BusinessLogicLayer --> PersistenceLayer : DatabaseOperations
```
