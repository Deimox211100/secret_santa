"""
Supabase database connection utility
Provides a singleton Supabase client for the application
"""
import os
from supabase import create_client, Client, ClientOptions
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Create Supabase client
_supabase_client: Client = None

def get_supabase_client() -> Client:
    """
    Get or create Supabase client singleton
    Returns:
        Client: Supabase client instance
    """
    global _supabase_client
    
    if _supabase_client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_KEY must be set in environment variables"
            )
        
        # Configure client to use 'secret-santa' schema
        options = ClientOptions(schema="secret-santa")
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY, options=options)
    
    return _supabase_client
