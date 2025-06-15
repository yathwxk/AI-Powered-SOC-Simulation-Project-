import pandas as pd

def parse_log_file(file_path):
    # Define empty lists to store the extracted information
    timestamps = []
    usernames = []
    ips = []
    statuses = []
    agents = []
    
    with open(file_path, 'r') as file:
        for line in file:
            # Strip any leading/trailing whitespace
            line = line.strip()

            # Skip lines that don't match the expected log format
            if "LOGIN" not in line:
                continue
            
            try:
                # Split the line by spaces
                parts = line.split(" ")

                # Check if the parts array has the expected number of elements
                if len(parts) < 5:
                    print(f"Skipping malformed line: {line}")
                    continue

                # Extract timestamp
                timestamp = parts[0] + " " + parts[1]  # Combining date and time
                timestamps.append(timestamp)
                
                # Extract username and handle missing parts
                user_part = next((part for part in parts if part.startswith("user=")), None)
                if user_part:
                    username = user_part.split("=")[1]
                else:
                    username = "Unknown"
                usernames.append(username)
                
                # Extract IP
                ip_part = next((part for part in parts if part.startswith("ip=")), None)
                if ip_part:
                    ip = ip_part.split("=")[1]
                else:
                    ip = "Unknown"
                ips.append(ip)
                
                # Extract status
                status_part = next((part for part in parts if part.startswith("status=")), None)
                if status_part:
                    status = status_part.split("=")[1]
                else:
                    status = "Unknown"
                statuses.append(status)

                # Extract User-Agent
                agent_part = next((part for part in parts if part.startswith("agent=")), None)
                if agent_part:
                    agent = agent_part.split("=")[1]
                else:
                    agent = "Unknown"
                agents.append(agent)
            
            except Exception as e:
                print(f"Error processing line: {line}")
                print(f"Error details: {e}")
                continue
    
    # Create a DataFrame to store the parsed data
    df = pd.DataFrame({
        'Timestamp': timestamps,
        'Username': usernames,
        'IP': ips,
        'Status': statuses,
        'User-Agent': agents
    })
    
    return df

# Example usage
log_file = r'C:\Users\yathw\OneDrive\Desktop\VAPT\logs\login_attempts.log'
df = parse_log_file(log_file)
print(df)
# Save the parsed data to CSV
df.to_csv(r'C:\Users\yathw\OneDrive\Desktop\VAPT\parsed_login_logs.csv', index=False)