import os
import sys
import json
import socket
import time
import subprocess

def check_dns(target_host="kubernetes.default.svc.cluster.local"):
    """Measures DNS resolution latency in milliseconds."""
    start_time = time.time()
    try:
        socket.gethostbyname(target_host)
        latency = (time.time() - start_time) * 1000
        return {"status": "HEALTHY", "latency_ms": round(latency, 2), "error": None}
    except socket.gaierror as e:
        return {"status": "CRITICAL", "latency_ms": -1, "error": f"DNS Resolution Failed: {str(e)}"}

def check_packet_drops(target_ip="8.8.8.8", count=4):
    """Checks for network layer packet loss using system ping."""
    try:
        # Run ping with a timeout to catch packet drops
        cmd = ["ping", "-c", str(count), "-W", "2", target_ip]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, _ = process.communicate()
        output = stdout.decode('utf-8')

        # Parse out packet loss percentage from the ping summary line
        # Example: 4 packets transmitted, 4 received, 0% packet loss
        for line in output.split('\n'):
            if "packet loss" in line:
                parts = line.split(',')
                for part in parts:
                    if "packet loss" in part:
                        loss_percentage = int(part.strip().split('%')[0].split()[-1])
                        status = "HEALTHY" if loss_percentage < 10 else "DEGRADED" if loss_percentage < 50 else "CRITICAL"
                        return {"status": status, "packet_loss_percent": loss_percentage, "error": None}
                        
        return {"status": "UNKNOWN", "packet_loss_percent": -1, "error": "Could not parse ping output"}
    except Exception as e:
        return {"status": "CRITICAL", "packet_loss_percent": -1, "error": str(e)}

def main():
    print("[-] KubeGuardian: Executing Network Telemetry Probe...")
    
    # 1. Check inside-cluster CoreDNS health
    dns_metrics = check_dns()
    
    # 2. Check outer-cluster network path stability 
    network_metrics = check_packet_drops()
    
    # 3. Consolidate into a unified SRE Metric payload
    telemetry_payload = {
        "timestamp": time.time(),
        "component": "kube-guardian-network-probe",
        "metrics": {
            "dns_resolution": dns_metrics,
            "network_fabric": network_metrics
        }
    }
    
    # Output metrics as a structured JSON string for logging aggregation
    print(json.dumps(telemetry_payload, indent=2))

if __name__ == '__main__':
    main()
