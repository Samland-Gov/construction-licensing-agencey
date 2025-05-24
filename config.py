import os


class Config(object):
    FEEDBACK_URL = "https://github.com/orgs/Samland-Gov/discussions/2"
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SERVICE_NAME = "Construction Licencing Agency"
    SERVICE_PHASE = "Alpha"
    SERVICE_URL = os.environ.get("SERVICE_URL") or "/"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = True