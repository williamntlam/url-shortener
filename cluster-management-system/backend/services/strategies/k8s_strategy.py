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
    def __init__(self):
        try:
            config.load_incluster_config()
            self.v1 = client.CoreV1Api()
            self.apps_v1 = client.AppsV1Api()
        except Exception as e:
            logger.error(f"Failed to initialize InClusterStrategy: {e}")
            raise

    def get_pod_statuses(self) -> List[Dict[str, Any]]:
        try:
            deployments = self.apps_v1.list_deployment_for_all_namespaces()
            pods = self.v1.list_pod_for_all_namespaces()

            pod_statuses = []

            # Process deployments
            for deployment in deployments.items:
                status = self._create_deployment_status(deployment)
                pod_statuses.append(status)

            for pod in pods.items:
                if not self._is_pod_part_of_deployment(pod, deployments.items):
                    status = self._create_pod_status(pod)
                    pod_statuses.append(status)

            return pod_statuses

        except Exception as e:
            logger.error(f"API Exception in get_pod_statuses: {e}")
            raise

    def scale_deployment(self) -> List[Dict[str, Any]]:
        try:
            pass
        except Exception as e:
            pass

    def get_cluster_info(self) -> Dict[str, Any]:
        try:
            pass
        except Exception as e:
            pass

    # Implementation here...

class KubeconfigStrategy(KubernetesStrategy):  # Implementation 2
    # Implementation here...

class KubectlStrategy(KubernetesStrategy):  # Implementation 3
    # Implementation here...