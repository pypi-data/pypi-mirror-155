from importlib.metadata import version
import subprocess
import requests
import os

def startApp():
    print("Start app")
    os.chdir(file_path)
    subprocess.run(["python", "-m", "ticsummary"])

def update():
    print("Updating...")
    subprocess.run(["python", "-m", "pip","install","--upgrade","neofti_ticsumary"])
    startApp()

currentVersion = version('neofti_ticsummary')
needUpdate = False
url = "https://pypi.org/pypi/neofti-ticsummary/json"

r = requests.get(url)
data = r.json()
listVersions = data["releases"].keys()
file_path = os.path.realpath(__file__).rsplit(os.sep,1)[0]

splitCurrentVersion = currentVersion.split('.')
valueCurrentVersion = int(splitCurrentVersion[0])*100 + int(splitCurrentVersion[1])*10 + int(splitCurrentVersion[2])
lastValueVersion = 0 
for pypiVersion in listVersions:
    splitPypiVersion = pypiVersion.split('.')
    valuePypiVersion = int(splitPypiVersion[0])*100 + int(splitPypiVersion[1])*10 + int(splitPypiVersion[2]) 
    if lastValueVersion < valuePypiVersion:
        lastValueVersion = valuePypiVersion
        lastVersion = pypiVersion
needUpdate = lastValueVersion <= valueCurrentVersion
if needUpdate:
    print("need Update")
    from PyQt6.QtWidgets import QMessageBox,QApplication
    import sys

    comment = data["releases"][lastVersion][0]['comment_text']
    app = QApplication(sys.argv)
    messageBox = QMessageBox()#title="Exit new version. Update?",text=comment)
    messageBox.setWindowTitle("New version available. Update?")
    messageBox.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
    messageBox.accepted.connect(lambda:update())
    messageBox.rejected.connect(lambda:startApp())
    if comment=="":
        messageBox.setText("Empty comment")
    else:
        messageBox.setText(comment)
    messageBox.show()
    sys.exit(app.exec())
else:
    startApp()