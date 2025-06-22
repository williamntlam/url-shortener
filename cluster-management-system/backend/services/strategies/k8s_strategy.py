class KubernetesStrategy(ABC):
    """Abstract base class for Kubernetes interaction strategies"""

    @abstractmethod
    def get_pod_statuses(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod

    def scale_deployment(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_cluster_info(self) -> Dict[str, Any]:
        pass
    
class InClusterStrategy(KubernetesStrategy):  # Implementation 1
    # Implementation here...

class KubeconfigStrategy(KubernetesStrategy):  # Implementation 2
    # Implementation here...

class KubectlStrategy(KubernetesStrategy):  # Implementation 3
    # Implementation here...