class KubernetesError(Exception):
    """Base exception for Kubernetes operations"""
    pass

class PodNotFoundError(KubernetesError):
    """Raised when pod is not found"""
    pass

class ScalingError(KubernetesError):
    """Raised when scaling operation fails"""
    pass

class AuthenticationError(KubernetesError):
    """Raised when authentication fails"""
    pass

class ConfigurationError(KubernetesError):
    """Raised when configuration is invalid"""
    pass