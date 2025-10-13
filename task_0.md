```mermaid
classDiagram
    class PresentationLayer {
      +ServiceAPI
    }
    
    class BusinessLogicLayer {
      +ModelClasses
    }
    
    class PersistenceLayer {
      +DatabaseAccess
    }
    
    PresentationLayer --> BusinessLogicLayer : FacadePattern
    BusinessLogicLayer --> PersistenceLayer : DatabaseOperations
```
