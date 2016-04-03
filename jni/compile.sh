mkdir ../target
mkdir ../target/classes
mkdir ../target/classes/resources
mkdir ../target/classes/resources/include
mkdir ../target/classes/resources/lib
mkdir ../target/classes/resources/src
mkdir ../target/classes/resources/build
mkdir ../target/classes/resources/build/opt
mkdir ../target/classes/resources/build/opt/src
mkdir ../target/classes/resources/build/opt/src/backends
mkdir ../target/classes/resources/build/opt/src/parsers
mkdir ../target/classes/com
mkdir ../target/classes/com/upstandinghackers
mkdir ../target/classes/com/upstandinghackers/hammer
cp libjhammer.so ../target/classes/resources/libjhammer.so
cp jhammer.h ../target/classes/resources/jhammer.h
cp ../common.mk ../target/classes/resources/common.mk
cp ../config.mk ../target/classes/resources/config.mk
cp -r com/upstandinghackers/hammer/*.class ../target/classes/com/upstandinghackers/hammer/
cp ../src/*.h ../target/classes/resources/include/
cp ../lib/*.c ../target/classes/resources/src/
cp ../lib/hush ../target/classes/resources/lib/
cp ../build/opt/src/*.os ../target/classes/resources/build/opt/src
cp ../build/opt/src/backends/*.os ../target/classes/resources/build/opt/src/backends
cp ../build/opt/src/parsers/*.os ../target/classes/resources/build/opt/src/parsers
