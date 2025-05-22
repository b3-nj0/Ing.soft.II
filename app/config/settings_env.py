from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ValidationError

class Settings(BaseSettings):
    DATABASE_URL: str 
    SECRET_KEY: str  
    ALGORITHM: str = "HS256"  
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ENV: str = "development"
    FRONTEND_ORIGINS: str 
    ASSET_URL: str

    model_config = SettingsConfigDict(env_file=".env")  
    
    #  esto se si la version de pydantic se kga 
    # class Config: 
    #     env_file = ".env"

try:


    settings_objeto = Settings()


except ValidationError as e:
    print("Error en configuracin del entorno:")
    print(e)
    raise e  # detiene la ejecución si hay error