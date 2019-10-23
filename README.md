# Stratum-POC

## Closed Loop Automation of SDN

### Abstract
We are trying to acheive closed loop automation by sensing the metric at switch level and pushing the new policies from controller to whitebox switches

### Components
SDN Controller : ONOS

Pipe line      : P4

Data Plane     : Stratum Switches

#### Data plane

Mininet Reference : https://github.com/stratum/tutorial

Intro - We are using MRI excersis for this POC. From P4 Tutorials compile MRI.P4 and collect the artifacts (mri.json & mri.p4.info.txt) 

1. Starting mininet - sudo ./start-mn.sh with a topology of two hosts and 1 switch
Manually add arp entries from mininet console for h1 and h2 - h1 arp -s 10.0.0.2 aa:bb:cc:dd:ee:ff
2. We can add entries into switch in two ways either P4runtime console which is python shell or via controller file directly lets see the first one
Reference link - https://github.com/p4lang/p4runtime-shell
Note: point the right artifacts of mri while loading P4runtime console which will inject basic info to the mininet topology and query the tables of MRI
```
docker run -it --rm \
  -v $PWD/cfg:/tmp/cfg \
  p4lang/p4runtime-sh \
  --grpc-addr 172.17.0.2:50001 \
  --device-id 1 --election-id 0,1 \
  --config /tmp/cfg/mri.p4.p4info.txt,/tmp/cfg/mri.json
  ```

#### Control plane

3. Using controller file

```
import p4runtime_sh.shell as sh
# you can omit the config argument if the switch is already configured with the
# correct P4 dataplane.
sh.setup(device_id=1,grpc_addr='172.17.0.2:50001',election_id=(1,0), config=sh.FwdPipeConfig('/tmp/cfg/mri.p4.p4info.txt', '/tmp/cfg/mri.json'))
# see p4runtime_sh/test.py for more examples
te = sh.TableEntry("MyEgress.swtrace")(action ="MyEgress.add_swtrace");
te.action["swid"] = ("1");
te.insert();
te = sh.TableEntry("MyIngress.ipv4_lpm")(action ="MyIngress.ipv4_forward");
te.match["hdr.ipv4.dstAddr"] = ("10.0.0.1");
te.action["dstAddr"] = ("ea:8c:e6:f0:e2:b3");
te.action["port"] = ("1");
te.insert();
te = sh.TableEntry("MyIngress.ipv4_lpm")(action ="MyIngress.ipv4_forward");
te.match["hdr.ipv4.dstAddr"] = ("10.0.0.2");
te.action["dstAddr"] = ("8e:f1:fc:dc:64:05");
te.action["port"] = ("2");
te.insert();
# ...
sh.teardown()
```
Run ``python ./controller.py``
which will connect to switch and push entries into the table

4. Hosts H1 & H2 will contain Send.py and Receive.py which are used to send and capture packets which contain MRI options like Eth,IP header along with Qdeapth etcand can be monitored from receive.py this value keeps changing based on traffic congestion over switch path
6. This whole topology is can be monitored from ONOS(SDN) controller  by connecting the topology