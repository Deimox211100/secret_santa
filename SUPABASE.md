# Migración a Supabase

## 🎯 Objetivo

Migrar la base de datos de PostgreSQL local (Docker) a Supabase para simplificar el deployment y obtener una base de datos en la nube.

## 📋 Pasos de Configuración

### 1. Crear Proyecto en Supabase

1. Ve a [supabase.com](https://supabase.com)
2. Crea una cuenta o inicia sesión
3. Crea un nuevo proyecto
4. Guarda las credenciales que te proporciona:
   - **Project URL**: `https://your-project.supabase.co`
   - **Anon/Public Key**: Para autenticación (no lo necesitamos ahora)
   - **Service Role Key**: Para acceso completo desde el backend
   - **Database Password**: La contraseña que elegiste

### 2. Configurar la Base de Datos

1. En tu proyecto de Supabase, ve a **SQL Editor**
2. Copia y pega el contenido de `utils/supabase_setup.sql`
3. Ejecuta el script (botón "Run")
4. Verifica que las tablas se crearon correctamente en **Table Editor**

### 3. Obtener Credenciales de Conexión

En Supabase, ve a **Project Settings** > **Database**:

**Opción A: Connection String (Recomendado)**
```
postgresql://postgres:[YOUR-PASSWORD]@db.your-project.supabase.co:5432/postgres
```

**Opción B: Credenciales Individuales**
- Host: `db.your-project.supabase.co`
- Database: `postgres`
- Port: `5432`
- User: `postgres`
- Password: `[tu contraseña]`

### 4. Configurar Variables de Entorno

Crea un archivo `.env` basado en `.env.example`:

```bash
cp .env.example .env
```

Edita `.env` y agrega tus credenciales de Supabase.

### 5. ⚠️ IMPORTANTE: Exponer el Schema en la API

Por defecto, Supabase solo expone el schema `public`. Como usamos el schema `secret-santa`, debes configurarlo manualmente:

1. Ve a **Settings** (engranaje) > **API** en tu dashboard de Supabase.
2. En la sección **API Settings** (PostgREST Config).
3. Busca el campo **Exposed schemas**.
4. Agrega `secret-santa` a la lista (ej. `public, secret-santa`).
5. Guarda los cambios.

> Si no haces esto, recibirás el error: `The schema must be one of the following: public, graphql_public`.

### 6. Actualizar Variables de Entorno

Edita tu archivo `.env`:

```bash
# Supabase Database Connection
DB_HOST=db.your-project.supabase.co
DB_USER=postgres
DB_PASSWORD=tu_password_de_supabase
DB_NAME=postgres
DB_PORT=5432

# Admin Password
ADMIN_PWD=tu_contraseña_admin

# App Port
APP_PORT=8501
```

### 5. Actualizar Admin Password

**IMPORTANTE**: Cambia la contraseña del admin en Supabase:

```sql
UPDATE "secret-santa".admin 
SET password = 'tu_contraseña_segura' 
WHERE username = 'gota';
```

### 6. Desplegar la Aplicación

```bash
# Reconstruir sin la base de datos local
docker-compose down -v
docker-compose up -d --build

# Verificar logs
docker-compose logs -f app
```

## ✅ Verificación

1. **Conexión a la Base de Datos**:
   ```bash
   docker-compose exec app python3 -c "import psycopg2; print('Conexión exitosa!')"
   ```

2. **Acceder a la Aplicación**:
   - Abre http://localhost:8501
   - Intenta registrarte
   - Verifica en Supabase Table Editor que el usuario se creó

3. **Login como Admin**:
   - Usuario: `gota`
   - Contraseña: la que configuraste en el paso 5

## 🔒 Seguridad

### Row Level Security (RLS)

El script de setup habilita RLS y crea políticas que permiten acceso completo usando el service role. Esto es seguro porque:

1. La aplicación usa conexión directa a PostgreSQL (no usa las APIs de Supabase)
2. Las credenciales están en variables de entorno
3. Solo el contenedor de la app tiene acceso

### Mejores Prácticas

1. **Nunca** compartas tu `DB_PASSWORD` o `ADMIN_PWD`
2. Usa contraseñas fuertes (mínimo 16 caracteres)
3. Cambia la contraseña del admin después del primer deploy
4. Considera usar Supabase Vault para secretos sensibles

## 📊 Ventajas de Supabase

✅ **Sin mantenimiento de infraestructura**
- No necesitas gestionar PostgreSQL
- Backups automáticos
- Escalado automático

✅ **Herramientas incluidas**
- Table Editor visual
- SQL Editor con autocompletado
- Logs y métricas en tiempo real

✅ **Gratis para empezar**
- 500 MB de base de datos
- 1 GB de almacenamiento
- 2 GB de ancho de banda

## 🔄 Rollback (Volver a PostgreSQL Local)

Si necesitas volver a PostgreSQL local:

1. Restaura el `docker-compose.yml` original (con servicio `db`)
2. Restaura el `.env` con variables locales
3. Ejecuta: `docker-compose up -d`

## 📝 Notas

- **Schema**: Usamos `"secret-santa"` como schema para organizar las tablas
- **Conexión**: La app se conecta directamente a PostgreSQL (puerto 5432)
- **No usamos**: Supabase Auth, Storage, o Realtime (solo la base de datos)

## 🆘 Troubleshooting

### Error: "could not connect to server"
- Verifica que el host sea correcto: `db.your-project.supabase.co`
- Verifica que el puerto sea `5432`
- Verifica que la contraseña sea correcta

### Error: "schema does not exist"
- Ejecuta el script `supabase_setup.sql` en el SQL Editor de Supabase

### Error: "permission denied"
- Verifica que estés usando el usuario `postgres`
- Verifica que las políticas RLS estén configuradas

---

**¡Listo!** Tu aplicación ahora usa Supabase como base de datos. 🎉
