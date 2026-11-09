import random
import time
from datetime import datetime

SERVICES = ["auth-service", "payment-gateway", "database-pg", "k8s-ingress", "sap-connector"]
LOG_LEVELS = ["INFO", "INFO", "INFO", "WARN", "ERROR"]

ERROR_MESSAGES = [
    "PostgreSQL Connection Timeout after 30000ms at 10.0.4.12:5432",
    "Kubernetes OOMKilled: Container memory limit (512MiB) exceeded",
    "BeyondTrust VPN Authentication failed for service account 'sa_backup'",
    "SAP RFC Connection Error: System PRD-01 unreachable on port 3300",
    "HTTP 504 Gateway Timeout: Ingress controller failed to route traffic"
]

INFO_MESSAGES = [
    "User authentication successful",
    "GET /api/v1/healthcheck HTTP/1.1 200 OK",
    "Scheduled job completed: cleanup_temp_files",
    "DB Connection pool idle: 4/10 active connections"
]

def generate_log_entry():
    level = random.choice(LOG_LEVELS)
    service = random.choice(SERVICES)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if level == "ERROR":
        message = random.choice(ERROR_MESSAGES)
        is_anomaly = True
    else:
        message = random.choice(INFO_MESSAGES)
        is_anomaly = False

    return {
        "timestamp": timestamp,
        "service": service,
        "level": level,
        "message": message,
        "is_anomaly": is_anomaly
    }