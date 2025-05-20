from rich import print
from rich.console import Console
from threading import Thread
from queue import Queue
import time

from core.monitor import Monitor
from core.analysis import Analysis

console = Console()

class Crawler:
    def __init__(self, batch_size=100):
        self.batch_size = batch_size
        self.queue = Queue()
        self.monitor = Monitor()
        self.analysis = Analysis()
        self.running = True

    def _sniff_packets(self):
        while self.running:
            packets_json = self.monitor.run(count=self.batch_size)
            self.queue.put(packets_json)

    def _analyze_packets(self):
        while self.running or not self.queue.empty():
            try:
                batch = self.queue.get(timeout=1)
                console.print("\n[cyan][+][/cyan] Analyzing next batch...\n")
                result = self.analysis._feed_to_LLM(self.analysis._generate_system_prompt(), batch)
                console.print(f"[green]{result}[/green]")
            except Exception as e:
                pass

    def run(self):
        console.print("[yellow][*][/yellow] Starting packet capture and analysis...\n")
        sniff_thread = Thread(target=self._sniff_packets)
        analyze_thread = Thread(target=self._analyze_packets)

        sniff_thread.start()
        analyze_thread.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            console.print("\n[bold red][!] Stopping...[/bold red]")
            self.running = False
            sniff_thread.join()
            analyze_thread.join()
            console.print("[bold green][*] Shutdown complete.[/bold green]")
