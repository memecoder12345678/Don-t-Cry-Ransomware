import os
from libc.stdlib cimport malloc, free
from libc.stdio cimport FILE, fopen, fread, fwrite, fclose, remove

from colorama import Fore
from Crypto.Cipher import AES

def decrypt_file(str path, bytes key, int chunk_size=268435456):
    cdef:
        bytes MAGIC = b"DCRY$"
        str decrypted_path = os.path.splitext(path)[0]
        FILE *f_in = fopen(path.encode(), "rb")
        FILE *f_out = fopen(decrypted_path.encode(), "wb")
        char *nonce = <char *>malloc(12)
        char *tag = <char *>malloc(16)
        char *buffer = <char *>malloc(chunk_size)
        char *magic_buffer = <char *>malloc(len(MAGIC))
        size_t read_size
        const unsigned char[:] decrypted_view
    success = False
    if not f_in or not f_out:
        print(f"{Fore.LIGHTRED_EX}Error opening file: {path}")
        return
    try:
        if fread(magic_buffer, 1, len(MAGIC), f_in) != len(MAGIC):
            print(f"{Fore.LIGHTRED_EX}File corrupted - Invalid header: {path}")
            return
        if bytes(magic_buffer[: len(MAGIC)]) != MAGIC:
            print(f"{Fore.LIGHTRED_EX}Invalid file format: {path}")
            return
        while True:
            if fread(nonce, 1, 12, f_in) != 12:
                break
            if fread(tag, 1, 16, f_in) != 16:
                print(f"{Fore.LIGHTRED_EX}File corrupted - Missing tag: {path}")
                return
            read_size = fread(buffer, 1, chunk_size, f_in)
            if read_size == 0:
                print(f"{Fore.LIGHTRED_EX}File corrupted - Missing encrypted data: {path}")
                return
            cipher = AES.new(key, AES.MODE_GCM, nonce=bytes(nonce[:12]))
            try:
                decrypted_chunk = cipher.decrypt_and_verify(
                    bytes(buffer[:read_size]), bytes(tag[:16])
                )
                decrypted_view = decrypted_chunk
                fwrite(
                    <const char *> &decrypted_view[0],
                    1,
                    len(decrypted_chunk),
                    f_out,
                )
            except ValueError:
                print(
                    f"{Fore.LIGHTRED_EX}Authentication failed for {path} - File may be tampered!"
                )
                return
        success = True
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}Error decrypting {path}: {e}")
    finally:
        if f_in:
            fclose(f_in)
        if f_out:
            fclose(f_out)
        if success:
            remove(path.encode())
        free(magic_buffer)
        free(nonce)
        free(tag)
        free(buffer)


def encrypt_file(str path, bytes key, int chunk_size=268435456):
    cdef:
        bytes MAGIC = b"DCRY$"
        str encrypted_path = path + ".dcry"
        FILE *f_in = fopen(path.encode(), "rb")
        FILE *f_out = fopen(encrypted_path.encode(), "wb")
        char *nonce = <char *>malloc(12)
        char *buffer = <char *>malloc(chunk_size)
        size_t read_size
        bytes nonce_bytes, encrypted_chunk, tag
        const unsigned char[:] encrypted_view
        const unsigned char[:] nonce_view
        const unsigned char[:] tag_view
    success = False
    if not f_in or not f_out:
        return
    try:
        fwrite(<char *>MAGIC, 1, len(MAGIC), f_out)
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
            fwrite(<char *> &nonce_view[0], 1, 12, f_out)
            fwrite(<char *> &tag_view[0], 1, 16, f_out)
            fwrite(<char *> &encrypted_view[0], 1, len(encrypted_chunk), f_out)
        success = True
    except Exception as e:
        print(f"Error encrypting {path}: {e}")
    finally:
        if f_in:
            fclose(f_in)
        if f_out:
            fclose(f_out)
        if success:
            remove(path.encode())
        free(nonce)
        free(buffer)
