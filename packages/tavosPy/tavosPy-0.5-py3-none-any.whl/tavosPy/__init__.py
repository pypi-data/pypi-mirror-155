#
# Author: Juraj Nyiri
#
#
#!/usr/bin/python
# -*- coding: UTF-8 -*-

from pyquery import PyQuery
import re
import datetime
import requests


class TavosPy:
    def __init__(self):
        self.url = "https://tavos.sk/nahlasene-odstavky-vody/"

        self.htmlData = ""
        self.data = ""

        self.maxSearchValue = 10

    def setUrl(self, url):
        self.url = url

    def getUrl(self):
        return self.url

    def sethtmlData(self, data):
        self.htmlData = data

    def gethtmlData(self):
        return self.htmlData

    def setData(self, data):
        self.data = data

    def getData(self):
        return self.data

    def updateHtml(self):
        try:
            r = requests.get(self.getUrl())
            if r.status_code == 200:
                self.sethtmlData(r.text)
                return True
        except requests.exceptions.RequestException:
            return False
        return False

    def updateData(
        self, tdStart=0, theBestDataFound=False, theBestDataCorrectness=False
    ):
        pq = PyQuery(self.htmlData)

        lastUpdate = pq(".elementor-shortcode").find("p").text()

        tag = pq("div > table > tbody > tr").find("td")

        pattern = re.compile(r"(\d+)")

        tdChild = tdStart

        try:
            data = {}
            data["updated"] = lastUpdate
            data["outages"] = []
            # Get start time
            i = 0
            for date in tag("td:nth-child(" + str(tdChild) + ")").items():
                if len(data["outages"]) <= i or data["outages"][i] is None:
                    data["outages"].append({})
                data["outages"][i]["date"] = {}
                data["outages"][i]["date"]["start"] = self.getTime(
                    re.findall(pattern, date.text())
                )
                i += 1

            tdChild += 1
            # Get city
            i = 0
            for city in tag("td:nth-child(" + str(tdChild) + ")").items():
                if len(data["outages"]) <= i or data["outages"][i] is None:
                    data["outages"].append({})
                data["outages"][i]["city"] = city.text()
                i += 1

            tdChild += 1

            # Get company
            i = 0
            for street in tag("td:nth-child(" + str(tdChild) + ")").items():
                if len(data["outages"]) <= i or data["outages"][i] is None:
                    data["outages"].append({})
                data["outages"][i]["company"] = street.text()
                i += 1

            tdChild += 1

            # Get street
            i = 0
            for street in tag("td:nth-child(" + str(tdChild) + ")").items():
                if len(data["outages"]) <= i or data["outages"][i] is None:
                    data["outages"].append({})
                data["outages"][i]["street"] = street.text()
                i += 1

            tdChild += 1

            # Get end time
            i = 0
            for date in tag("td:nth-child(" + str(tdChild) + ")").items():
                if len(data["outages"]) <= i or data["outages"][i] is None:
                    data["outages"].append({})
                data["outages"][i]["date"]["end"] = self.getTime(
                    re.findall(pattern, date.text())
                )
                i += 1

            tdChild += 1
            # Get water import
            i = 0
            for waterImport in tag("td:nth-child(" + str(tdChild) + ")").items():
                if len(data["outages"]) <= i or data["outages"][i] is None:
                    data["outages"].append({})
                data["outages"][i]["waterImport"] = waterImport.text()
                i += 1

            tdChild += 1

            # Get notes
            i = 0
            for note in tag("td:nth-child(" + str(tdChild) + ")").items():
                if len(data["outages"]) <= i or data["outages"][i] is None:
                    data["outages"].append({})
                data["outages"][i]["notes"] = note.text()
                i += 1

            tdChild += 1

            # Get ID
            i = 0
            for note in tag("td:nth-child(" + str(tdChild) + ")").items():
                if len(data["outages"]) <= i or data["outages"][i] is None:
                    data["outages"].append({})
                data["outages"][i]["id"] = note.text()
                i += 1

            # analyze data["outages"] set for the best accuracy
            currentCorrectness = self.analyzeDataCorrectness(data["outages"])

            if (
                not theBestDataFound or not theBestDataCorrectness
            ) or currentCorrectness > theBestDataCorrectness:
                theBestDataFound = data
                theBestDataCorrectness = currentCorrectness
            if tdStart <= self.maxSearchValue:
                return self.updateData(
                    tdStart + 1, theBestDataFound, theBestDataCorrectness
                )
            else:
                return self.finishUpdateData(theBestDataFound)
        except Exception as e:
            if tdStart > self.maxSearchValue:
                return self.finishUpdateData(theBestDataFound)
            return self.updateData(
                tdStart + 1, theBestDataFound, theBestDataCorrectness
            )

    def finishUpdateData(self, data):
        properOutages = []
        for outage in data["outages"]:
            if not (
                not "street" in outage
                or "notes" not in outage
                or "waterImport" not in outage
                or "id" not in outage
            ):
                properOutages.append(outage)
        data["outages"] = properOutages
        self.setData(data)
        return len(data) > 0

    def analyzeDataCorrectness(self, data):
        correctness = 0
        for entry in data:
            if "date" in entry and "start" in entry["date"] and entry["date"]["start"]:
                correctness += 1
            if "date" in entry and "end" in entry["date"] and entry["date"]["end"]:
                correctness += 1
            if "city" in entry and entry["city"] and entry["city"] != "":
                correctness += 1
            if "street" in entry and entry["street"] and entry["street"] != "":
                correctness += 1
            if (
                "waterImport" in entry
                and entry["waterImport"]
                and entry["waterImport"] != ""
            ):
                correctness += 1
            if "company" in entry and entry["company"] and entry["company"] != "":
                correctness += 1
            if "notes" in entry and entry["notes"] and entry["notes"] != "":
                correctness += 1
            if "id" in entry and entry["id"] and entry["id"] != "":
                correctness += 1
        return correctness

    def update(self):
        return self.updateHtml() and self.updateData()

    def getTime(self, numbers):
        date = False

        if len(numbers) > 0:

            day = False
            month = False
            year = False

            minute = False
            second = False

            for number in numbers:
                if len(number) <= 2:
                    if day == False:
                        day = number
                    elif month == False:
                        month = number
                    elif minute == False:
                        minute = number
                    elif second == False:
                        second = number
                elif len(number) == 4:
                    year = number

            if (
                day != False
                and month != False
                and year != False
                and minute != False
                and second != False
            ):
                date = datetime.datetime(
                    int(year), int(month), int(day), int(minute), int(second),
                )
        return date
