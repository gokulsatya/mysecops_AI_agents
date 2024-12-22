import json

# Simulate IOC search
def search_iocs(enriched_logs, ioc_database):
    ioc_matches = []
    for log in enriched_logs:
        if log["source_ip"] in ioc_database:
            ioc_matches.append({
                "alert_id": log["alert_id"],
                "source_ip": log["source_ip"],
                "ioc": ioc_database[log["source_ip"]],
                "description": "Matched known IOC"
            })
    return ioc_matches

# Map IOCs to MITRE ATT&CK and ATLAS TTPs
def map_ttps(ioc_matches, attck_data, atlas_data):
    mapped_results = []
    for match in ioc_matches:
        ttp = attck_data.get(match["source_ip"], "Unknown TTP")
        ai_threat = atlas_data.get(match["source_ip"], "No AI-specific threat")

        match["ttp"] = ttp
        match["ai_threat"] = ai_threat
        mapped_results.append(match)
    return mapped_results

# Assign threat scores based on TTP severity
def assign_threat_scores(mapped_results):
    severity_mapping = {
        "TA0001: Initial Access": "Critical",
        "TA0003: Execution": "High",
        "Unknown TTP": "Medium",
        "No AI-specific threat": "Low"
    }

    for result in mapped_results:
        ttp_severity = severity_mapping.get(result["ttp"], "Medium")
        ai_threat_severity = severity_mapping.get(result["ai_threat"], "Low")

        # Combine both scores; use the higher one as the overall score
        if ttp_severity == "Critical" or ai_threat_severity == "Critical":
            result["threat_score"] = "Critical"
        elif ttp_severity == "High" or ai_threat_severity == "High":
            result["threat_score"] = "High"
        elif ttp_severity == "Medium" or ai_threat_severity == "Medium":
            result["threat_score"] = "Medium"
        else:
            result["threat_score"] = "Low"
    return mapped_results

# Save TTP mappings to file
def save_mappings(mappings, output_path):
    with open(output_path, "w") as file:
        json.dump(mappings, file, indent=4)

if __name__ == "__main__":
    # Load enriched logs
    with open("data/enriched_alerts.json", "r") as file:
        enriched_logs = json.load(file)

    # Mock IOC database
    ioc_database = {
        "192.168.1.1": "Brute Force Attack",
        "192.168.1.2": "Credential Stuffing"
    }

    # Mock MITRE ATT&CK data
    attck_data = {
        "192.168.1.1": "TA0001: Initial Access",
        "192.168.1.2": "TA0003: Execution"
    }

    # Mock MITRE ATLAS data
    atlas_data = {
        "192.168.1.1": "Model Theft: Inversion",
        "192.168.1.2": "Data Poisoning"
    }

    # Perform IOC search
    ioc_matches = search_iocs(enriched_logs, ioc_database)
    print("IOC Matches:", ioc_matches)

    # Map to ATT&CK and ATLAS TTPs
    ttp_results = map_ttps(ioc_matches, attck_data, atlas_data)

    # Assign threat scores
    scored_results = assign_threat_scores(ttp_results)
    print("Scored Results:", scored_results)

    # Save mapped results to JSON
    save_mappings(scored_results, "data/ttp_mappings_with_scores.json")
    print("Mapped TTPs with Threat Scores saved to data/ttp_mappings_with_scores.json")
