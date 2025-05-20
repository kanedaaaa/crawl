import argparse
from rich import print
from rich.console import Console
from core.crawler import Crawler
from dotenv import load_dotenv
import os

load_dotenv()

console = Console()

def main():
    parser = argparse.ArgumentParser(description="🕵️ Gemini Network Analyzer CLI")
    parser.add_argument("--batch-size", type=int, default=100, help="Number of packets per batch (default: 100)")
    args = parser.parse_args()

    console.print(f"[bold green]Starting crawler with batch size: {args.batch_size}[/bold green]")

    try:
        crawler = Crawler(batch_size=args.batch_size)
        crawler.run()
    except KeyboardInterrupt:
        console.print("\n[bold red]Interrupted by user. Exiting...[/bold red]")

if __name__ == "__main__":
    main()
