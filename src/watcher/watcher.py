import os
import sys
from kubernetes import client, config, watch

def main():
    print("[-] KubeGuardian: Initializing Event Watcher Engine...")
    
    try:
        config.load_incluster_config()
        print("[+] Loaded In-Cluster Kubernetes Configuration.")
    except config.ConfigException:
        try:
            config.load_kube_config()
            print("[+] Loaded Local Kubeconfig Context.")
        except config.ConfigException:
            print("[CRITICAL] Could not configure Kubernetes client. Exiting.")
            sys.exit(1)

    v1 = client.CoreV1Api()
    w = watch.Watch()

    print("[+] KubeGuardian: Actively streaming cluster events. Listening...")
    
    try:
        for event in w.stream(v1.list_event_for_all_namespaces):
            event_obj = event['object']
            
            # Use fallback empty strings if the cluster events emit None values
            reason = event_obj.reason or ""
            message = event_obj.message or ""
            
            target_reasons = ["CrashLoopBackOff", "Failed", "BackOff", "OOMKilled"]
            
            # Safe checking against validated string objects
            if reason in target_reasons or any(x in message for x in target_reasons):
                print(f"\n[ALERT DETECTED] Time: {event_obj.last_timestamp or event_obj.first_timestamp}")
                print(f" Namespace: {event_obj.metadata.namespace}")
                print(f" Reason   : {reason}")
                print(f" Message  : {message}")
                print("-" * 50)
                
    except KeyboardInterrupt:
        print("\n[-] Watcher engine stopped by user.")
    except Exception as e:
        print(f"[ERROR] An unexpected exception occurred: {e}")

if __name__ == '__main__':
    main()
