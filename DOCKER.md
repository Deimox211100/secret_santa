# Secret Santa - Docker Setup

## Quick Start

### Prerequisites
- Docker Desktop installed
- Docker Compose installed

### 1. Setup Environment

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` if you want to change default values (optional):
```bash
# Database Configuration
DB_USER=postgres
DB_PASSWORD=postgres  # Change this!
DB_NAME=secret_santa
DB_PORT=5432

# Application Configuration
APP_PORT=8501
```

### 2. Start the Application

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# View app logs only
docker-compose logs -f app
```

### 3. Access the Application

Open your browser and navigate to:
```
http://localhost:8501
```

### 4. Stop the Application

```bash
# Stop services
docker-compose down

# Stop and remove volumes (WARNING: deletes database data)
docker-compose down -v
```

## Docker Commands Reference

### Build & Start
```bash
# Build images
docker-compose build

# Start services in background
docker-compose up -d

# Start services with logs
docker-compose up

# Rebuild and start
docker-compose up -d --build
```

### Monitoring
```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f app
docker-compose logs -f db
```

### Database Management
```bash
# Access PostgreSQL shell
docker-compose exec db psql -U postgres -d secret_santa

# Run SQL file
docker-compose exec db psql -U postgres -d secret_santa -f /docker-entrypoint-initdb.d/02-setup.sql

# Backup database
docker-compose exec db pg_dump -U postgres secret_santa > backup.sql

# Restore database
cat backup.sql | docker-compose exec -T db psql -U postgres secret_santa
```

### Cleanup
```bash
# Stop services
docker-compose down

# Remove volumes (deletes data)
docker-compose down -v

# Remove images
docker-compose down --rmi all

# Full cleanup
docker-compose down -v --rmi all --remove-orphans
```

## Service Details

### PostgreSQL Database
- **Container**: `secret-santa-db`
- **Image**: `postgres:15-alpine`
- **Port**: `5432` (configurable via `DB_PORT`)
- **Volume**: `postgres_data` (persistent storage)
- **Health Check**: Automatic readiness check

### Streamlit Application
- **Container**: `secret-santa-app`
- **Port**: `8501` (configurable via `APP_PORT`)
- **Auto-restart**: Yes
- **Depends on**: Database (waits for DB to be healthy)

## Troubleshooting

### Database Connection Issues
```bash
# Check if database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

### Application Issues
```bash
# Check app logs
docker-compose logs app

# Restart app
docker-compose restart app

# Rebuild app
docker-compose up -d --build app
```

### Port Already in Use
If port 8501 or 5432 is already in use, edit `.env`:
```bash
APP_PORT=8502
DB_PORT=5433
```

Then restart:
```bash
docker-compose down
docker-compose up -d
```

### Reset Everything
```bash
# Stop and remove everything
docker-compose down -v

# Start fresh
docker-compose up -d
```

## Development Mode

To develop with live code reloading, mount the source code:

```yaml
# Add to docker-compose.yml under app service:
volumes:
  - .:/app
  - ./config.json:/app/config.json
```

Then restart:
```bash
docker-compose down
docker-compose up -d
```

## Production Deployment

For production, consider:

1. **Change default passwords** in `.env`
2. **Use secrets management** instead of `.env` file
3. **Enable SSL/TLS** for the database
4. **Set up backups** for the database volume
5. **Use a reverse proxy** (nginx) for HTTPS
6. **Monitor logs** and set up alerts

## Network

All services run on the `secret-santa-network` bridge network, allowing them to communicate using service names (e.g., `db`, `app`).
