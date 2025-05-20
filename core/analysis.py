from core.monitor import Monitor
from google import genai
import os

class Analysis:
    def __init__(self):
        self.monitor = Monitor()
        self.apiKey = os.getenv("GEMINI_API_KEY")

        if not self.apiKey:
            print("API key is undefined, did you forgot to add GEMINI_API_KEY to .env?")
            return

    def run(self):
        packets = self.monitor.run()
        output = self._feed_to_LLM(self._generate_system_prompt(), packets)
        return output

    def _generate_system_prompt(self):
        return """
        You are a cybersecurity analyst AI specialized in network traffic analysis.

        You will be given a JSON object representing a single network packet with the following fields:
        - timestamp: ISO8601 timestamp of the packet capture
        - src_ip: Source IP address
        - dst_ip: Destination IP address
        - protocol: IP protocol number (e.g., 6 for TCP)
        - src_port: Source port number
        - dst_port: Destination port number
        - flags: TCP flags set on the packet (e.g., "A" for ACK)
        - length: Packet length in bytes

        Your task is to:

        1. Analyze the packet fields to detect potential anomalies or suspicious signs.
        2. Provide an **abnormality rate** — a numeric score between 0 and 100, where 0 means perfectly normal traffic and 100 means highly suspicious or abnormal.
        3. Explain in a short paragraph the main reasons for your score, citing any suspicious attributes.

        Output your response in JSON format like this:

        {
          "abnormality_rate": <number between 0-100>,
          "reason": "<short explanation>"
        }

        Evaluate the packet carefully based on typical network behavior, ports, protocols, flags, and IP addresses. Consider aspects like unusual ports, suspicious flag combinations, or uncommon packet sizes.

        ---

        Here is the packet JSON:
        <INSERT PACKET JSON HERE>
        """

    def _feed_to_LLM(self, systemPrompt, packetsToAnalyse):
        client = genai.Client(api_key=self.apiKey)
        chat = client.chats.create(model='gemini-1.5-flash')

        response = chat.send_message(f"{systemPrompt} {packetsToAnalyse}")

        output = response.candidates[0].content.parts[0].text
        return output
