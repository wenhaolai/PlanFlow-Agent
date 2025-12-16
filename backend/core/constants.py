"""
系统常量定义
集中管理所有魔法数字和字符串常量
"""

# ===================================
# Token相关常量
# ===================================
DEFAULT_TOKEN_EXPIRE_MINUTES = 30
MAX_TOKEN_EXPIRE_MINUTES = 1440  # 24小时
PASSWORD_RESET_TOKEN_EXPIRE_MINUTES = 30  # 密码重置令牌30分钟有效

# ===================================
# 分页相关常量
# ===================================
DEFAULT_PAGE_SIZE = 100
MAX_PAGE_SIZE = 1000
MIN_PAGE_SIZE = 1

# ===================================
# 密码相关常量
# ===================================
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 100
PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]'

# ===================================
# 用户相关常量
# ===================================
MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 50
USERNAME_REGEX = r'^[a-zA-Z0-9_-]+$'
FORBIDDEN_USERNAMES = ['admin', 'root', 'system', 'administrator', 'superuser', 'test']


# ===================================
# 日志级别常量
# ===================================
class LogLevel:
    """日志级别"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# ===================================
# HTTP状态码常量
# ===================================
class HTTPStatus:
    """常用HTTP状态码"""
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    INTERNAL_SERVER_ERROR = 500


# ===================================
# 数据库相关常量
# ===================================
DB_CONNECTION_POOL_SIZE = 20
DB_MAX_OVERFLOW = 10
DB_POOL_TIMEOUT = 30
DB_POOL_RECYCLE = 3600  # 1小时


# ===================================
# 错误消息常量
# ===================================
class ErrorMessages:
    """错误消息模板"""
    # 认证相关
    INVALID_CREDENTIALS = "邮箱或密码错误"
    ACCOUNT_DISABLED = "账户已被禁用"
    TOKEN_EXPIRED = "登录已过期，请重新登录"
    INVALID_TOKEN = "无效的认证凭据"

    # 用户相关
    USER_NOT_FOUND = "用户不存在"
    EMAIL_EXISTS = "该邮箱已注册"
    USERNAME_EXISTS = "该用户名已存在"
    WEAK_PASSWORD = "密码强度不足"

    # 通用错误
    INVALID_INPUT = "输入数据无效"
    OPERATION_FAILED = "操作失败"
    PERMISSION_DENIED = "权限不足"
    RESOURCE_NOT_FOUND = "资源不存在"


# ===================================
# 成功消息常量
# ===================================
class SuccessMessages:
    """成功消息模板"""
    LOGIN_SUCCESS = "登录成功"
    REGISTER_SUCCESS = "注册成功"
    PASSWORD_RESET_SUCCESS = "密码重置成功"
    UPDATE_SUCCESS = "更新成功"
    DELETE_SUCCESS = "删除成功"
    CREATE_SUCCESS = "创建成功"
    OPERATION_SUCCESS = "操作成功"
