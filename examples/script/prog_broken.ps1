$mwd=(Get-Item -Path '.\' -Verbose).FullName

cd $PSScriptRoot/java_trash
javac ProgBroken.java
py CreateManifest.py ProgBroken
jar cmf ProgBroken.mf ProgBroken.jar ProgBroken.class Logic.class

cd $mwd
java -jar $PSScriptRoot/java_trash/ProgBroken.jar