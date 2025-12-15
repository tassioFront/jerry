

def mask_email(email: str) -> str:
    local, domain = email.split('@')
    localLength = 3 if len(local) > 3 else 1
    visible = min(localLength, len(local))
    masked_local = local[:visible] + '*' * (len(local) - visible)
    display = f"{masked_local}@{domain}"
    return display