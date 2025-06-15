import random
import time
import datetime

def simulate_single_ip_brute_force(log_file, start_time, num_attempts=100):
    ip = "192.168.1.100"  # Single IP address
    username = "admin"  # Common username for brute-force attack
    status = "FAILURE"  # All attempts will fail
    user_agent = "Mozilla/5.0"  # Random user agent for variety
    
    with open(log_file, 'a') as file:
        for _ in range(num_attempts):
            timestamp = start_time + datetime.timedelta(seconds=random.randint(0, 60))  # Random time within 1 minute
            log_line = f"[{timestamp}] user={username} ip={ip} status={status} agent={user_agent}\n"
            file.write(log_line)
            time.sleep(random.uniform(0.1, 1))  # Random interval between attempts

# Example usage:
log_file = r'C:\Users\yathw\OneDrive\Desktop\VAPT\logs\login_attempts.log'
start_time = datetime.datetime.now()
simulate_single_ip_brute_force(log_file, start_time)
