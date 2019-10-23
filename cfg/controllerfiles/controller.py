import p4runtime_sh.shell as sh

# you can omit the config argument if the switch is already configured with the
# correct P4 dataplane.
sh.setup(device_id=1,grpc_addr='172.17.0.2:50001',election_id=(1,0), config=sh.FwdPipeConfig('mri.p4.p4info.txt', 'mri.json'))

# see p4runtime_sh/test.py for more examples
te = table_entry["MyEgress.swtrace"](action ="MyEgress.add_swtrace");
te.action["swid"] = ("1");
te.insert();

te = table_entry["MyIngress.ipv4_lpm"](action ="MyIngress.ipv4_forward");
te.match["hdr.ipv4.dstAddr"] = ("10.0.0.1");
te.action["dstAddr"] = ("7a:da:30:9f:7b:a2");
te.action["port"] = ("1");
te.insert();


te = table_entry["MyIngress.ipv4_lpm"](action ="MyIngress.ipv4_forward");
te.match["hdr.ipv4.dstAddr"] = ("10.0.0.2");
te.action["dstAddr"] = ("f6:4e:94:ee:0d:cd");
te.action["port"] = ("2");
te.insert();
# ...

sh.teardown()
