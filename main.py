#!/usr/bin/env python3
"""
MySECOPS AI Agents - Main Orchestrator
This script runs the complete security alert processing pipeline:
1. Triage Agent - Enriches alerts using GPT-4
2. Hunting Agent - Maps to MITRE ATT&CK/ATLAS and scores threats
3. Response Agent - Generates mitigation recommendations
4. Dashboard - Visualizes results (optional)
"""

import json
import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('secops_pipeline.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Import agent modules
try:
    sys.path.append(str(Path(__file__).parent))
    from triage_agent.triage_agent import load_logs, enrich_logs, save_enriched_logs
    from hunting_agent.hunting_agent import search_iocs, map_ttps, assign_threat_scores, save_mappings
    from response_agent.response_agent import generate_response
except ImportError as e:
    logger.error(f"Failed to import agent modules: {e}")
    sys.exit(1)


class SecOpsOrchestrator:
    """Orchestrates the security operations AI agent pipeline"""

    def __init__(self):
        self.config = {
            'mock_logs': os.getenv('MOCK_LOGS_PATH', 'triage_agent/mock_logs.json'),
            'enriched_alerts': os.getenv('ENRICHED_ALERTS_PATH', 'data/enriched_alerts.json'),
            'ttp_mappings': os.getenv('TTP_MAPPINGS_PATH', 'data/ttp_mappings_with_scores.json'),
        }

        # Ensure data directory exists
        Path('data').mkdir(exist_ok=True)

    def run_triage_agent(self):
        """Step 1: Enrich security alerts using OpenAI GPT-4"""
        logger.info("=" * 60)
        logger.info("STEP 1: Running Triage Agent (Alert Enrichment)")
        logger.info("=" * 60)

        try:
            # Load mock logs
            logger.info(f"Loading logs from {self.config['mock_logs']}")
            logs = load_logs(self.config['mock_logs'])
            logger.info(f"Loaded {len(logs)} alerts")

            # Enrich logs with OpenAI
            logger.info("Enriching alerts with GPT-4...")
            enriched_logs = enrich_logs(logs)

            # Save enriched logs
            save_enriched_logs(enriched_logs, self.config['enriched_alerts'])
            logger.info(f"Enrichment completed. Saved to {self.config['enriched_alerts']}")

            return enriched_logs

        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Triage agent failed: {e}")
            raise

    def run_hunting_agent(self, enriched_logs):
        """Step 2: Hunt for IOCs and map to MITRE ATT&CK/ATLAS"""
        logger.info("=" * 60)
        logger.info("STEP 2: Running Hunting Agent (IOC Search & TTP Mapping)")
        logger.info("=" * 60)

        try:
            # Mock IOC database (in production, this would query a real threat intelligence database)
            ioc_database = {
                "192.168.1.1": "Brute Force Attack",
                "192.168.1.2": "Credential Stuffing",
                "10.0.0.5": "Malware C2 Communication"
            }

            # Mock MITRE ATT&CK data
            attck_data = {
                "192.168.1.1": "TA0001: Initial Access",
                "192.168.1.2": "TA0003: Execution",
                "10.0.0.5": "TA0011: Command and Control"
            }

            # Mock MITRE ATLAS data (AI/ML specific threats)
            atlas_data = {
                "192.168.1.1": "Model Theft: Inversion",
                "192.168.1.2": "Data Poisoning",
                "10.0.0.5": "Model Backdoor"
            }

            # Perform IOC search
            logger.info("Searching for IOCs...")
            ioc_matches = search_iocs(enriched_logs, ioc_database)
            logger.info(f"Found {len(ioc_matches)} IOC matches")

            # Map to ATT&CK and ATLAS TTPs
            logger.info("Mapping to MITRE ATT&CK and ATLAS TTPs...")
            ttp_results = map_ttps(ioc_matches, attck_data, atlas_data)

            # Assign threat scores
            logger.info("Assigning threat scores...")
            scored_results = assign_threat_scores(ttp_results)

            # Save mapped results
            save_mappings(scored_results, self.config['ttp_mappings'])
            logger.info(f"TTP mappings saved to {self.config['ttp_mappings']}")

            return scored_results

        except Exception as e:
            logger.error(f"Hunting agent failed: {e}")
            raise

    def run_response_agent(self, scored_results):
        """Step 3: Generate incident response recommendations"""
        logger.info("=" * 60)
        logger.info("STEP 3: Running Response Agent (Mitigation Recommendations)")
        logger.info("=" * 60)

        try:
            logger.info("Generating response recommendations...")
            responses = generate_response(scored_results)
            logger.info(f"Generated {len(responses)} response recommendations")

            # Display responses
            for i, response in enumerate(responses, 1):
                logger.info(f"\nRecommendation {i}:")
                logger.info(f"  Alert ID: {response['alert_id']}")
                logger.info(f"  Action: {response['action']}")
                logger.info(f"  Description: {response['description']}")

            return responses

        except Exception as e:
            logger.error(f"Response agent failed: {e}")
            raise

    def run_pipeline(self):
        """Execute the complete security operations pipeline"""
        logger.info("\n" + "=" * 60)
        logger.info("MySECOPS AI Agents Pipeline Starting")
        logger.info("=" * 60 + "\n")

        try:
            # Step 1: Triage Agent
            enriched_logs = self.run_triage_agent()

            # Step 2: Hunting Agent
            scored_results = self.run_hunting_agent(enriched_logs)

            # Step 3: Response Agent
            responses = self.run_response_agent(scored_results)

            logger.info("\n" + "=" * 60)
            logger.info("Pipeline completed successfully!")
            logger.info("=" * 60)
            logger.info(f"\nResults saved to:")
            logger.info(f"  - Enriched Alerts: {self.config['enriched_alerts']}")
            logger.info(f"  - TTP Mappings: {self.config['ttp_mappings']}")
            logger.info(f"\nTo view the dashboard, run:")
            logger.info(f"  streamlit run dashboard/dashboard.py")

            return {
                'enriched_logs': enriched_logs,
                'scored_results': scored_results,
                'responses': responses
            }

        except Exception as e:
            logger.error(f"\nPipeline failed: {e}")
            logger.error("Please check the logs above for details")
            sys.exit(1)


def main():
    """Main entry point"""
    # Verify OpenAI API key is set
    if not os.getenv('OPENAI_API_KEY'):
        logger.error("OPENAI_API_KEY not found in environment variables")
        logger.error("Please create a .env file with your API key (see .env.example)")
        sys.exit(1)

    # Run the pipeline
    orchestrator = SecOpsOrchestrator()
    orchestrator.run_pipeline()


if __name__ == "__main__":
    main()
