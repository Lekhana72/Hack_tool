from scapy.all import sniff, wrpcap, IP, TCP, Raw
import datetime

# Store captured packets
packets = []

# Packet handler
def packet_callback(packet):
    packets.append(packet)  # Store for saving later
    
    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        proto = packet[IP].proto
        length = len(packet)

        # Protocol name
        if proto == 6:
            proto_name = "TCP"
        elif proto == 17:
            proto_name = "UDP"
        else:
            proto_name = str(proto)

        print(f"[+] {ip_src} --> {ip_dst} | Protocol: {proto_name} | Length: {length}")

        # Try to parse HTTP traffic
        if packet.haslayer(Raw) and packet.haslayer(TCP):
            try:
                payload = packet[Raw].load.decode(errors="ignore")
                if "HTTP" in payload or "GET " in payload or "POST " in payload:
                    print("\n--- HTTP Data ---")
                    print(payload.split("\n")[0:10])  # Show first 10 lines of HTTP data
                    print("-----------------\n")
            except:
                pass

# Main capture function
def start_sniffer():
    print("[*] Starting advanced packet sniffer...")
    print("[*] Press Ctrl+C to stop and save packets to file.\n")

    try:
        sniff(filter="ip", prn=packet_callback, store=False)
    except KeyboardInterrupt:
        save_packets()

# Save packets to pcap
def save_packets():
    filename = f"packets_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pcap"
    wrpcap(filename, packets)
    print(f"\n[+] Saved {len(packets)} packets to {filename}")
    print("[*] You can open this file in Wireshark.")

if __name__ == "__main__":
    start_sniffer()
