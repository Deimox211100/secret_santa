-- Add comentarios_generales column to users table
ALTER TABLE "secret-santa".users 
ADD COLUMN IF NOT EXISTS "comentarios_generales" TEXT;
