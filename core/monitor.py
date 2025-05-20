from scapy.all import sniff
from datetime import datetime
import json

class Monitor:
    def run(self, count = 30):
        packets = sniff(count)
        packet_data = [self._extract_packet_info(pkt) for pkt in packets]
        json_data = json.dumps(packet_data, indent=2)

        return json_data

    def _extract_packet_info(self, pkt):
        info = {}

        info['timestamp'] = datetime.fromtimestamp(pkt.time).isoformat()

        if pkt.haslayer('IP'):
            ip_layer = pkt['IP']
            info['src_ip'] = ip_layer.src
            info['dst_ip'] = ip_layer.dst
            info['protocol'] = ip_layer.proto

        if pkt.haslayer('TCP'):
            tcp = pkt['TCP']
            info['src_port'] = tcp.sport
            info['dst_port'] = tcp.dport
            info['flags'] = str(tcp.flags)
        elif pkt.haslayer('UDP'):
            udp = pkt['UDP']
            info['src_port'] = udp.sport
            info['dst_port'] = udp.dport

        info['length'] = len(pkt)

        if pkt.haslayer('Raw'):
            payload = pkt['Raw'].load
            try:
                info['payload'] = payload[:100].decode(errors='ignore')
            except:
                info['payload'] = str(payload[:100])

        return info
