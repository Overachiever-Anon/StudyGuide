"""
Supabase storage service for EduForge
"""

import os
import time
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class SupabaseStorage:
    """Handles file storage operations with Supabase"""
    
    def __init__(self):
        """Initialize Supabase client"""
        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_key = os.environ.get("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("Supabase URL and key must be set in .env file")
            
        self.supabase: Client = create_client(supabase_url, supabase_key)
        self.bucket_name = os.environ.get("SUPABASE_BUCKET_NAME", "eduforge-pdfs")
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """Ensure the storage bucket exists"""
        try:
            # Try to get bucket info - if it doesn't exist, this will raise an exception
            self.supabase.storage.get_bucket(self.bucket_name)
        except:
            # Create the bucket if it doesn't exist
            self.supabase.storage.create_bucket(self.bucket_name, public=False)
    
    def upload_file(self, file_content, file_name, user_id):
        """
        Upload a file to Supabase Storage
        
        Args:
            file_content: The binary content of the file
            file_name: Name of the file
            user_id: User ID for folder organization
            
        Returns:
            file_path: The path to the file in Supabase Storage
        """
        # Create a unique path for the file
        timestamp = int(time.time())
        safe_filename = Path(file_name).stem.replace(" ", "_")
        file_path = f"{user_id}/{safe_filename}_{timestamp}.pdf"
        
        # Upload file to Supabase storage
        self.supabase.storage.from_(self.bucket_name).upload(
            file_path,
            file_content
        )
        
        return file_path
    
    def download_file(self, file_path, local_path=None):
        """
        Download a file from Supabase Storage
        
        Args:
            file_path: Path to the file in storage
            local_path: Optional local path to save file
            
        Returns:
            bytes: File content if local_path is None, else None
        """
        # Get file from storage
        file_content = self.supabase.storage.from_(self.bucket_name).download(file_path)
        
        # Save to local path if provided
        if local_path:
            with open(local_path, 'wb') as f:
                f.write(file_content)
            return None
            
        return file_content
    
    def get_file_url(self, file_path, expires_in=3600):
        """
        Get a signed URL for a file
        
        Args:
            file_path: Path to the file in storage
            expires_in: Expiration time in seconds
            
        Returns:
            str: Signed URL
        """
        return self.supabase.storage.from_(self.bucket_name).create_signed_url(
            file_path, 
            expires_in
        )
    
    def delete_file(self, file_path):
        """
        Delete a file from storage
        
        Args:
            file_path: Path to the file in storage
            
        Returns:
            bool: Success status
        """
        try:
            self.supabase.storage.from_(self.bucket_name).remove(file_path)
            return True
        except Exception:
            return False
