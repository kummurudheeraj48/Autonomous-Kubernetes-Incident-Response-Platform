# KubeGuardian: Autonomous Kubernetes Incident Response Platform

An intelligent, cloud-native Site Reliability Engineering (SRE) microservice engine that monitors cluster health, executes automated network fabric latency checks, and leverages rule-based string analytics to instantly diagnose application runtime failures and container engine registry misconfigurations.

## 🏗️ System Architecture Overview

- **Detection Engine (`src/watcher/`)**: A 24/7 background daemon running natively inside the cluster that uses the official Kubernetes API to intercept failing cluster event hooks.
- **Diagnosis Engine (`src/diagnosis/`)**: A modular regex-pattern-matching analysis engine that parses raw cluster failure logs and maps them to clear, structured remediation workflows.
- **Network Fabric Probe (`src/probes/`)**: An automated network utility scheduled as a Kubernetes CronJob to execute lightweight diagnostic packet pings every 5 minutes to verify internal cluster routing.

## 🚀 Getting Started & Deployment

### 1. In-Cluster Security (RBAC)
Apply the customized access policies to grant the engine permission to monitor your cluster events namespaces:
```bash
sudo kubectl apply -f k8s/base/rbac.yaml
