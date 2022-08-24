# save cwd
$mwd=(Get-Item -Path '.\' -Verbose).FullName

# change to script local
cd $PSScriptRoot/java_trash
# make jar
javac Prog.java
py CreateManifest.py Prog
jar cmf Prog.mf Prog.jar Prog.class Logic.class

# change back cwd
cd $mwd
# run it (stdin and stdout are automatically redirected)
java -jar $PSScriptRoot/java_trash/Prog.jar