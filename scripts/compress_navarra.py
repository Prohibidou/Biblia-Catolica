import gzip
import shutil

print("Compressing navarra.sqlite to navarra.sqlite.gz...")

with open('public/bibles/navarra.sqlite', 'rb') as f_in:
    with gzip.open('public/bibles/navarra.sqlite.gz', 'wb', compresslevel=9) as f_out:
        shutil.copyfileobj(f_in, f_out)

print("Done! File compressed.")

# Verify
import os
original_size = os.path.getsize('public/bibles/navarra.sqlite')
compressed_size = os.path.getsize('public/bibles/navarra.sqlite.gz')
ratio = (1 - compressed_size / original_size) * 100

print(f"Original: {original_size:,} bytes ({original_size/1024/1024:.2f} MB)")
print(f"Compressed: {compressed_size:,} bytes ({compressed_size/1024/1024:.2f} MB)")
print(f"Compression ratio: {ratio:.1f}%")
