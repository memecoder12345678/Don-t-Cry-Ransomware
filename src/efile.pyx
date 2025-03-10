from libc.stdlib cimport malloc, free
from libc.stdio cimport FILE, fopen, fread, fwrite, fclose, remove
from libc.string cimport memcpy
from Crypto.Cipher import AES
import os

def encrypt_file(str path, bytes key, int chunk_size=268435456):
    cdef:
        bytes MAGIC = b"DCRY$"
        str encrypted_path = path + ".dcry"
        FILE* f_in = fopen(path.encode(), "rb")
        FILE* f_out = fopen(encrypted_path.encode(), "wb")
        char* nonce = <char*> malloc(12)
        char* buffer = <char*> malloc(chunk_size)
        size_t read_size
        bytes nonce_bytes, encrypted_chunk, tag
        const unsigned char[:] encrypted_view
        const unsigned char[:] nonce_view
        const unsigned char[:] tag_view
    if not f_in or not f_out:
        return
    try:
        fwrite(<char*>MAGIC, 1, len(MAGIC), f_out)
        while True:
            read_size = fread(buffer, 1, chunk_size, f_in)
            if read_size == 0:
                break
            nonce_bytes = os.urandom(12)
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce_bytes)
            encrypted_chunk, tag = cipher.encrypt_and_digest(bytes(buffer[:read_size]))
            nonce_view = nonce_bytes
            tag_view = tag
            encrypted_view = encrypted_chunk
            fwrite(<char*>&nonce_view[0], 1, 12, f_out)
            fwrite(<char*>&tag_view[0], 1, 16, f_out)
            fwrite(<char*>&encrypted_view[0], 1, len(encrypted_chunk), f_out)
        fclose(f_in)
        fclose(f_out)
        remove(path.encode())
    except Exception as e:
        print(f"Error encrypting {path}: {e}")
    finally:
        free(nonce)
        free(buffer)