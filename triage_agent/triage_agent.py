import json
import openai

# Set your OpenAI API key
openai.api_key = "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"

# Load mock logs
def load_logs(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# Enrich logs with OpenAI GPT
def enrich_logs(logs):
    enriched_logs = []
    for log in logs:
        # Using ChatCompletion API for enrichment
        prompt = f"Enrich the following alert: {log}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant that enriches security alerts."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            request_timeout=30  # Add timeout to avoid hanging
        )
        log["enrichment"] = response["choices"][0]["message"]["content"].strip()
        enriched_logs.append(log)
    return enriched_logs

# Save enriched logs
def save_enriched_logs(enriched_logs, output_path):
    with open(output_path, "w") as file:
        json.dump(enriched_logs, file, indent=4)

if __name__ == "__main__":
    # Load logs
    logs = load_logs("triage_agent/mock_logs.json")
    # Enrich logs
    enriched_logs = enrich_logs(logs)
    # Save enriched logs
    save_enriched_logs(enriched_logs, "data/enriched_alerts.json")
    print("Enrichment completed. Check data/enriched_alerts.json")
