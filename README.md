# Secret Santa - The Simpsons Edition 🎄

A Secret Santa web application with a parametric topic system. For 2025, the theme is **The Simpsons**!

## Features

- 🎭 **Parametric Topics** - Easily change themes each year
- 🖼️ **Character Photos** - Visual character selection and display
- 🎁 **Wish Lists** - Users can add up to 3 wishes with links
- 🔒 **Secure Login** - Password-protected character accounts
- 🎲 **Random Assignment** - Automated secret friend matching
- 🐳 **Docker Support** - Easy deployment with Docker Compose

## Quick Start with Docker + Supabase

### Prerequisites
- Docker Desktop
- Supabase account ([supabase.com](https://supabase.com))

### 1. Setup Supabase Database

1. Create a project in Supabase
2. Run the SQL script in Supabase SQL Editor:
   - Copy content from `utils/supabase_setup.sql`
   - Paste and execute in SQL Editor
3. Get your database credentials from Project Settings > Database

### 2. Configure Environment

```bash
cd secret_santa
cp .env.example .env
```

Edit `.env` with your Supabase credentials:
```bash
DB_HOST=db.your-project.supabase.co
DB_USER=postgres
DB_PASSWORD=your-supabase-password
DB_NAME=postgres
DB_PORT=5432
ADMIN_PWD=your_admin_password
```

### 3. Start the Application
```bash
docker-compose up -d
```

### 4. Access
Open your browser: **http://localhost:8501**

### 5. Stop
```bash
docker-compose down
```

For detailed Supabase setup, see [SUPABASE.md](SUPABASE.md)

## Manual Setup (Without Docker)

### Prerequisites
- Python 3.9+
- Supabase account

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Supabase
1. Create project in Supabase
2. Run `utils/supabase_setup.sql` in SQL Editor
3. Get database credentials

### 3. Configure Environment
Create a `.env` file:
```bash
DB_HOST=db.your-project.supabase.co
DB_USER=postgres
DB_PASSWORD=your-supabase-password
DB_NAME=postgres
DB_PORT=5432
ADMIN_PWD=your_admin_password
```

### 4. Run Application
```bash
streamlit run app.py
```

## Usage

### Register
1. Click "Iniciar Sesión"
2. Select your Simpsons character
3. Add your wishes (with optional links)
4. Create a password

### Login
1. Enter your character name
2. Enter your password

### View Secret Friend
1. Admin runs: `python utils/assign_friends.py`
2. Users click "Ver Amigo Secreto"
3. See your assigned friend's wishes and photo

## Changing Topics (Future Years)

### For 2026 - Example: Star Wars

1. Create `utils/starwars_characters.json`:
```json
[
  {
    "name": "Luke Skywalker",
    "photo_url": "https://..."
  }
]
```

2. Update `config.json`:
```json
{
  "year": 2026,
  "topic": "Star Wars",
  "characters_file": "starwars_characters.json"
}
```

3. Clear database or create new schema
4. Restart application - No code changes needed! 🎉

## Project Structure

```
secret_santa/
├── app.py                          # Main Streamlit app
├── config.json                     # Topic configuration
├── docker-compose.yml              # Docker setup
├── Dockerfile                      # App container
├── requirements.txt                # Python dependencies
├── pages/
│   ├── login.py                   # Login page
│   ├── register.py                # Registration page
│   ├── home.py                    # Home page
│   ├── profile.py                 # User profile
│   └── secret_friend.py           # Secret friend reveal
├── utils/
│   ├── config_loader.py           # Config utilities
│   ├── simpsons_characters.json   # 2025 characters
│   ├── assign_friends.py          # Assignment script
│   ├── init_db.sql                # DB initialization
│   └── setup.sql                  # Users table schema
└── DOCKER.md                       # Docker documentation
```

## Database Schema

### Users Table
- `id` - Primary key
- `nombre` - First name
- `apellido` - Last name
- `character_name` - Selected character (unique)
- `character_photo_url` - Character photo URL
- `deseo1`, `deseo2`, `deseo3` - Wishes
- `link_deseo1`, `link_deseo2`, `link_deseo3` - Wish links
- `password` - User password

### Secret Friends Table
- `user_id` - User ID
- `id_secret_friend` - Assigned friend ID

## Documentation

- [DOCKER.md](DOCKER.md) - Docker setup and commands
- [MIGRATION.md](MIGRATION.md) - Database migration guide

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.9
- **Database**: PostgreSQL 15
- **Deployment**: Docker + Docker Compose

## Contributing

This is a personal project for Secret Santa events. Feel free to fork and customize for your own events!

## License

MIT License - Feel free to use and modify!

---

Made with ❤️ for Secret Santa 2025 - The Simpsons Edition
