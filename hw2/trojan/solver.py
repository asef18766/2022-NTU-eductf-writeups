from scapy.all import * 
from scapy.layers.inet import TCP
from scapy.packet import Raw
def dump_payload(filename:str)->bytearray:
    paylist = bytearray()
    with PcapReader(filename) as pcap_reader:
        for idx, pkt in enumerate(pcap_reader):
            if 'TCP' in pkt:
                tcp_pkt:TCP = pkt['TCP']
                if idx in [7, 8, 9]:
                    paylist += bytearray(bytes(tcp_pkt.payload))
    return paylist
def main():
    ct = dump_payload('log_65a0163d1ae2e798.pcapng')
    key = b"0vCh8RrvqkrbxN9Q7Ydx\x00"
    open("res.png", "wb").write(bytes([key[idx % 0x15] ^ c for idx, c in enumerate(ct)]))
    
if __name__ == "__main__":
    main()