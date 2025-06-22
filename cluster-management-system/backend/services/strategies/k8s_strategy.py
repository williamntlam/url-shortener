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

    def scale_deployment(self, name: str, namespace: str, replicas: int) -> bool:
        """
        Scale a deployment to specified number of replicas
        
        Args:
            name: Name of the deployment (e.g., "frontend")
            namespace: Kubernetes namespace (e.g., "default")
            replicas: Number of pods to run (0 = stop, 1+ = start)
        
        Returns:
            bool: True if successful, False if failed
        """

        try:

            if replicas < 0:
                logger.error(f"Invalid replicas value: {replicas}. Must be >= 0")
                return False

            if not name or not namespace:
                logger.error(f"Invalid name or namespace: name={name}, namespace={namespace}")
                return False

            self.apps_v1.patch_namespaced_deployment_scale(
                name=name,
                namespace=namespace,
                body={'spec': {'replicas': replicas}}
            )

            # Log success
            action = "stopped" if replicas == 0 else f"scaled to {replicas} replicas"
            logger.info(f"Successfully {action} deployment '{name}' in namespace '{namespace}'")

            return True

        except client.ApiException as e:
            # Handle specific Kubernetes API errors
            if e.status == 404:
                logger.error(f"Deployment '{name}' not found in namespace '{namespace}'")
            elif e.status == 403:
                logger.error(f"Not authorized to scale deployment '{name}' in namespace '{namespace}'")
            elif e.status == 409:
                logger.error(f"Conflict scaling deployment '{name}'. Deployment may be updating.")
            else:
                logger.error(f"API error scaling deployment '{name}': {e}")
            return False
            
        except Exception as e:
            # Handle any other unexpected errors
            logger.error(f"Unexpected error scaling deployment '{name}': {e}")
            return False

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