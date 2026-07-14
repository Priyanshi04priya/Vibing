from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "VibeTrip AI"
    environment: str = "development"
    debug: bool = True
    weather_api_key: str | None = None
    maps_api_key: str | None = None
    model_name: str = "gemini-2.5-flash"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
