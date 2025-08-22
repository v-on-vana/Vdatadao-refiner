import hashlib

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