"""
Storage Service for Supabase Storage
"""
from app.services.supabase import get_supabase_admin_client
from werkzeug.utils import secure_filename
from PIL import Image
import io
import os
import uuid


class StorageService:
    """Handle file uploads to Supabase Storage"""
    
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
    MAX_SIZE = 5 * 1024 * 1024  # 5MB
    
    @staticmethod
    def allowed_file(filename: str) -> bool:
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in StorageService.ALLOWED_EXTENSIONS
    
    @staticmethod
    def optimize_image(file_data: bytes, max_width: int = 1200, quality: int = 85) -> bytes:
        """Optimize image size and quality"""
        try:
            image = Image.open(io.BytesIO(file_data))
            
            # Convert RGBA to RGB if necessary
            if image.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            
            # Resize if too large
            if image.width > max_width:
                ratio = max_width / image.width
                new_height = int(image.height * ratio)
                image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
            # Save optimized
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=quality, optimize=True)
            return output.getvalue()
        
        except Exception as e:
            print(f"Error optimizing image: {e}")
            return file_data
    
    @staticmethod
    def upload_product_image(file, product_id: str, optimize: bool = True) -> dict:
        """Upload product image to Supabase Storage"""
        try:
            if not file or not StorageService.allowed_file(file.filename):
                return {'success': False, 'error': 'Invalid file type'}
            
            # Read file data
            file_data = file.read()
            
            if len(file_data) > StorageService.MAX_SIZE:
                return {'success': False, 'error': 'File too large (max 5MB)'}
            
            # Optimize image
            if optimize:
                file_data = StorageService.optimize_image(file_data)
            
            # Generate unique filename
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{product_id}/{uuid.uuid4()}.{ext}"
            
            # Upload to Supabase Storage
            supabase = get_supabase_admin_client()
            response = supabase.storage.from_('products').upload(
                filename,
                file_data,
                {'content-type': f'image/{ext}'}
            )
            
            # Get public URL
            public_url = supabase.storage.from_('products').get_public_url(filename)
            
            return {
                'success': True,
                'path': filename,
                'url': public_url
            }
        
        except Exception as e:
            print(f"Error uploading image: {e}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def delete_file(bucket: str, path: str) -> dict:
        """Delete file from Supabase Storage"""
        try:
            supabase = get_supabase_admin_client()
            supabase.storage.from_(bucket).remove([path])
            return {'success': True}
        
        except Exception as e:
            print(f"Error deleting file: {e}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def upload_banner(file) -> dict:
        """Upload banner image"""
        try:
            if not file or not StorageService.allowed_file(file.filename):
                return {'success': False, 'error': 'Invalid file type'}
            
            file_data = file.read()
            
            if len(file_data) > 10 * 1024 * 1024:  # 10MB for banners
                return {'success': False, 'error': 'File too large (max 10MB)'}
            
            # Optimize
            file_data = StorageService.optimize_image(file_data, max_width=1920, quality=90)
            
            # Generate filename
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"banners/{uuid.uuid4()}.{ext}"
            
            # Upload
            supabase = get_supabase_admin_client()
            response = supabase.storage.from_('banners').upload(
                filename,
                file_data,
                {'content-type': f'image/{ext}'}
            )
            
            public_url = supabase.storage.from_('banners').get_public_url(filename)
            
            return {
                'success': True,
                'path': filename,
                'url': public_url
            }
        
        except Exception as e:
            print(f"Error uploading banner: {e}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def upload_avatar(file, user_id: str) -> dict:
        """Upload user avatar"""
        try:
            if not file or not StorageService.allowed_file(file.filename):
                return {'success': False, 'error': 'Invalid file type'}
            
            file_data = file.read()
            
            if len(file_data) > 2 * 1024 * 1024:  # 2MB for avatars
                return {'success': False, 'error': 'File too large (max 2MB)'}
            
            # Optimize and resize to square
            try:
                image = Image.open(io.BytesIO(file_data))
                
                # Convert to RGB
                if image.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', image.size, (255, 255, 255))
                    background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                    image = background
                
                # Crop to square
                width, height = image.size
                size = min(width, height)
                left = (width - size) // 2
                top = (height - size) // 2
                image = image.crop((left, top, left + size, top + size))
                
                # Resize to 400x400
                image = image.resize((400, 400), Image.Resampling.LANCZOS)
                
                # Save
                output = io.BytesIO()
                image.save(output, format='JPEG', quality=90, optimize=True)
                file_data = output.getvalue()
            
            except Exception as e:
                print(f"Error processing avatar: {e}")
            
            # Generate filename
            filename = f"{user_id}/avatar.jpg"
            
            # Upload
            supabase = get_supabase_admin_client()
            
            # Delete old avatar if exists
            try:
                supabase.storage.from_('avatars').remove([filename])
            except:
                pass
            
            response = supabase.storage.from_('avatars').upload(
                filename,
                file_data,
                {'content-type': 'image/jpeg'}
            )
            
            public_url = supabase.storage.from_('avatars').get_public_url(filename)
            
            return {
                'success': True,
                'path': filename,
                'url': public_url
            }
        
        except Exception as e:
            print(f"Error uploading avatar: {e}")
            return {'success': False, 'error': str(e)}
