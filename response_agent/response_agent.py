def generate_response(ioc_matches):
    responses = []
    for match in ioc_matches:
        response = {
            "alert_id": match["alert_id"],
            "action": f"Block IP {match['source_ip']} on the firewall",
            "description": f"Response to {match['ioc']} linked to TTP: {match['ttp']}"
        }
        responses.append(response)
    return responses

if __name__ == "__main__":
    # Mock data for IOC matches
    ioc_matches = [
        {
            "alert_id": "123",
            "source_ip": "192.168.1.1",
            "ioc": "Brute Force Attack",
            "ttp": "TA0001: Initial Access"
        }
    ]

    # Generate responses
    responses = generate_response(ioc_matches)
    print("Suggested Responses:", responses)
