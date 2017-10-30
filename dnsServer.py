from scapy.all import *

white_list = [
    'teredo.ipv6.microsoft.com',
]

black_list = [
    'sajajlyoogrmkokirbxarnollmwlvajdkotpkcwetgqjjhngydlpl.ltfsaveknnjnlmhtcoeslsosnupq.nylalobghyhirgh.com.',
    'sajajlyoogrmkbkjmijfogwgsmwlvajdkntpkcwetgqjjhngyd.lplltfsaveknnjnlmhtcoeslsosnupq.nylalobghyhirgh.com.',
]

def dnsServer(pkt):
    if pkt.haslayer(DNSQR):  # DNS question record
        print('Receive:')
        print('\tqd=%s' % pkt[DNS].qd)
        print('\tqname=%s' % pkt[DNS].qd.qname)
        print('\trd=%s' % pkt[DNS].rd)
        print('\tqtype=%s\n' % pkt[DNS].qd.qtype)
        if pkt[DNS].qd.qtype == 16:  # TXT
            ipLayer = IP(dst=pkt[IP].src, src=pkt[IP].dst)
            udpLayer = UDP(dport=pkt[UDP].sport, sport=pkt[UDP].dport)
            dnsLayer = DNS(id=pkt[DNS].id,
                            aa=1, #we are authoritative
                            qr=1, #it's a response
                            rd=pkt[DNS].rd, # copy recursion-desired
                            qdcount=pkt[DNS].qdcount, # copy question-count
                            qd=pkt[DNS].qd, # copy question itself
                            ancount=1, #we provide a single answer
                            an=DNSRR(rrname=pkt[DNS].qd.qname, type='TXT', ttl=1, rdlen=len('door')+1, rdata='door'),
                        )

            answer = ipLayer / udpLayer / dnsLayer

            send(answer)
            print('Send:')
            print('\t%s' % dnsLayer.show())


#sniff(filter='udp port 53', iface='eth0', store=0, prn=dnsServer)
ipLayer = IP(dst='192.168.154.138', src='192.168.154.135')
udpLayer = UDP(dport=53, sport=12345)
qname = 'google.com.'
qd = 'google.com'
dnsLayer = DNS(id=1, aa=1, qr=1, rd=1, qdcount=1, qd=qd, ancount=1, an=DNSRR(rrname=qname, type='TXT', ttl=1, rdlen=len('door')+1, rdata='door'))

answer = ipLayer / udpLayer / dnsLayer
send(answer)