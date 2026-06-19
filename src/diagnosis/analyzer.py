import re

class IncidentAnalyzer:
    def __init__(self):
        # Precise error signatures for rule-based matching
        self.signatures = {
            "OOMKilled": r"(OOMKilled|Exit Code 137|LimitExceeded)",
            "CrashLoopBackOff": r"(CrashLoopBackOff|BackOff|Exit Code 1|runtime error)",
            "ImagePullFailure": r"(ErrImagePull|ImagePullBackOff|not found|repository does not exist)"
        }

    def analyze_incident(self, reason, message):
        """Parses event metadata to determine the exact root cause."""
        combined_text = f"{reason} {message}".lower()
        
        # 1. Check for Image Pull issues
        if any(re.search(self.signatures["ImagePullFailure"].lower(), combined_text) or x in combined_text for x in ["pull", "image"]):
            return {
                "root_cause": "IMAGE_REGISTRY_ERROR",
                "confidence": "HIGH",
                "recommended_action": "Verify container image tag spelling, registry permissions, or network access to Docker Hub."
            }
            
        # 2. Check for Out-Of-Memory termination
        if re.search(self.signatures["OOMKilled"].lower(), combined_text):
            return {
                "root_cause": "RESOURCE_OOM_KILLED",
                "confidence": "MAXIMUM",
                "recommended_action": "Increase the memory limit constraints inside the pod's deployment manifest."
            }
            
        # 3. Check for application code crashes
        if re.search(self.signatures["CrashLoopBackOff"].lower(), combined_text):
            return {
                "root_cause": "APPLICATION_RUNTIME_CRASH",
                "confidence": "HIGH",
                "recommended_action": "Check container internal logs using 'kubectl logs' to debug application runtime faults."
            }
            
        return {
            "root_cause": "UNKNOWN_INFRASTRUCTURE_FAULT",
            "confidence": "LOW",
            "recommended_action": "Escalate incident telemetry to cluster administrator for manual inspection."
        }

# Quick local unit test
if __name__ == "__main__":
    analyzer = IncidentAnalyzer()
    print("Testing Diagnostic Analyzer Engine...")
    test_result = analyzer.analyze_incident("BackOff", "Back-off pulling image nginx:invalid-tag")
    print(f"Diagnostic Result:\n{test_result}")
