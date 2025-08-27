import hashlib
import re
import json
from typing import Dict, Any, List, Union

def mask_email(email: str) -> str:
    """
    Mask email addresses by hashing the local part (before @).
    
    Args:
        email: The email address to mask
        
    Returns:
        Masked email address with hashed local part
    """
    if not email or '@' not in email:
        return email
        
    local_part, domain = email.split('@', 1)
    hashed_local = hashlib.md5(local_part.encode()).hexdigest()
    
    return f"{hashed_local}@{domain}"

def mask_full_name(name: str) -> str:
    """
    Mask full names by creating anonymous hash-based identifier.
    
    Args:
        name: The full name to mask
        
    Returns:
        Anonymous hash-based identifier
    """
    if not name:
        return name
    hash_name = hashlib.sha256(name.encode()).hexdigest()
    return f"User_{hash_name[:8]}"

def mask_username(username: str) -> str:
    """
    Mask usernames by creating anonymous hash-based identifier.
    
    Args:
        username: The username to mask
        
    Returns:
        Anonymous hash-based identifier
    """
    if not username:
        return username
    hash_user = hashlib.sha256(username.encode()).hexdigest()
    return f"user_{hash_user[:8]}"

def mask_wallet_address(wallet: str) -> str:
    """
    Partially mask wallet address showing only first 6 and last 4 characters.
    
    Args:
        wallet: The wallet address to mask
        
    Returns:
        Partially masked wallet address
    """
    if not wallet or len(wallet) < 10:
        return wallet
    return f"{wallet[:6]}...{wallet[-4:]}"

def mask_birth_date(birth_date: str) -> str:
    """
    Mask birth date by hiding the day part.
    
    Args:
        birth_date: The birth date to mask (YYYY-MM-DD format)
        
    Returns:
        Masked birth date with day replaced by XX
    """
    if not birth_date or '-' not in birth_date:
        return birth_date
    try:
        year, month, day = birth_date.split('-')
        return f"{year}-{month}-XX"  # Hide day part
    except:
        return "XXXX-XX-XX"

def generate_anonymous_id(original_value: str) -> str:
    """
    Generate completely anonymous ID from original value.
    
    Args:
        original_value: The original value to anonymize
        
    Returns:
        Anonymous identifier
    """
    hash_val = hashlib.sha256(original_value.encode()).hexdigest()
    return f"anon_{hash_val[:12]}"

PII_SENSITIVE_KEYS = {
    'username', 'user', 'name', 'full_name', 'display_name', 'first_name', 'last_name',
    'message', 'text', 'content', 'caption', 'comment', 'description', 'bio',
    'location', 'address', 'city', 'country', 'place', 'geo', 'coordinates',
    'query', 'search', 'search_term', 'keyword',
    'email', 'mail', 'phone', 'mobile', 'tel', 'telephone',
    'ip', 'ip_address', 'device_id', 'user_id', 'profile_id'
}

SAFE_KEYS = {
    'count', 'timestamp', 'date', 'time', 'created_at', 'updated_at',
    'likes_count', 'comments_count', 'views', 'followers_count', 'following_count',
    'duration', 'size', 'width', 'height', 'type', 'format', 'status',
    'is_', 'has_', 'can_', 'should_', 'enabled', 'disabled', 'public', 'private'
}

def is_sensitive_key(key: str) -> bool:
    """
    Check if a key contains sensitive information.
    
    Args:
        key: The key name to check
        
    Returns:
        True if key is potentially sensitive
    """
    key_lower = key.lower()
    
    # Tam eşleşme kontrol et
    if key_lower in PII_SENSITIVE_KEYS:
        return True
    
    # Güvenli anahtarları kontrol et
    if any(safe_key in key_lower for safe_key in SAFE_KEYS):
        return False
        
    # Kısmi eşleşme kontrol et
    return any(sensitive in key_lower for sensitive in PII_SENSITIVE_KEYS)

def mask_text_content(text: str) -> str:
    """
    Mask text content by removing/masking potentially sensitive parts.
    
    Args:
        text: The text content to mask
        
    Returns:
        Masked text content
    """
    if not isinstance(text, str) or not text:
        return text
    
    # Email maskele
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL_MASKED]', text)
    
    # Telefon numarası maskele  
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE_MASKED]', text)
    text = re.sub(r'\+\d{1,3}[-.\s]?\d{3,4}[-.\s]?\d{3,4}[-.\s]?\d{3,4}', '[PHONE_MASKED]', text)
    
    # URL'leri maskele
    text = re.sub(r'https?://[^\s]+', '[URL_MASKED]', text)
    
    # Eğer çok kısa ise (3 kelimeden az) tamamen maskele
    if len(text.split()) < 3:
        return mask_username(text)
    
    return text

def clean_raw_export_data(raw_data: Dict[str, Any], max_depth: int = 10) -> Dict[str, Any]:
    """
    Clean raw export data by removing or masking PII.
    
    Args:
        raw_data: The raw export data dictionary
        max_depth: Maximum recursion depth to prevent infinite loops
        
    Returns:
        Cleaned data dictionary
    """
    if max_depth <= 0:
        return {"_masked": "max_depth_reached"}
    
    if not isinstance(raw_data, dict):
        return raw_data
    
    cleaned_data = {}
    
    for key, value in raw_data.items():
        is_sensitive = is_sensitive_key(key)
        
        if isinstance(value, dict):
            # Nested dictionary - recursive clean
            cleaned_data[key] = clean_raw_export_data(value, max_depth - 1)
            
        elif isinstance(value, list):
            # List - clean each item
            cleaned_list = []
            for item in value:
                if isinstance(item, dict):
                    cleaned_list.append(clean_raw_export_data(item, max_depth - 1))
                elif isinstance(item, str) and is_sensitive:
                    cleaned_list.append(mask_text_content(item))
                else:
                    cleaned_list.append(item)
            cleaned_data[key] = cleaned_list
            
        elif isinstance(value, str):
            if is_sensitive:
                # Sensitive string - mask it
                if any(sens_key in key.lower() for sens_key in ['username', 'user', 'name']):
                    cleaned_data[key] = mask_username(value)
                elif any(msg_key in key.lower() for msg_key in ['message', 'text', 'caption', 'comment']):
                    cleaned_data[key] = mask_text_content(value)
                elif 'email' in key.lower():
                    cleaned_data[key] = mask_email(value)
                else:
                    cleaned_data[key] = mask_text_content(value)
            else:
                # Safe string - keep as is
                cleaned_data[key] = value
                
        else:
            # Numbers, booleans, etc. - keep as is
            cleaned_data[key] = value
    
    return cleaned_data

def process_raw_export_safely(raw_export_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function to safely process raw export data.
    
    Args:
        raw_export_data: Raw export data from unrefined model
        
    Returns:
        Safely processed data ready for storage
    """
    if not raw_export_data:
        return {}
    
    try:
        # Ana temizleme işlemi
        cleaned_data = clean_raw_export_data(raw_export_data)
        
        # Boyut kontrolü - çok büyükse summary'e dönüştür
        data_str = json.dumps(cleaned_data, ensure_ascii=False)
        if len(data_str) > 50000:  # 50KB limitli
            return {
                "_summary": "Large data cleaned and summarized",
                "_original_size": len(data_str),
                "_keys_count": len(cleaned_data),
                "_sample_keys": list(cleaned_data.keys())[:10]
            }
        
        return cleaned_data
        
    except Exception as e:
        # Hata durumunda güvenli fallback
        return {
            "_error": "Failed to process raw data safely",
            "_error_type": str(type(e).__name__),
            "_fallback": True
        } 