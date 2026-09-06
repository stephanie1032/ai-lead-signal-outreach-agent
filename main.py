import argparse
import logging

from src.pipeline import OutreachPipeline

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv():
        return False


def parse_args():
    parser = argparse.ArgumentParser(description="Detect sales signals and draft outreach.")
    parser.add_argument("--input", required=True, help="Path to a CSV file of leads")
    parser.add_argument("--database", default="outreach.db", help="SQLite audit database")
    parser.add_argument("--minimum-score", type=int, default=45)
    parser.add_argument("--dry-run", action="store_true", help="Never prompt for approval")
    parser.add_argument("--use-llm", action="store_true", help="Use OpenAI for message drafts")
    return parser.parse_args()


def main():
    load_dotenv()
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
    pipeline = OutreachPipeline(
        database_path=args.database,
        minimum_score=args.minimum_score,
        dry_run=args.dry_run,
        use_llm=args.use_llm,
    )
    pipeline.run(args.input)


if __name__ == "__main__":
    main()
