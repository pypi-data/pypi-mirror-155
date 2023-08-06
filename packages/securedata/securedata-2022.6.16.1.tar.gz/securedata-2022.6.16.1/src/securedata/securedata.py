import os
import json
import pathlib
import logging
from sys import argv, exit, stdout
from datetime import date

initialized = False


def main():
    global PATH_SECUREDATA
    global PATH_LOG
    global PATH_CONFIG_FILE
    global SETTINGS
    global initialized
    SETTINGS = None

    if initialized:
        return

    # config file, stored within the package
    PATH_CONFIG_FILE = f'{pathlib.Path(__file__).resolve().parent}/config.json'

    # Determines where settings.json is stored; by default, this is ~/securedata
    PATH_SECUREDATA = os.path.expanduser(
        getConfigItem('path_securedata') or '~/securedata')

    # initialize settings file if it doesn't exist
    try:
        with open(f'{PATH_SECUREDATA}/settings.json', 'r+') as f:
            f.seek(0, os.SEEK_END)
    except:
        if not os.path.exists(PATH_SECUREDATA):
            os.makedirs(PATH_SECUREDATA)
        with open(f'{PATH_SECUREDATA}/settings.json', 'x+') as f:
            print(
                f"\n\nWarning: settings.json not found; created a blank one in {PATH_SECUREDATA}")
            print("You can change this location by calling 'securedata config'.\n\n")
            f.write('{}')

    try:
        SETTINGS = json.load(open(f'{PATH_SECUREDATA}/settings.json'))
    except json.decoder.JSONDecodeError as e:
        response = input(
            f"The settings file ({PATH_SECUREDATA}/settings.json) is not valid JSON. Do you want to replace it with an empty JSON file? (you will lose existing data) (y/n)\n")
        if(response.lower().startswith("y")):
            print("Backing up...")

            # for some reason, this only works when you call touch; TODO fix this
            os.system(
                f"touch {PATH_SECUREDATA}/settings-backup.json && cp {PATH_SECUREDATA}/settings.json {PATH_SECUREDATA}/settings-backup.json")
            print(f"Backed up to {PATH_SECUREDATA}/settings-backup.json")
            with open(f'{PATH_SECUREDATA}/settings.json', 'w+') as f:
                f.write('{}')
            print("Done. Please try your last command again.")
        else:
            print(
                f"OK. Please fix {PATH_SECUREDATA}/settings.json and try again.")

        exit(-1)

    PATH_LOG = getItem('path', 'log')
    if PATH_LOG == None:
        PATH_LOG = setItem(
            'path', 'log', f"{PATH_SECUREDATA}/log", fileName='settings.json')
        print(
            f"\n\nCalling securedata.log in Python will now write to {PATH_SECUREDATA}/log by default.")
        print(f"You can change this in {PATH_SECUREDATA}/settings.json.\n\n")
    if not os.path.exists(PATH_LOG):
        os.makedirs(PATH_LOG)
    if not PATH_LOG[-1] == '/':
        PATH_LOG += '/'

    initialized = True


"""
Edit and save a file using Vim
Allows for shortcuts by setting paths in settings.json -> path -> edit
settings.json -> path -> edit -> sync is reserved for the command to be run to sync files
"""


def editFile(path):

    pull_command = getItem("path", "edit", "sync-pull")
    if pull_command:
        print(f"Pulling {path} from cloud...")
        os.system(pull_command)
        print("Pulled.")

    # allows for shortcuts by setting paths in settings.json -> path -> edit
    if path in getItem("path", "edit"):
        path = getItem("path", "edit", path)

    if not os.path.exists(path):
        print(f"File does not exist: {path}")
        exit(-1)

    os.system(f"vim {path}")

    push_command = getItem("path", "edit", "sync-push")
    if push_command:
        print(f"Saving {path} to cloud...")
        os.system(push_command)
        print("Saved.")


def getItem(*attribute, warn=False):
    """
    Returns a property in settings.json.
    Usage: get('person', 'name')
    """

    global SETTINGS
    if SETTINGS == None:
        return None

    _settings = SETTINGS

    for index, item in enumerate(attribute):
        if item in _settings:
            _settings = _settings[item]
        elif attribute[1] != "edit":
            print(
                f"Warning: {item} not found in {_settings if index > 0 else f'{PATH_SECUREDATA}/settings.json'}")
            return None
        else:
            return None

    return _settings


def setItem(*attribute, value=None, fileName='settings.json'):
    """
    Sets a property in settings.json (or some other `fileName`).
    Usage: set('person', 'name', 'Tyler')
    The last argument is the value to set, unless value is specified.
    Returns the value set.
    """

    global SETTINGS
    secureFullPath = f"{PATH_SECUREDATA}/{fileName}"

    if(not value):
        value = attribute[-1]

    _settings = SETTINGS if fileName == 'settings.json' else json.load(
        open(secureFullPath))

    # iterate through entire JSON object and replace 2nd to last attribute with value

    partition = _settings
    for index, item in enumerate(attribute[:-1]):
        if item not in partition:
            partition[item] = value if index == len(attribute) - 2 else {}
            partition = partition[item]
            print(
                f"Warning: Adding new key '{item}' to {partition if index > 0 else secureFullPath}")
        else:
            if(index == len(attribute) - 2):
                partition[item] = value
            else:
                partition = partition[item]

    with open(secureFullPath, 'w+') as file:
        json.dump(_settings, file, indent=4)

    return value


def getFileAsArray(item, filePath=None, strip=True):
    """
    Returns the file as an array; strips using strip() unless strip is set to False
    """

    global PATH_LOG
    if(filePath == None):
        filePath = PATH_LOG
    elif(filePath == "notes"):
        filePath = getItem('path', 'notes', 'local')

        if(not filePath[-1] == '/'):
            filePath += '/'

        # pull from cloud
        try:
            os.system(
                f"rclone copy {getItem('path', 'notes', 'cloud')} {filePath}")
        except Exception as e:
            log(f"Could not pull Notes from cloud: {e}", level="error")

    try:
        content = open(filePath + item, "r").read()

        if strip is not False:
            content = content.strip()

        return content.split('\n')
    except Exception as e:
        log(f"getFileAsArray: {e}", level="error")
        return ""


def writeFile(fileName, filePath=None, content=None, append=False):
    """
    Writes a file to the specified path and creates subfolders if necessary
    """

    global PATH_LOG
    _filePath = filePath

    if filePath == None:
        filePath = PATH_LOG
    elif filePath == "notes":
        filePath = getItem('path', 'notes', 'local')

    if content == None:
        content = ""

    if not os.path.exists(filePath):
        os.makedirs(filePath)

    with open(filePath + "/" + fileName, 'w+' if not append else 'a+') as file:
        file.write(content)
        print(f"Wrote to '{filePath}/{fileName}'")

    # push to cloud
    if _filePath == "notes":
        try:
            os.system(
                f"rclone copy {filePath} {getItem('path', 'notes', 'cloud')}")
        except Exception as e:
            log(f"Could not sync Notes to cloud: {e}", level="error")


def getConfigItem(key=None):
    global PATH_CONFIG_FILE

    try:
        with open(PATH_CONFIG_FILE, 'r+') as file:
            return json.load(file)[key]
    except FileNotFoundError as e:
        if key == 'path_securedata':
            # set default settings.json and log path to ~/securedata
            setConfigItem(key, f"{pathlib.Path.home().resolve()}/securedata")
            return f"{pathlib.Path.home().resolve()}/securedata"
    except KeyError:
        print(f"Warning: Key error for key: {key}")
        return ""
    except json.decoder.JSONDecodeError as e:
        response = input(
            f"The config file ({PATH_CONFIG_FILE}) is not valid JSON. Do you want to replace it with an empty JSON file?  (you will lose existing data) (y/n)\n")
        if(response.lower().startswith("y")):
            with open(PATH_CONFIG_FILE, 'w+') as f:
                f.write('{}')
            print("Done. Please try your last command again.")
        else:
            print(f"OK. Please fix {PATH_CONFIG_FILE} and try again.")

        exit(-1)


def setConfigItem(key=None, value=None):
    """
    Updates the internal configuration file
    """

    global PATH_CONFIG_FILE

    if value == "":
        print("No changes were made.")
        exit(1)
    else:

        # error correction
        if(key == 'path_securedata' and value[0] != '/' and value[0] != '~'):
            value = f"/{value}"
        if(key == 'path_securedata' and value[-1] == '/'):
            value = f"{value[:-1]}"

        # warn about potential problems
        if(not os.path.exists(os.path.expanduser(value))):
            print(f"Warning: {value} is not a valid path.")
        if(value[0] == '~'):
            print("Warning: using tilde expansions may cause problems if using securedata for multiple users. It is recommended to use full paths.")

    try:
        with open(PATH_CONFIG_FILE, 'r+') as file:
            config = json.load(file)
    except FileNotFoundError:
        with open(PATH_CONFIG_FILE, 'x+') as f:
            print(f"Note: Could not find an existing config file... creating a new one.")
            f.write('{}')
            config = {}

    config[key] = value

    with open(PATH_CONFIG_FILE, 'w+') as file:
        json.dump(config, file, indent=4)

    print(f"\n\nUpdated configuration file ({PATH_CONFIG_FILE}).")
    print(f"{key} is now {value}\n")

    return value


def getLogger(logName=None, level=logging.INFO, filePath=None):
    """
    Returns a custom logger with the given name and level
    """

    today = str(date.today())

    if filePath == None:
        filePath = f"{PATH_LOG}{today}"
    if logName == None:
        logName = f"LOG_DAILY {today}"

    # create path if necessary
    if not os.path.exists(filePath):
        print(f"Creating {filePath}")
        os.makedirs(filePath)

    logger = logging.getLogger(logName)
    logger.setLevel(level)

    if logger.handlers:
        logger.handlers = []

    format_string = ("%(asctime)s — %(levelname)s — %(message)s")
    log_format = logging.Formatter(format_string)
    console_handler = logging.StreamHandler(stdout)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)
    file_handler = logging.FileHandler(f"{filePath}/{logName}.log", mode='a')
    file_handler.setFormatter(log_format)

    logger.addHandler(file_handler)
    return logger


def log(message=None, logName=None, level="info", filePath=None):

    if message == None:
        message = ""

    if level == None or level == "info":
        logger = getLogger(
            logName=logName, level=logging.INFO, filePath=filePath)
        logger.info(message)
    elif level == "debug":
        logger = getLogger(
            logName=logName, level=logging.DEBUG, filePath=filePath)
        logger.debug(message)
    elif level == "warn" or level == "warning":
        logger = getLogger(
            logName=logName, level=logging.WARN, filePath=filePath)
        logger.warning(message)
    elif level == "error":
        logger = getLogger(
            logName=logName, level=logging.ERROR, filePath=filePath)
        logger.error(message)
    elif level == "critical":
        logger = getLogger(
            logName=logName, level=logging.CRITICAL, filePath=filePath)
        logger.critical(message)
    else:
        logger = getLogger(
            logName=logName, level=logging.ERROR, filePath=filePath)
        logger.error(f"Unknown log level: {level}; using ERROR")
        logger.error(message)


# Initialize
main()

if __name__ == "__main__":
    print(f"SecureData is a library not intended to be directly run. See README.md.")

if argv[-1] == 'config':
    setConfigItem('path_securedata', input(
        f"Enter the full path of where you want to store all data (currently {PATH_SECUREDATA}/settings.json):\n"))

if len(argv) > 2 and argv[1] == 'edit':
    editFile(argv[2])
