import unicodedata
import re


def indexOfSubstring(list, substring):
    substring = substring.lower()
    for i, s in enumerate(list):
        if substring in s.lower():
            return i
    return -1


def getDetails(text):
    indexOfName = indexOfSubstring(text, "Exact name") - 1
    indexOfState = indexOfSubstring(text, "State or ") - 1
    indexOfIndustrialClass = indexOfSubstring(text, "Primary Standard Industrial") - 1
    indexOfIRSNumber = indexOfSubstring(text, "Employer Identification") - 1
    indexOfAddress = indexOfSubstring(text, "Address") - 1
    indexOfDate = indexOfSubstring(text, "date of") - 1

    Name = text[indexOfName]
    State = text[indexOfState]
    IndustrialClass = text[indexOfIndustrialClass]
    IRSNumber = text[indexOfIRSNumber]
    Address = text[indexOfAddress]
    Date = text[indexOfDate]

    print("Name: ", Name)
    print("State: ", State)
    print("IndustrialClass: ", IndustrialClass)
    print("IRSNumber: ", IRSNumber)
    print("Address: ", Address)
    print("Date: ", Date)


def strip(line):
    escapes = "".join([chr(char) for char in range(1, 32)])
    translator = str.maketrans("", "", escapes)
    t = line.translate(translator)
    t = unicodedata.normalize("NFKD", t).strip()
    t = re.sub("\([0-9]\)", "", t)
    return t
