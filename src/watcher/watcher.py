import os
import sys
from kubernetes import client, config, watch
from diagnosis.analyzer import IncidentAnalyzer
# Import the diagnosis engine from your new sibling directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from diagnosis.analyzer import IncidentAnalyzer

def main():
    print("[-] KubeGuardian: Initializing Event Watcher Engine...")
    
    # Initialize the automated diagnosis sub-engine
    analyzer = IncidentAnalyzer()

    try:
        config.load_incluster_config()
        print("[+] Loaded In-Cluster Kubernetes Configuration.")
    except config.ConfigException:
        try:
            config.load_kube_config()
            print("[+] Loaded Local Kubeconfig Context.")
        except Exception as e:
            print(f"[!] Critical: Failed to load any Kubernetes authorization context: {e}")
            sys.exit(1)

    v1 = client.CoreV1Api()
    w = watch.Watch()
    
    # Targeted operational failure states
    target_reasons = ["CrashLoopBackOff", "Failed", "BackOff", "OOMKilled", "ErrImagePull", "ImagePullBackOff"]
    
    print("[+] KubeGuardian: Actively streaming cluster events. Listening...")
    
    try:
        for event in w.stream(v1.list_event_for_all_namespaces, timeout_seconds=0):
            obj = event['object']
            if obj and hasattr(obj, 'reason') and obj.reason in target_reasons:
                reason = obj.reason or ""
                message = obj.message or ""
                namespace = obj.metadata.namespace if obj.metadata else "unknown"
                
                print(f"\n[ALERT DETECTED] Namespace: {namespace} | Reason: {reason}")
                print(f" Raw Message: {message}")
                
                # Execute Automated Root Cause Diagnosis
                diagnosis = analyzer.analyze_incident(reason, message)
                
                print(f" [DIAGNOSIS]: {diagnosis['root_cause']} (Confidence: {diagnosis['confidence']})")
                print(f" [ACTION REQUIRED]: {diagnosis['recommended_action']}")
                print("-" * 50)
                
    except KeyboardInterrupt:
        print("\n[-] Shutting down KubeGuardian Watcher Engine gracefully.")

if __name__ == "__main__":
    main()
