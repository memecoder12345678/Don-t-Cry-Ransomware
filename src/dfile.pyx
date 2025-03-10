from libc.stdlib cimport malloc, free
from libc.stdio cimport FILE, fopen, fread, fwrite, fclose, remove
from Crypto.Cipher import AES
import os
from colorama import Fore

def decrypt_file(str path, bytes key, int chunk_size=268435456):
    cdef:
        bytes MAGIC = b"DCRY$"
        str decrypted_path = os.path.splitext(path)[0]
        FILE* f_in = fopen(path.encode(), "rb")
        FILE* f_out = fopen(decrypted_path.encode(), "wb")
        char* nonce = <char*> malloc(12)
        char* tag = <char*> malloc(16)
        char* buffer = <char*> malloc(chunk_size)
        char* magic_buffer = <char*> malloc(len(MAGIC))
        size_t read_size
        const unsigned char[:] decrypted_view
    if not f_in or not f_out:
        print(f"{Fore.LIGHTRED_EX}Error opening file: {path}")
        return
    try:
        if fread(magic_buffer, 1, len(MAGIC), f_in) != len(MAGIC):
            print(f"{Fore.LIGHTRED_EX}File corrupted - Invalid header: {path}")
            return
        if bytes(magic_buffer[:len(MAGIC)]) != MAGIC:
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
                decrypted_chunk = cipher.decrypt_and_verify(bytes(buffer[:read_size]), bytes(tag[:16]))
                decrypted_view = decrypted_chunk
                fwrite(<const char*>&decrypted_view[0], 1, len(decrypted_chunk), f_out)
            except ValueError:
                print(f"{Fore.LIGHTRED_EX}Authentication failed for {path} - File may be tampered!")
                return
        fclose(f_in)
        fclose(f_out)
        remove(path.encode())
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}Error decrypting {path}: {e}")
    finally:
        free(magic_buffer)
        free(nonce)
        free(tag)
        free(buffer)
