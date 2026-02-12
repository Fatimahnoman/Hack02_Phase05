# Running with Docker

## Prerequisites

- Docker Desktop installed
- Docker Compose plugin enabled

## Quick Start

To run the entire application stack with Docker Compose:

```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Copy environment files and update values as needed
cp backend/.env backend/.env.local
# Edit backend/.env.local with your actual values

# Build and start the services
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend API Documentation: http://localhost:8000/docs

## Development Mode

For development with live reloading:

```bash
# Build and start services in development mode
docker-compose -f docker-compose.dev.yml up --build
```

This will mount your source code into the containers, allowing for real-time updates without rebuilding.

## Environment Variables

Make sure to set up your environment variables in the `.env` files:

- `backend/.env` or `backend/.env.local` for backend configuration
- `frontend/.env.local` for frontend configuration

## Stopping Services

To stop the running services:

```bash
docker-compose down
```

To stop and remove containers, networks, and volumes:

```bash
docker-compose down -v
```

## Troubleshooting

1. If you get connection errors, make sure both frontend and backend services are running
2. Check that the `NEXT_PUBLIC_API_URL` in frontend points to the correct backend address
3. Make sure your environment variables are properly set in the .env files