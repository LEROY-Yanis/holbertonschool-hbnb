📘 Part 1: Technical Documentation

Task 1: High-Level Package Diagram (3-Layer Architecture + Facade)

Create a package diagram that shows the 3 layers:

Presentation / API Layer (REST endpoints)

Business Logic Layer (Models, core logic, Facade interface)

Persistence Layer (Data access layer: repositories, DB handlers)

Show how the layers communicate via the Facade design pattern.

Include short notes explaining each layer’s responsibilities and how the facade simplifies communication.

Task 2: Detailed Class Diagram (Business Logic Layer)

Create class diagrams for:

User, Place, Review, Amenity, and a shared base like BaseModel.

For each class, list:

Attributes (with types)

Key methods

Show relationships:

Place belongs to a User (owner)

Place has multiple Amenity objects

Place has multiple Review objects

Review links a User and a Place

Indicate multiplicity (1.., 0.., etc.)

If there are useful business methods (e.g. average rating), show or document them.

Task 3: Sequence Diagrams for API Calls
Create sequence diagrams for at least 4 REST API endpoints showing how data flows between:

Client → API (Presentation Layer)

Business Logic (Facade, Models)

Persistence Layer (Repositories)

Example API calls:

Register a user (POST /users)

Create a place (POST /places)

Submit a review (POST /places/<id>/reviews)

Fetch list of places (GET /places)

Each diagram should show method calls, return values, validation steps, and error handling.

Task 4: Documentation Compilation

Write an introduction explaining the purpose of the document.

Organize it into logical sections:

Architecture & Package Diagram

Business Logic Layer Class Diagram

API Call Sequence Diagrams

For each diagram:

Explain what it shows

Design decisions taken

How it fits in the overall architecture

Export it to a shareable format: Markdown with Mermaid, PDF, or Word document
