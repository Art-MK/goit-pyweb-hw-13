import cloudinary
import cloudinary.uploader
import cloudinary.api
from src.config import settings

# Configure Cloudinary with the provided credentials
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

def upload_avatar(file):
    result = cloudinary.uploader.upload(file, folder="avatars")
    return result['secure_url']
