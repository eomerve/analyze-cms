
from pathlib import Path
import re
import struct

data = Path("cms_raw.bin").read_bytes()

positions = [
    m.start()
    for m in re.finditer(b"QCMS", data)
]

output = Path("packets")
output.mkdir(mode=0o700, exist_ok=True)

print("Total bytes:", len(data))
print("QCMS headers:", len(positions))
print("-" * 60)

for i, start in enumerate(positions):

    if i + 1 < len(positions):
        end = positions[i + 1]
        status = "candidate frame"
    else:
        end = len(data)
        status = "last frame - unverified"

    packet = data[start:end]

    filename = output / f"packet_{i+1:03d}.bin"
    filename.write_bytes(packet)

    print(f"\nPacket: {i+1}")
    print(f"Offset: {start}")
    print(f"Length: {len(packet)}")
    print(f"Status: {status}")
    print("Header:", packet[:24].hex(" "))

    if len(packet) >= 8:
        value = struct.unpack_from("<I", packet, 4)[0]
        print("Header field at byte 4:", value)

print("\nPackets saved.")