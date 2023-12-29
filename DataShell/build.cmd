@ECHO off

@REM openssl genrsa -out key.pem 4096
@REM openssl pkcs8 -topk8 -inform PEM -outform DER -in key.pem -out key.der -nocrypt

@REM monkeyc -y resources/key.der -f monkey.jungle -o bin/DataShellApp.prg
@REM ECHO %1

IF "%1"=="sim" GOTO Simulator
GOTO Option1
:Simulator
ECHO "Simulator..."
connectiq

:Option1
IF "%1"=="all" GOTO Compile
IF "%1."=="." GOTO Compile
GOTO Option2
:Compile
ECHO "Compiling..."
monkeyc -o bin/DataShellApp.prg -y resources/key.der -m manifest.xml -z resources/strings.xml;resources/bitmaps.xml source/DataShellDelegate.mc source/DataShellView.mc source/DataShellApp.mc

:Option2
IF "%1"=="run" GOTO Execute
GOTO Finish
:Execute
ECHO "Running..."
@REM monkeydo bin/DataShellApp.prg edge1040
@REM monkeydo bin/DataShellApp.prg edge820
monkeydo bin/DataShellApp.prg fenix5x

:Finish
