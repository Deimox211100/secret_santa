-- Migration script to update schema for email and image uploads
-- Run this if you have existing data

-- Step 1: Rename apellido to email
ALTER TABLE "secret-santa".users 
RENAME COLUMN apellido TO email;

-- Step 2: Add image columns for wishes
ALTER TABLE "secret-santa".users 
ADD COLUMN IF NOT EXISTS imagen_deseo1 TEXT,
ADD COLUMN IF NOT EXISTS imagen_deseo2 TEXT,
ADD COLUMN IF NOT EXISTS imagen_deseo3 TEXT;

COMMIT;
