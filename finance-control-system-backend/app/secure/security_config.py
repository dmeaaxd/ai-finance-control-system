from fastapi.security import APIKeyHeader

apikey_scheme = APIKeyHeader(name="Authorization")
