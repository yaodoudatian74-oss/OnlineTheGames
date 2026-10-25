#!/bin/bash
set -e
BT=/opt/android/build-tools/34.0.0
AJ=/opt/android/platforms/android-34/android.jar
cd /home/claude/apk
rm -rf out && mkdir -p out/classes out/dex
cp /home/claude/island/local.html assets/index.html
$BT/aapt2 compile --dir res -o out/res.zip
$BT/aapt2 link -o out/base.apk -I $AJ --manifest AndroidManifest.xml -A assets out/res.zip --min-sdk-version 24 --target-sdk-version 34 --version-code 1 --version-name 1.0 --java out/gen
javac -source 8 -target 8 -bootclasspath $AJ -cp $AJ -d out/classes $(find src out/gen -name '*.java') 2>&1 | grep -v "warning\|^Note\|bootstrap" || true
$BT/d8 --release --min-api 24 --lib $AJ --output out/dex $(find out/classes -name '*.class')
cp out/base.apk out/unsigned.apk
(cd out/dex && zip -q ../unsigned.apk classes.dex)
$BT/zipalign -f -p 4 out/unsigned.apk out/aligned.apk
[ -f release.keystore ] || keytool -genkeypair -keystore release.keystore -storepass islandpass -keypass islandpass -alias island -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=Island Survival, O=Claude Games, C=JP" >/dev/null 2>&1
$BT/apksigner sign --ks release.keystore --ks-pass pass:islandpass --key-pass pass:islandpass --ks-key-alias island --out out/island-survival.apk out/aligned.apk
$BT/apksigner verify --print-certs out/island-survival.apk | head -3
ls -la out/island-survival.apk
