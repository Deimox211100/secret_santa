-- Migration script to update existing database from stations to characters
-- Run this script if you have existing data in your database

-- Step 1: Add the new character_photo_url column
ALTER TABLE "secret-santa".users 
ADD COLUMN IF NOT EXISTS character_photo_url TEXT;

-- Step 2: Rename the estacion column to character_name
ALTER TABLE "secret-santa".users 
RENAME COLUMN estacion TO character_name;

-- Step 3: Increase the size of character_name column to accommodate longer names
ALTER TABLE "secret-santa".users 
ALTER COLUMN character_name TYPE VARCHAR(100);

COMMIT;
