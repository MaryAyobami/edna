"""Profile for Edna, running Ubuntu 20.04

Instructions:
See https://github.com/MaryAyobami/edna/blob/cloudlab-repro-fixes/README.md

This profile no longer attaches an image-backed dataset to /data: that
dataset lived in a different CloudLab project than most experiments run
under, which made the blockstore silently come up unformatted instead of
failing outright. /data is now a plain sized blockstore, which Emulab
formats and mounts automatically regardless of which project you're in.

Node type is a dropdown so the same profile can be reused across a
hardware-generation sweep without editing this file each time.
"""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Node types used for the hardware-generation sweep. CloudLab resolves each
# hardware type to its owning cluster automatically (Utah, Wisconsin, or
# Clemson here), so a single dropdown can span clusters.
NODE_TYPES = [
    ("c8220", "c8220 (Clemson, 2013 Ivy Bridge, 20c/40t, 256GB, HDD)"),
    ("c220g5", "c220g5 (Wisconsin, 2017 Skylake, 20c/40t, 192GB, SSD+HDD)"),
    ("c6420", "c6420 (Clemson, 2017 Skylake, 32c/64t, 384GB, HDD)"),
    ("c6525-25g", "c6525-25g (Utah, 2019-21 Rome, 16c/32t, 128GB, SSD)"),
    ("c6620", "c6620 (Utah, 2025 Emerald Rapids, 28c/56t, 128GB, NVMe)"),
]

pc.defineParameter("NODE_TYPE", "Node type",
                    portal.ParameterType.NODETYPE, NODE_TYPES[0],
                    NODE_TYPES,
                    longDescription="Hardware to allocate. Pick one node "
                    "per run for the hardware-generation sweep.")
pc.defineParameter("MPOINT", "Mountpoint for file system",
                    portal.ParameterType.STRING, "/data")
pc.defineParameter("BS_SIZE", "Blockstore size (GB)",
                    portal.ParameterType.INTEGER, 100)

params = pc.bindParameters()

node = request.RawPC("mynode")
node.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU20-64-STD'
node.hardware_type = params.NODE_TYPE

# add the blockstore: plain sized blockstore, no dataset attachment, so it
# is always formatted/mounted regardless of which project you're running in
bs = node.Blockstore("bs", params.MPOINT)
bs.size = str(params.BS_SIZE) + "GB"

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
