# apps/api/app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, field_validator
from typing import List, Union

class Settings(BaseSettings):
    PROJECT_NAME: str = "Autonomous B2B Sales Agent"
    API_V1_STR: str = "/api/v1"
    
    # SECURITY
    SECRET_KEY: str = "CHANGEME_IN_PRODUCTION"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    
    # SUPABASE
    SUPABASE_URL: str
    SUPABASE_KEY: str
    DATABASE_URL: str = ""
    
    # CORS
    BACKEND_CORS_ORIGINS: List[Union[str, AnyHttpUrl]] = [
        "http://localhost:5173", # Vite Dev Server
        "http://localhost:3000", # Next.js/React standard port
    ]
    
    # EXTERNAL API KEYS
    ANTHROPIC_API_KEY: str = ""

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )

settings = Settings()
