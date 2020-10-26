import os, sys, socket, shutil
from colorama import init, Fore
init(autoreset=True)

def pm(args):
	arguments = args.split(" ")
	if len(arguments) < 1:
		print("Invalid arguments")
		print("Usage: pm [install/list/uninstall] [url/name] [name]")
		print("\tpm install https://example.com/plugin.py exampleplugin")
		print("\tpm uninstall exampleplugin")
		print("\tpm list")
		return
    
	import os
	from urllib.request import urlretrieve as downloadFile
	if arguments[0] == "install":
		if len(arguments) != 3:
			print("Invalid arguments")
			print("Usage: pm [install/list/uninstall] [url/name] [name]")
			print("\tpm install https://example.com/plugin.py exampleplugin")
			print("\tpm uninstall exampleplugin")
			print("\tpm list")
			return

		try:
			print("Downloading plugin...")
			downloadFile(arguments[1], "plugins/" + arguments[2] + ".py")
			print("Importing...")
			exec("from plugins." + arguments[2].replace(".py", "") + " import *")
			print("Successfully installed", arguments[1], "as", arguments[2])
		except Exception as error:
			print("Failed to install", arguments[1])
			print(str(error))
	elif arguments[0] == "list":
		print("Currently installed plugins")
		pluginsList = os.listdir("plugins")
		for plugin in pluginsList:
			if plugin.lower().endswith(".py"):
				print("\t>", plugin)
	elif arguments[0] == "uninstall":
		if len(arguments) < 1:
			print("Invalid arguments")
			print("Usage: pm [install/list/uninstall] [url/name] [name]")
			print("\tpm install https://example.com/plugin.py exampleplugin")
			print("\tpm uninstall exampleplugin")
			print("\tpm list")
			return
        
		if not os.path.exists("plugins/" + arguments[1] + ".py"):
			print("Invalid plugin name of", arguments[1] + ".py")
			return

		try:
			os.remove("plugins/" + arguments[1] + ".py")
		except:
			print("Failed to uninstall", arguments[1])
			return

		print("Successfully uninstalled", arguments[1])
		print("Restart the shell to completely remove its commands")
	else:
		print("Invalid arguments")
		print("Usage: pm [install/list/uninstall] [url/name] [name]")
		print("\tpm install https://example.com/plugin.py exampleplugin")
		print("\tpm uninstall exampleplugin")
		print("\tpm list")

def shell(args):
	try:
		os.system(args)
	except Exception as error:
		print("Command failed with error:", str(error))

def cd(args):
    if not os.path.exists(args):
        print("Could not locate:", args)
        return
    os.chdir(args)

def helpMenu(args):
	def parseFile(file):
		with open(file) as f:
			linesList = f.read().splitlines()
		functions = []
		for line in linesList:
			if line.lower().startswith("def"):
				functions.append(line.split("def ")[1].split("(")[0])
		return functions

	print("Defined functions in", args)

	parsedFunctions = None
	if os.path.exists(args + ".py"):
		parsedFunctions = parseFile(args + ".py")
	if os.path.exists("plugins/" + args + ".py"):
		parsedFunctions = parseFile("plugins/" + args + ".py")
	
	if args.lower() == "help":
		parsedFunctions = parseFile("main.py")
	elif not parsedFunctions:
		print("No plugin or main function called:", args)
		return
	
	num = 0
	string = "\t"
	for func in parsedFunctions:
		if num > 4:
			print(string)
			num = 0
			string = "\t"
		string += func + "   "
		num += 1
	print(string)


def exit(args):
    print("Closing Shell...")
    sys.exit(0)

def header(pluginNumber):
    print(Fore.LIGHTWHITE_EX + "PyTerminal v0.1 - IWick Development 2020")
    print(Fore.MAGENTA + "Loaded", str(pluginNumber), Fore.MAGENTA + "plugins")
    print("")

plugNum = 0

if not os.path.exists("plugins"):
    os.mkdir("plugins")
else:
    if os.path.exists("plugins/__pycache__"):
        try:
            shutil.rmtree("plugins/__pycache__")
        except:
            pass
    plugins = os.listdir("plugins")
    for plugin in plugins:
        if plugin.lower().endswith(".py"):
            exec("from plugins." + plugin.replace(".py", "") + " import *")
            plugNum += 1

header(plugNum)

while True:
	command = input(Fore.GREEN + 
	os.getlogin() + 
	Fore.WHITE +"@" + 
	Fore.BLUE + socket.gethostname() + 
	Fore.WHITE +":" + 
	Fore.YELLOW + 
	os.getcwd() + 
	Fore.LIGHTCYAN_EX + 
	"$ " + Fore.RESET).split(" ", 1)

	try:
		if command[0].lower() == "help":
			helpMenu(command[-1])
		else:
			expression = command[0] + "('" + command[-1].replace("\\", "/") + "')"
			eval(expression)
	except NameError:
		print("Undefined command [ " + command[0] + " ]")
	except Exception as error:
		print(str(error))
	print("")
