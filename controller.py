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
te.action["dstAddr"] = ("9a:96:b1:20:bf:84");
te.action["port"] = ("1");
te.insert();


te = sh.TableEntry("MyIngress.ipv4_lpm")(action ="MyIngress.ipv4_forward");
te.match["hdr.ipv4.dstAddr"] = ("10.0.0.2");
te.action["dstAddr"] = ("de:cb:66:ce:75:8e");
te.action["port"] = ("2");
te.insert();
# ...

sh.teardown()
