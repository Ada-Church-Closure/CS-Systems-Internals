This repository collects systems- and security-focused coursework and my own notes/projects from well-known university classes.

------

1. [CMU CS15213: CSAPP](https://csapp.cs.cmu.edu) (2025.3-2025.6)
- Focus: linking and the ELF toolchain, x86-64 calling conventions, C memory model, cache behavior.
- Labs: bomblab (control flow, disassembly), cachelab (locality, miss analysis), malloclab (allocator with free lists/coalescing).
- Tools: gdb, objdump, readelf, nm, valgrind; emphasis on debugging and basic performance profiling.

2. [CS61A: Structure and Interpretation of Computer Programs](https://insideempire.github.io/CS61A-Website-Archive/) (2025.6-2025.8)
- Project: Scheme interpreter (parsing, eval/apply, lexical scoping) in Python.
- Takeaway: concept-heavy, light on debugging; good for building foundations in abstraction and interpreter design.
- Ref: 2024 archived site; Chinese handbook: https://composingprograms.netlify.app (I contributed minor fixes).

3. [MIT 6.S081 Operating System Engineering](https://pdos.csail.mit.edu/6.828/2021/schedule.html) (2025.9-2025.11, ~90%)
- Topics: processes, syscalls, traps/interrupts, page tables and virtual memory, file system, scheduling, synchronization.
- Work: xv6 labs (syscall extensions, virtual memory and page-fault handling, copy-on-write, simple file-system changes, basic concurrency).
- Note: small codebase but conceptually deep; solo debugging can be challenging. I plan to revisit the papers and remaining topics.
