from pydantic_settings import BaseSettings
from pydantic import field_validator, model_validator, Field
from typing import Optional
import secrets
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # 数据库配置（使用 validation_alias 兼容 Docker 环境变量）
    db_host: str = Field(validation_alias="MYSQL_HOST")
    db_port: int = Field(default=3306, validation_alias="MYSQL_PORT")
    db_user: str = Field(validation_alias="MYSQL_USER")
    db_password: str = Field(validation_alias="MYSQL_PASSWORD")
    db_name: str = Field(validation_alias="MYSQL_DATABASE")
    
    # 数据库连接URL（自动构建，无需手动配置）
    database_url: Optional[str] = None
    
    # 服务器配置
    server_base_url: str = "http://localhost:8000"  # 服务器基础URL，用于生成固件下载链接等
    firmware_base_url: Optional[str] = None  # 固件下载基础URL（可选，默认使用server_base_url）
    
    # JWT配置（必须从环境变量读取）
    secret_key: str = Field(validation_alias="SECURITY_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = Field(
        default=15,
        validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES",
        description="access token有效期（分钟）"
    )
    refresh_token_expire_minutes: int = Field(
        default=45,
        validation_alias="REFRESH_TOKEN_EXPIRE_MINUTES",
        description="refresh token有效期（分钟）"
    )

    # LLM API Key
    dashscope_api_key: Optional[str] = Field(default=None, validation_alias="DASHSCOPE_API_KEY")

    # 环境配置
    environment: str = "development"  # development, production, testing
    
    # 日志级别配置
    log_level: str = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # 忽略额外的环境变量，避免部署时出错
    
    @model_validator(mode='after')
    def build_database_url(self):
        """从独立配置项构建数据库URL"""
        self.database_url = f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        return self
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._validate_security_settings()
    
    def _validate_security_settings(self):
        """验证安全配置"""
        # 验证JWT密钥强度
        if len(self.secret_key) < 32:
            logger.error("SECRET_KEY必须至少32个字符！")
            raise ValueError("SECRET_KEY必须至少32个字符以确保安全性")
        
        # 生产环境必须使用强密钥
        if self.environment == "production":
            if "your-secret-key" in self.secret_key.lower() or "change" in self.secret_key.lower():
                raise ValueError("生产环境禁止使用默认密钥！")
        
        # 输出Token配置信息（用于调试）
        logger.info(f"🔑 Token有效期 - Access: {self.access_token_expire_minutes}分钟, Refresh: {self.refresh_token_expire_minutes}分钟")
        
        logger.info("✅ 安全配置验证通过")
    
    @property
    def get_firmware_base_url(self) -> str:
        """获取固件下载基础URL"""
        return self.firmware_base_url or self.server_base_url

# 创建全局settings实例
try:
    settings = Settings()
except Exception as e:
    logger.error(f"❌ 配置加载失败: {e}")
    logger.info("💡 提示：请确保 .env 文件已正确配置所有必需的环境变量")
    logger.info("💡 参考 env.example 文件创建 .env")
    raise