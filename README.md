# MySECOPS AI Agents

An AI-powered Security Operations (SECOPS) pipeline that automates security alert triage, threat hunting, and incident response using OpenAI GPT-4 and MITRE ATT&CK/ATLAS frameworks.

## Overview

This project implements a modular pipeline of AI agents that work together to:

1. **Triage Agent**: Enriches security alerts using OpenAI GPT-4
2. **Hunting Agent**: Searches for Indicators of Compromise (IOCs) and maps threats to MITRE ATT&CK and ATLAS frameworks
3. **Response Agent**: Generates automated incident response recommendations
4. **Dashboard**: Visualizes threat intelligence and TTP mappings using Streamlit

## Architecture

```
Security Alerts → Triage Agent → Hunting Agent → Response Agent → Dashboard
                      ↓               ↓              ↓              ↓
                 Enrichment    IOC/TTP Mapping  Mitigations   Visualization
```

## Features

- **AI-Powered Alert Enrichment**: Leverages GPT-4 to provide context and analysis for security alerts
- **MITRE Integration**: Maps threats to MITRE ATT&CK tactics and MITRE ATLAS AI/ML-specific threats
- **Threat Scoring**: Automatically assigns severity levels (Critical, High, Medium, Low)
- **Automated Response**: Generates actionable mitigation recommendations
- **Interactive Dashboard**: Real-time visualization with filtering capabilities
- **Secure Configuration**: Environment variable management for API keys

## Prerequisites

- Python 3.8+
- OpenAI API key (GPT-4 access required)
- pip or conda for package management

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/mysecops_AI_agents.git
cd mysecops_AI_agents
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4
```

**IMPORTANT**: Never commit your `.env` file to version control!

## Usage

### Running the Complete Pipeline

The easiest way to run the entire pipeline is using the orchestrator:

```bash
python main.py
```

This will:
1. Load mock security alerts from `triage_agent/mock_logs.json`
2. Enrich alerts using GPT-4
3. Search for IOCs and map to MITRE frameworks
4. Generate response recommendations
5. Save results to the `data/` directory

### Running Individual Agents

You can also run each agent independently:

#### Triage Agent (Alert Enrichment)

```bash
python triage_agent/triage_agent.py
```

Output: `data/enriched_alerts.json`

#### Hunting Agent (IOC Search & TTP Mapping)

```bash
python hunting_agent/hunting_agent.py
```

Output: `data/ttp_mappings_with_scores.json`

#### Response Agent (Mitigation Recommendations)

```bash
python response_agent/response_agent.py
```

Output: Console output with recommendations

#### Dashboard (Visualization)

```bash
streamlit run dashboard/dashboard.py
```

Access the dashboard at: http://localhost:8501

### Testing OpenAI Connection

To verify your API key is working:

```bash
python scripts/test_openai.py
```

## Project Structure

```
mysecops_AI_agents/
├── main.py                          # Main orchestrator
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variable template
├── .gitignore                       # Git ignore rules
├── README.md                        # This file
│
├── triage_agent/                    # Alert enrichment
│   ├── triage_agent.py
│   └── mock_logs.json
│
├── hunting_agent/                   # IOC search & TTP mapping
│   └── hunting_agent.py
│
├── response_agent/                  # Mitigation recommendations
│   └── response_agent.py
│
├── dashboard/                       # Streamlit visualization
│   └── dashboard.py
│
├── data/                            # Generated outputs
│   ├── enriched_alerts.json
│   └── ttp_mappings_with_scores.json
│
└── scripts/                         # Utility scripts
    └── test_openai.py
```

## Configuration

Environment variables (`.env` file):

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `OPENAI_MODEL` | GPT model to use | `gpt-4` |
| `MOCK_LOGS_PATH` | Path to mock logs | `triage_agent/mock_logs.json` |
| `ENRICHED_ALERTS_PATH` | Output path for enriched alerts | `data/enriched_alerts.json` |
| `TTP_MAPPINGS_PATH` | Output path for TTP mappings | `data/ttp_mappings_with_scores.json` |

## Sample Data

The project includes mock security alerts in `triage_agent/mock_logs.json`:

```json
[
  {
    "alert_id": "123",
    "source_ip": "192.168.1.1",
    "event": "Failed SSH login",
    "timestamp": "2025-01-10T12:00:00Z"
  }
]
```

### Adding Your Own Alerts

Edit `triage_agent/mock_logs.json` to add custom alerts. Each alert should include:
- `alert_id`: Unique identifier
- `source_ip`: Source IP address
- `event`: Description of the security event
- `timestamp`: ISO 8601 timestamp

## Output Files

### Enriched Alerts (`data/enriched_alerts.json`)

Contains original alerts with GPT-4 enrichment:

```json
[
  {
    "alert_id": "123",
    "source_ip": "192.168.1.1",
    "event": "Failed SSH login",
    "enrichment": "This alert indicates a potential brute force attack..."
  }
]
```

### TTP Mappings (`data/ttp_mappings_with_scores.json`)

Contains threat intelligence mappings:

```json
[
  {
    "alert_id": "123",
    "source_ip": "192.168.1.1",
    "ioc": "Brute Force Attack",
    "ttp": "TA0001: Initial Access",
    "ai_threat": "Model Theft: Inversion",
    "threat_score": "Critical"
  }
]
```

## Security Considerations

1. **API Key Protection**: Never commit `.env` files or hardcode API keys
2. **Mock Data**: This project uses simulated data. In production:
   - Integrate with real SIEM systems (Splunk, ELK, etc.)
   - Connect to actual threat intelligence feeds
   - Implement proper authentication and authorization
3. **Rate Limiting**: OpenAI API has rate limits. Implement batching for large alert volumes
4. **Data Privacy**: Ensure compliance with data protection regulations when processing security logs

## Limitations

- **Mock Data**: Currently uses simulated IOC databases and MITRE mappings
- **No Persistence**: Results are stored in JSON files (consider adding a database)
- **Sequential Processing**: Pipeline runs sequentially (could be parallelized)
- **Limited Error Recovery**: Basic error handling (needs production-grade resilience)

## Future Enhancements

- [ ] Integration with real SIEM platforms (Splunk, ELK)
- [ ] Database backend (PostgreSQL, MongoDB)
- [ ] Real-time alert streaming
- [ ] Automated response execution (with approval workflow)
- [ ] Multi-model support (Claude, Gemini, Llama)
- [ ] REST API for external integrations
- [ ] Containerization (Docker)
- [ ] CI/CD pipeline
- [ ] Unit and integration tests

## Troubleshooting

### "OPENAI_API_KEY not found" error

Make sure:
1. You created a `.env` file in the project root
2. The file contains `OPENAI_API_KEY=your-key-here`
3. There are no spaces around the `=` sign

### Import errors

Install dependencies:
```bash
pip install -r requirements.txt
```

### OpenAI API errors

Check:
1. Your API key is valid
2. You have GPT-4 access enabled
3. You have sufficient API credits
4. Your network allows connections to api.openai.com

### Dashboard not loading data

Ensure you've run the pipeline first:
```bash
python main.py
```

This generates the required `data/ttp_mappings_with_scores.json` file.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **OpenAI**: GPT-4 API for alert enrichment
- **MITRE**: ATT&CK and ATLAS frameworks for threat intelligence
- **Streamlit**: Interactive dashboard framework

## Support

For issues or questions:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review OpenAI documentation: https://platform.openai.com/docs

## Disclaimer

This is a demonstration project for educational purposes. For production security operations, conduct thorough security audits, implement proper access controls, and follow your organization's security policies.
