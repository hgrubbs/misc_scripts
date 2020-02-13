## ip tuntap
from http://www.rkeene.org/tmp/ssh-ip-tunnel.txt

    HostA$ sudo -i ip tuntap add mode tun user rkeene name tun9410
    HostA$ sudo -i ip link set tun9410 up
    HostA$ sudo -i ip addr add local 1.2.3.4/32 remote 1.2.3.5/32 dev tun9410
    HostA$ ssh HostB 'sudo -i ip tuntap add mode tun user rkeene name tun174'
    HostA$ ssh HostB 'sudo -i ip link set tun174 up'
    HostA$ ssh HostB 'sudo -i ip addr add local 1.2.3.5/32 remote 1.2.3.4/32 dev tun174'
    HostA$ ip link show dev tun9410

    9701: tun9410: &lt;NO-CARRIER,POINTOPOINT,MULTICAST,NOARP,UP&gt; mtu 1500 qdisc pfifo_fast state DOWN mode DEFAULT group default qlen 500
        link/none

    HostA$ ip addr show dev tun9410
    9701: tun9410: &lt;NO-CARRIER,POINTOPOINT,MULTICAST,NOARP,UP&gt; mtu 1500 qdisc pfifo_fast state DOWN group default qlen 500
        link/none
        inet 1.2.3.4/32 peer 1.2.3.5/32 scope global tun9410
           valid_lft forever preferred_lft forever

    HostA$ ssh -w 9410:174 HostB 'ping -c 5 1.2.3.4'
    PING 1.2.3.4 (1.2.3.4) 56(84) bytes of data.
    64 bytes from 1.2.3.4: icmp_seq=1 ttl=64 time=1.06 ms
    64 bytes from 1.2.3.4: icmp_seq=2 ttl=64 time=1.74 ms
    64 bytes from 1.2.3.4: icmp_seq=3 ttl=64 time=1.83 ms
    64 bytes from 1.2.3.4: icmp_seq=4 ttl=64 time=1.09 ms
    64 bytes from 1.2.3.4: icmp_seq=5 ttl=64 time=1.02 ms

    --- 1.2.3.4 ping statistics ---
    5 packets transmitted, 5 received, 0% packet loss, time 4005ms
    rtt min/avg/max/mdev = 1.023/1.352/1.831/0.360 ms
    HostA$ ssh HostB 'ping -c 5 1.2.3.4'
    PING 1.2.3.4 (1.2.3.4) 56(84) bytes of data.

    --- 1.2.3.4 ping statistics ---
    5 packets transmitted, 0 received, 100% packet loss, time 3999ms

    HostA$ sudo -i ip link delete dev tun9410
    HostA$ ssh HostB 'sudo -i ip link delete dev tun174'
