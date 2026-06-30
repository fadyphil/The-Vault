# Memory Hardening & Secure Memory Management

In a zero-trust Secrets Manager like **The Vault**, securing data at rest in the database is only half the battle. If an attacker can dump the physical RAM of the host machine or read OS swap files, they may recover sensitive API keys, database credentials, or even the primary `MASTER_KEY`.

This document explores **three memory vulnerabilities** specific to systems like ours and details **mitigations** you can apply to make memory storage bulletproof.

---

## ⚠️ The Vulnerabilities

### 1. OS Swap File Leakage (Swap Spillage)

When a server runs low on physical RAM, the operating system's Virtual Memory Manager swaps pages of memory out to a swap file on the disk (e.g., `/var/swap` on Linux, `pagefile.sys` on Windows).

* **The Risk:** If a page containing the plaintext `MASTER_KEY` or a decrypted secret is swapped to disk, it is written in **plaintext** to non-volatile storage. Even if the server shuts down or the process terminates, the secret remains on the physical disk block, bypassing all database encryption.

### 2. Go Garbage Collection & Array Copies

Go is a garbage-collected language. Unlike C or Rust, memory is managed automatically, which introduces subtle leakage patterns:

* **String Immutability:** Go `string` objects are immutable. If you cast a `[]byte` containing a secret to a `string`, Go allocates new memory. You cannot clear or overwrite a `string` in memory; it remains in the heap until the Garbage Collector decides to sweep it.
* **Slice Reallocation Copies:** If you expand a byte slice (e.g., using `append(secret, byte)`) and it exceeds its capacity, Go allocates a new, larger backing array, copies the data over, and leaves the old array in unreferenced memory. The secret now exists in *two* places in RAM.

---

## 🛡️ Cryptographic Mitigations

To protect secrets in memory, we implement a defense-in-depth hierarchy:

### Tier 1: Explicit Zeroing (Scrubbing)

Never use strings for sensitive keys or plaintexts. Always use byte slices (`[]byte`) and explicitly overwrite the slice with zeroes (`0`) immediately after sealing or returning the data:

```go
func Scrub(b []byte) {
    for i := range b {
        b[i] = 0
    }
}
```

### Tier 2: RAM Locking (`mlock` Syscall)

To prevent the OS from ever swapping sensitive keys from RAM to disk, use the `mlock` system call. This instructs the OS kernel to pin the specified memory pages in physical RAM.

In Go, this is done via the `syscall` package:

```go
import "syscall"

// LockMemory pins a byte slice in RAM, preventing it from being swapped to disk.
func LockMemory(data []byte) error {
    return syscall.Mlock(data)
}

// UnlockMemory releases the lock.
func UnlockMemory(data []byte) error {
    return syscall.Munlock(data)
}
```

### Tier 3: Guard Pages & Sealed Heaps

For enterprise-grade security, avoid the default Go allocator for the Master Key. Instead, allocate memory pages directly from the OS (using `mmap`) and place guard pages around them:

1. **No-Read/No-Write Guard Pages:** Allocate page boundaries before and after the secret page with protection flag `PROT_NONE`. If the process attempts a buffer overrun (like Heartbleed), it immediately triggers a kernel-level Segmentation Fault (`SIGSEGV`) instead of reading the key.
2. **Third-party secure heaps:** In production Go systems, developers use libraries like **`awnumar/memguard`** which automate locking memory, zeroing buffers on interrupt signals, and applying guard pages.
