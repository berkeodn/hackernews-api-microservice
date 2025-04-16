# HackerNews Stories API

## Overview

The HackerNews Stories API is a FastAPI-based microservice that allows users to explore and interact with top stories from Hacker News. It includes features such as fetching stories, filtering by author or score, and retrieving statistics about top authors. The project also includes an ETL (Extract, Transform, Load) pipeline to periodically fetch and update story data from the Hacker News API.

## Technology Stack

The project is built using the following technologies:

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python.
- **SQLAlchemy**: An ORM (Object-Relational Mapper) for interacting with the PostgreSQL database.
- **PostgreSQL**: A powerful, open-source relational database system.
- **APScheduler**: A Python library for scheduling tasks, used for running the ETL pipeline periodically.
- **Requests**: A Python library for making HTTP requests to external APIs.
- **Docker**: Used to containerize the application and its dependencies.
- **Docker Compose**: For orchestrating multi-container setups (FastAPI app, PostgreSQL, and pgAdmin).
- **SlowAPI**: A rate-limiting middleware for FastAPI to control API usage.
- **Pydantic**: For data validation and serialization in FastAPI.

## Features

- **RESTful API**:
  - Fetch paginated lists of stories.
  - Search and filter stories by author, score, or keywords.
  - Retrieve detailed information about a specific story.
  - Get statistics about top authors based on story scores.
- **ETL Pipeline**:
  - Periodically fetch top stories and their details from Hacker News.
  - Upsert (update or insert) story data into a PostgreSQL database.
  - Log errors encountered during the ETL process.
- **Rate Limiting**:
  - Protect the API with rate limits using `slowapi`.
- **Authentication**:
  - API key-based authentication for secure access.
- **Scheduler**:
  - Automatically run the ETL job every 1 hour using `APScheduler`.

## Project Structure

blackkite_case/                     # Root directory of the project
├── app/                            # Main application directory
│   ├── db/                         # Database-related files
│   │   ├── __init__.py             # Empty file to mark this directory as a Python package
│   │   ├── models.py               # SQLAlchemy models for database tables (e.g., Story, ETLError)
│   │   ├── schema.sql              # SQL schema file for database initialization (if applicable)
│   │   ├── session.py              # Database session management (e.g., connection setup, session lifecycle)
│   ├── dependencies/               # Dependency injection utilities
│   │   ├── auth.py                 # API key authentication logic for securing endpoints
│   ├── routers/                    # API route definitions
│   │   ├── stories.py              # Routes for handling story-related API endpoints
│   ├── schemas/                    # Pydantic schemas for request/response validation
│   │   ├── __init__.py             # Empty file to mark this directory as a Python package
│   │   ├── schemas.py              # Pydantic models for validating and serializing API data
│   ├── scheduler.py                # Scheduler for running periodic ETL jobs
│   ├── utils.py                    # Utility functions for API and ETL operations
├── etl/                            # ETL (Extract, Transform, Load) pipeline logic
│   ├── __init__.py                 # Empty file to mark this directory as a Python package
│   ├── etl_job.py                  # Implementation of the ETL pipeline (fetching and updating stories)
├── main.py                         # Entry point for the FastAPI application
├── Dockerfile                      # Dockerfile for containerizing the application
├── docker-compose.yaml             # Docker Compose configuration for multi-container setup
├── requirements.txt                # List of Python dependencies for the project
├── .env                            # Environment variables for configuration (e.g., database credentials, API URLs)
├── .dockerignore                   # Files and directories to exclude from Docker builds

## Installation

### Prerequisites

- Python 3.9+
- Docker and Docker Compose

### Steps

1\. Clone the repository:

``` bash
git clone <repository-url>
cd blackkite_case
```

2\. Create a .env file with the following content (update values as needed):

```bash
DB_HOST=postgres
DB_PORT=5432
DB_NAME=hackernews
DB_USER=hacker
DB_PASSWORD=news
API_KEY=supersecret
TOP_STORIES_URL=https://hacker-news.firebaseio.com/v0/topstories.json
ITEM_URL=https://hacker-news.firebaseio.com/v0/item/{}.json

```

3\. Build and start the services using Docker Compose:

```
docker-compose up --build
```
Note: This will automatically starts scheduled ETL job as well.

4\. Access the API via Swagger UI at http://localhost:8000.

5\. (Optional) Access pgAdmin at http://localhost:80 (default credentials: admin@admin.com / admin).

API Endpoints
-------------

### Stories

-   **GET** `/stories`\
    Fetch a paginated list of stories with optional filters.
    #### Available Query Parameters:
    **page** (int, default: 1): The page number to retrieve (must be greater than or equal to 1).

    **limit** (int, default: 20): The number of stories per page (must be between 0 and 20).
    
    **author** (str, optional): Filter stories by the author's name (case-insensitive, partial match allowed).

    **min_score** (int, optional): Filter stories with a minimum score.
    
    **search** (str, optional): Search for stories by title (case-insensitive, partial match allowed).

-   **GET** `/stories/{story_id}`\
    Retrieve details of a specific story by ID.

-   **GET** `/stats/top-authors`\
    Get the top 5 authors based on their total story scores.

### Authentication

All endpoints require an API key to be passed in the `api-key` header.

### Rate Limiting

The API enforces a rate limit of 10 requests per minute per client.

### Testing

-   Use tools like Postman, Swagger UI or cURL to test the API endpoints.
-   Ensure the `.env` file is properly configured for local testing.

Deployment
----------

The application is containerized using Docker. Use the provided `docker-compose.yaml` file to deploy the application along with its dependencies (PostgreSQL and pgAdmin).
