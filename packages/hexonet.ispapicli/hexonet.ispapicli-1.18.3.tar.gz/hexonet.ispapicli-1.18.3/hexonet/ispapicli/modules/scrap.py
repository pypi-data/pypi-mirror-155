from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QProgressDialog
from .db import DB
import re
import requests


class Scrap:

    USER = "hexonet"
    REPO = "hexonet-api-documentation"

    def __init__(self):
        # init db
        self.dbObj = DB()

    def __saveCommandToDB(self, commandName, data):
        """
        Creates a record in DB for the command: commandName

        Returns:
        --------
        True | Raise exception
        """
        try:
            self.dbObj.insertCommand(commandName, data)
            return True
        except Exception:
            raise Exception("Couldn't insert the command: " + commandName)

    def __getCommandData(self, commandName, description, availability, parameters):
        """
        Gather all command data in a list and return it

        Returns:
        --------
        Dict{}: data
        """
        try:
            data = {}
            data["command"] = commandName
            data["description"] = description
            data["availability"] = availability
            data["paramaters"] = parameters
            return data
        except Exception as e:
            raise e

    def __getCommandsParams(self, raw):
        """
        Parse parameters from raw md data

        Returns:
        --------
        List[]: params
        """
        # split the rows based on | delimiter
        # this will return a list of paramname, min, type, etc.
        headers = raw[2].split("|")
        params = []
        param = {}
        # skip uncessary spaces, start from line/row 4
        for i in range(4, len(raw)):
            if raw[i] != "----":
                try:
                    cols = raw[i].split("|")  # split each row data to match the headers
                    for j in range(0, len(cols)):
                        headType = headers[j].strip(" \t\n\r")
                        headValue = cols[j].strip(" \t\n\r")
                        param[headType] = headValue
                    # append params | add only valid params
                    if len(param) == 4:
                        params.append(param)
                    param = {}
                except Exception as e:
                    return params
            else:
                return params
        return params

    def __getMDfiles(self, tree):
        MDfiles = []
        for file in tree:
            path = file["path"]
            if path.endswith(".md"):
                MDfiles.append(path)
        return MDfiles

    def scrapCommands(self):
        """
        Executes the scrap process

        Returns:
        --------
        List || False
        """

        url = "https://api.github.com/repos/{}/{}/git/trees/master?recursive=1".format(
            self.USER, self.REPO
        )
        response = requests.get(url)

        if response.status_code == 200:
            res = response.json()
            MDfiles = self.__getMDfiles(res["tree"])
            # add commands
            return MDfiles
        else:
            return False

    def readRawFiles(self, rawfiles):
        """
        Read and save raw files

        Returns:
        --------
        True || False
        """
        # prepare command sections
        commandRegex = r"^#\s\w+$"
        secionRegex = r"^#{2}\s\w+$"
        counter = 1

        self.dialog = QProgressDialog("...", "Cancel", counter, len(rawfiles) + 1)
        self.dialog.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.dialog.setWindowTitle("Please wait...")
        self.dialog.setMinimumWidth(300)
        self.dialog.setAutoClose(True)
        self.dialog.show()
        for file in rawfiles:
            # update the progress
            counter += 1
            self.dialog.setValue(counter)
            QApplication.processEvents()
            if self.dialog.wasCanceled():
                break
            # get file content
            url = "https://raw.githubusercontent.com/{}/{}/master/{}".format(
                self.USER, self.REPO, file
            )
            response = requests.get(url)
            if response.status_code == 200:
                res = response.content
                result = res.decode("utf-8")
                result = result.splitlines()
                # command details
                commandName = ""
                description = ""
                availability = ""
                parameters = []
                # get command data
                for i in range(len(result)):
                    if result[i] != "":
                        # check command name
                        commandValue = re.findall(commandRegex, result[i])
                        if len(commandValue) == 1:
                            commandName = result[i][1:]
                            self.dialog.setLabelText(
                                "<p align='left'> Updating: " + commandName + "</p>"
                            )
                            QApplication.processEvents()
                            continue
                        # checkSection
                        section = re.findall(secionRegex, result[i])
                        if len(section) == 1:
                            sectionName = (section[0].split(" "))[1]
                            if sectionName == "DESCRIPTION":
                                description = result[i + 1]
                            if sectionName == "AVAILABILITY":
                                availability = result[i + 1]
                            if sectionName == "COMMAND":
                                parameters = self.__getCommandsParams(result[i:])
                                break  # end the loop here, other data is not relevant
                data = self.__getCommandData(
                    commandName, description, availability, parameters
                )
                self.__saveCommandToDB(commandName, data)
            else:
                return False
        print("\nCommands count: " + str(counter))
        print("Command finished.")
        return True
