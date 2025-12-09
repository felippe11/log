from django.core import signing
from drivers.models import Driver

PORTAL_TOKEN_AGE_SECONDS = 60 * 60 * 24 * 7  # 7 days
PORTAL_SALT = "driver-portal"


def generate_portal_token(driver: Driver) -> str:
    signer = signing.TimestampSigner(salt=PORTAL_SALT)
    return signer.sign(driver.id)


def resolve_portal_token(token: str) -> Driver:
    signer = signing.TimestampSigner(salt=PORTAL_SALT)
    driver_id = signer.unsign(token, max_age=PORTAL_TOKEN_AGE_SECONDS)
    return Driver.objects.select_related("municipality").get(id=driver_id, status=Driver.Status.ACTIVE)
