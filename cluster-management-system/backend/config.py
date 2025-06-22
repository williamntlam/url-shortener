from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Application settings
    app_name: str = "Cluster Management System"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Kubernetes settings
    k8s_strategy: str = "auto"  # auto, in_cluster, kubeconfig, kubectl
    k8s_namespace: str = "default"
    k8s_context: Optional[str] = None
    
    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api"
    
    # Retry settings
    max_retry_attempts: int = 3
    retry_delay: float = 1.0
    
    # Cache settings
    cache_ttl_seconds: int = 30
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Security
    cors_origins: list = ["*"]
    api_key_header: str = "X-API-Key"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings() 