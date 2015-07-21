This an exploit for CVE-2015-2426 (MS-078), a Windows kernel local privilege escalation 0day from the Hacking Team archive (email [here](https://wikileaks.org/hackingteam/emails/emailid/974752)). It was developed by Eugene Ching / Qavar security. Original contents below:

Summary.
======== 

Windows kernel memory corruption exploit leading to privilege escalation.

Tested on Windows 8.1 fully-patched (as of 28 Jan 2015).

Also tested to work against:

  * Google Chrome, up to v40.0.2214.93 (64-bit); and  
  * Google Chrome Canary, up to v42.0.2290.6 canary (64-bit)  

assuming a suitable RCE in Chrome (simulated via injecting a thread into 
Chrome)


Main exploit code.
==================

The main exploit is implemented in `PIC.c`, which is provided as part of a
Visual Studio 2013 Express solution.

Building the solution would produce `PIC.exe`.


Exploit "raw bytes".
====================

We ultimately want to inject the exploit into the target's memory, and directly
run it. In order to do that, we need to inject only the relevant instructions
(opcodes) and the necessary data.

Hence, we extract the code segment (the opcodes) from `PIC.exe`, and append the
necessary data (the malformed font, `font-data.bin`) into a sequence of  bytes.

This produces the "raw bytes" that we can directly inject into the target and
call `CreateRemoteThread()` on.

This process is automated through the Python script named `make-raw-bytes.py`.
The output is `raw-bytes.bin`.


Injection into target.
======================

To convert the "raw bytes" into an .exe that actually injects the "raw bytes"
into a target, we need to call `WriteProcessMemory()` & `CreateRemoteThread()`.

This process is handled by `make-injector-cpp.py`. The output is
`injector.cpp`, a piece of code which, when compiled, takes a target PID and
executes the exploit.


Convenience wrapper.
====================

As a convenience, `make.bat` will produce `injector.exe` directly by performing
the steps described above.

In other words, `make.bat` will:
  - make-raw-bytes.py
  - make-injector-cpp.py
  - build injector.exe
