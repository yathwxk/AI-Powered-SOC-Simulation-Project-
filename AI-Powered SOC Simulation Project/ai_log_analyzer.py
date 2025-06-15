import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def load_data(file_path):
    return pd.read_csv(file_path)

def generate_statistics(df):
    total_entries = len(df)
    total_failed_attempts = df['Failed_Attempts'].sum()
    total_unique_ips = df['IP'].nunique()
    anomalies_detected = df[df['Anomaly'] == 'Anomaly'].shape[0]

    print("====== Log Summary ======")
    print(f"Total Log Entries        : {total_entries}")
    print(f"Total Failed Attempts    : {total_failed_attempts}")
    print(f"Unique IPs               : {total_unique_ips}")
    print(f"Anomalies Detected       : {anomalies_detected}")
    print("==========================\n")

    return {
        "total": total_entries,
        "failures": total_failed_attempts,
        "ips": total_unique_ips,
        "anomalies": anomalies_detected
    }

def ai_analysis(df):
    print("====== AI Layer Analysis ======")
    
    # Convert Anomaly to numeric
    df['Anomaly_Label'] = df['Anomaly'].apply(lambda x: 1 if x == 'Anomaly' else 0)
    
    X = df[['Failed_Attempts', 'IP_Encoded', 'Agent_Encoded']]
    y = df['Anomaly_Label']

    # Split and train a simple model (not for prediction, but insight)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # Show feature importances (weights)
    coeffs = model.coef_[0]
    features = X.columns
    print("Feature Impact on Anomalies:")
    for feature, coef in zip(features, coeffs):
        print(f"- {feature}: {'🔺' if coef > 0 else '🔻'} {round(coef, 3)}")

    print("\nClassification Report (Model Fit):")
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    print("==================================")

def analyze_anomalies(file_path):
    df = load_data(file_path)

    # Basic log stats
    generate_statistics(df)

    # AI layer for pattern interpretation
    ai_analysis(df)

if __name__ == "__main__":
    file_path = r'C:\Users\yathw\OneDrive\Desktop\VAPT\anomaly_output.csv'  # <-- This must be the output of your anomaly script
    analyze_anomalies(file_path)
