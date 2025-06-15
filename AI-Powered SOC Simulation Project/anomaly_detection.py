import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

# Load parsed login data (CSV file)
def load_data(file_path):
    return pd.read_csv(file_path)

# Example usage
file_path = r'C:\Users\yathw\OneDrive\Desktop\VAPT\parsed_login_logs.csv'
data = load_data(file_path)

# Feature Engineering
def feature_engineering(df):
    # Convert Timestamp to datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='[%Y-%m-%d %H:%M:%S]')
    
    # Create additional features: Hour of the day, Failed attempts count, etc.
    df['Hour'] = df['Timestamp'].dt.hour
    df['Failed'] = df['Status'].apply(lambda x: 1 if x == 'FAILURE' else 0)

    # Encoding categorical features (Username, IP, User-Agent)
    label_encoder = LabelEncoder()
    df['Username_Encoded'] = label_encoder.fit_transform(df['Username'])
    df['IP_Encoded'] = label_encoder.fit_transform(df['IP'])
    df['Agent_Encoded'] = label_encoder.fit_transform(df['User-Agent'])

    # Aggregate data to create features for anomaly detection
    df_agg = df.groupby(['IP', 'Hour', 'Username_Encoded'], as_index=False).agg(
        {'Failed': 'sum', 'IP_Encoded': 'first', 'Agent_Encoded': 'first'}).rename(columns={'Failed': 'Failed_Attempts'})

    return df_agg

# Anomaly Detection using Isolation Forest
def detect_anomalies(df):
    # Select relevant features for anomaly detection
    features = ['Failed_Attempts', 'IP_Encoded', 'Agent_Encoded']
    X = df[features]

    # Initialize and fit the Isolation Forest model
    model = IsolationForest(contamination=0.05)  # Adjust contamination as needed
    df['Anomaly'] = model.fit_predict(X)

    # -1 indicates an anomaly, 1 means normal
    df['Anomaly'] = df['Anomaly'].apply(lambda x: 'Anomaly' if x == -1 else 'Normal')
    
    return df

# Visualization
def plot_anomalies(df):
    anomaly_df = df[df['Anomaly'] == 'Anomaly']
    normal_df = df[df['Anomaly'] == 'Normal']

    plt.figure(figsize=(10, 6))
    plt.scatter(normal_df['Failed_Attempts'], normal_df['IP_Encoded'], color='blue', label='Normal', alpha=0.6)
    plt.scatter(anomaly_df['Failed_Attempts'], anomaly_df['IP_Encoded'], color='red', label='Anomaly', alpha=0.6)
    plt.xlabel('Failed Attempts')
    plt.ylabel('IP Encoded')
    plt.title('Anomaly Detection: Failed Login Attempts')
    plt.legend()
    plt.show()

# Main function to orchestrate the process
def main():
    # Load data (CSV output from the parsing script)
    log_file = r'C:\Users\yathw\OneDrive\Desktop\VAPT\parsed_login_logs.csv'
    df = load_data(log_file)

    # Feature Engineering
    df_agg = feature_engineering(df)
    
    # Detect anomalies
    df_anomalies = detect_anomalies(df_agg)

    # Show detected anomalies
    print("Detected Anomalies:")
    print(df_anomalies[df_anomalies['Anomaly'] == 'Anomaly'])
    df_anomalies.to_csv(r'C:\Users\yathw\OneDrive\Desktop\VAPT\anomaly_output.csv', index=False)
    # Plot results
    plot_anomalies(df_anomalies)

if __name__ == "__main__":
    main()
