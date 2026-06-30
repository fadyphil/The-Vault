# ADR-0001: Enforce Memory Scrubbing and RAM Locking for Plaintext Secrets

* **Status**: Accepted
* **Date**: 2026-06-29
* **Author(s)**: fadyphil
* **Deciders**: fadyphil

---

## 1. Context and Problem Statement

As a zero-trust Secrets Manager, The Vault processes highly sensitive cryptographic keys (including the Master Key) and plaintext user secrets in memory. Because Go is a garbage-collected language with mutable heap variables, unmanaged byte slices can linger in physical memory indefinitely, and physical RAM pages containing sensitive data can be swapped to disk in plaintext. We need a standard to prevent key leakage via RAM dumps or OS swap file spillage.

## 2. Decision Drivers

* **Security Compliance**: Absolute prevention of plaintext secret leakage to non-volatile disks.
* **Performance Overhead**: Key locking syscalls should not degrade REST API throughput.
* **Portability**: System calls like `mlock` are OS-specific (POSIX/Linux) and require fallback handling on non-POSIX platforms.

## 3. Considered Options

### Option A: Standard Go Memory Allocations

* **Description**: Let Go's default memory allocator manage strings and byte slices for keys and plaintexts.
* **Pros**: Zero code complexity; cross-platform compatible out of the box.
* **Cons**: Secrets are copied implicitly during GC and slice expansion; keys can leak to swap partitions.

### Option B: Ephemeral Byte Slices with Explicit Zeroing (Scrubbing)

* **Description**: Exclusively use `[]byte` (never `string`) for secrets, and manually overwrite bytes with `0` immediately after encryption/decryption.
* **Pros**: Protects against lingering heap pointers; works on all operating systems without elevated privileges.
* **Cons**: Does not prevent the OS from swapping RAM pages containing the secret to disk while the process is running.

### Option C: Explicit Scrubbing + RAM Locking (`mlock`)

* **Description**: Combine Option B with platform-specific `syscall.Mlock` calls to pin memory blocks in physical RAM, with standard Go fallbacks for unsupported platforms.
* **Pros**: Full mitigation against both heap retention and OS swap spillage.
* **Cons**: Higher implementation complexity; potential resource limit constraints on locking memory size.

## 4. Decision Outcome

Chosen Option: **Option C: Explicit Scrubbing + RAM Locking (`mlock`)**

### Rationale

Option C satisfies our zero-trust threat model. Manual byte-scrubbing clears memory references in the Go runtime, while `mlock` guarantees that active pages are never written to disk in plaintext.

---

## 5. Consequences

* **✅ Positive Impact (Benefits)**:
  * Secrets are safe from swap file inspection.
  * Reduced lifetime of plaintext byte slices in memory.
* **❌ Negative Impact (Drawbacks/Risks)**:
  * We must carefully manage array capacities to avoid implicit copies during slice resizing.
  * Operating system constraints (e.g. `ulimit -l` on Linux) limit the amount of memory a non-root process can lock.
* **⚠️ Technical Debt/Future Actions**:
  * Implement a robust fallback wrapper that logs a warning if `mlock` fails due to permissions, instead of crashing the server.

## 6. Compliance and Verification

* Verification is done via code-review checklists in the pull request template.
* We can write unit tests that assert sensitive memory regions are cleared after function termination.
