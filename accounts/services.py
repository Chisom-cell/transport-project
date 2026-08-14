# accounts/services.py
import requests
from django.conf import settings

def verify_identity_numbers(nin, abssin, first_name=None, last_name=None):
    nin_valid = bool(nin) and nin.isdigit() and len(nin) == 11
    abssin_valid = bool(abssin) and abssin.isdigit() and len(abssin) == 10

    if nin_valid and abssin_valid:
        return True, "Verification successful"
    if not nin_valid:
        return False, "Invalid NIN details"
    return False, "Invalid ABSSIN details"