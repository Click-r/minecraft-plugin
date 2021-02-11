import os
import json

parsed = {"groupid": "", "artifactid": "", "version": "", "name": "", "new directory": "", "plugin name": ""}

subname = lambda name: f"\\{name}"

def init():
    """
    Does all important things that need to be done first
    """
    
    create = __file__.replace('\\main\\' + __file__.split('\\')[-1], '\\output\\')
    newdir(create)
    
    listForm = list(parsed)
    i = 0

    while i != len(parsed):
        setting = listForm[i]
        arg = input(f"enter value for {setting}: ")
        parsed[setting] = arg
        i += 1

    try:
        parsed["java.home"] = os.environ.get("JAVA_HOME")
    except OSError:
        print("could not find the JAVA_HOME environment variable")

    global pom_content
    pom_content = ""

    with open("content.txt", "r") as f:
        lines = f.readlines()
        pom_content = ''.join(lines).format(groupid = parsed['groupid'], artifactid = parsed['artifactid'], version = parsed['version'])

    return 1

def newdir(path):
    """
    Creates a new directory
    """
    
    try:
        os.mkdir(path)
        print(f"created directory {path}")
    except OSError:
        print(f"{path} already exists")
        return 0
    return path

def putfile(name, directory):
    """
    Puts a file into a separate directory.
    """
    
    currdir = __file__
    fileDir = currdir.replace(currdir.split('/')[-1], name)
    os.rename(fileDir, directory + subname(name))
    
    print(f"put {name} into {directory}")
    
    return directory

def configWorkspace():
    """
    Writes the workspace file necessary in vscode
    """

    nd = __file__.replace('\\main\\' + __file__.split('\\')[-1], '\\output\\' + parsed["new directory"])
    
    if newdir(nd):
        name = "default.code-workspace"
        
        with open(name,"x") as wspace:
            
            wspace.write(json.dumps({
                "folders":[
                    {
                        "path": "."
                    }
                ],
                "settings": {
                        "files.autoGuessEncoding": True,
                        "files.encoding": "utf8",
                        "java.home": parsed["java.home"],
                        "java.jdt.ls.vmargs": "-Dfile.encoding=UTF-8",
                        "javac-linter.javac": "javac -Dfile.encoding=UTF-8"
                    }
                
                }
            ))

        return putfile(name, nd)
    else:
        return 0

def pom_xml(directory):
    """
    Writes necessary xml data into a pom.xml file
    """
    
    name = "pom.xml"

    with open(name, "x") as xmlp:
        xmlp.write(pom_content)

    return putfile(name, directory)

def makeFolders(directory, name):
    """
    Sets up the necessary folders
    """
    
    maindir = directory + subname(name)
    newdir(maindir)

    targetdir = newdir(maindir + subname("target"))
    
    srcmain = newdir(maindir + subname("src"))
    srcmain = newdir(srcmain + subname("main"))
    
    sourcedir = newdir(srcmain + subname("java"))
    sourcedir = newdir(sourcedir + subname(name))

    resources = newdir(srcmain + subname("resources"))

    return {"maindir": maindir, "target": targetdir, "srcmain": srcmain, "sourcedir": sourcedir, "resources": resources}

def setupYAML(directory):
    """
    Writes needed data to a YAML file
    """
    
    name = "plugin.yml"
    
    with open(name, "x") as yml:
        yml.write(f"main: {parsed['plugin name']}.App\nname: {parsed['name']}\nversion: {parsed['version']}")

    return putfile(name, directory)

if __name__ == "__main__":
    if init():
        workspace = configWorkspace()
        directories = makeFolders(workspace, parsed["plugin name"])
        pom = pom_xml(directories["maindir"])
        yaml = setupYAML(directories["resources"])
        
        print(f"\n\nSucessfully setup! You can find the template in output.\nPlease create a java file named App in the java\{parsed['plugin name']}\ directory.\nClick on the Maven Projects pane, right click your plugin and select 'install' from the menu.\nBe sure to download maven as it is needed for the process.\n")
        print("From here, follow the tutorial over at https://www.spigotmc.org/wiki/creating-a-blank-spigot-plugin-in-vs-code/ from the 'Create blank plugin' step of the tutorial. Happy developing!")
