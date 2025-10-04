from django import template
import hashlib

register = template.Library()

@register.filter
def initials(user):
    """Return initials from first and last name, or username fallback"""
    if user.first_name and user.last_name:
        return f"{user.first_name[0]}{user.last_name[0]}".upper()
    elif user.first_name:
        return user.first_name[0].upper()
    elif user.username:
        return user.username[0].upper()
    return "?"

@register.filter
def color_for_user(user):
    """
    Generate a consistent color for a user based on their username/id.
    Returns a hex color.
    """
    seed = user.username or str(user.id)

    if not seed:
        return '#6c757d' #fallback color
    
    hash_digest = hashlib.md5(seed.encode("utf-8")).hexdigest()
    # Use first 6 chars of hash as a color
    return f"#{hash_digest[:6]}"