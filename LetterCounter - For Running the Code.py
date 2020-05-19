# Letter Counter
#
# This program takes a text file and counts the amount of times the letters A-Z appear in it, and then
# outputs the results of that to a CSV file.
#
# Original code by Yash Dani
# Rewritten by Eric Chen
#
# Last updated June 10th, 2018
# This code is NOT to be redistributed without the permission of those listed above.
#

from collections import Counter
import csv
from datetime import datetime

fileName = ""
fileCounter = 0
maxCharacters = 0
repeat = "n"

while True:
    # Open Text File (Place in the same folder as this file and rename it to 'FileToScan.txt')
    # Skip items 25 and 29 due to file corruption (can be deleted for normal operation)
    # if fileCounter == 25:
    #     fileCounter = 26
    if fileCounter == 29:
        fileCounter = 30
    fileCounter += 1
    if fileCounter == 1:
        while True:
            repeat = input("Automatically run through all files without stopping? This assumes that you would like"
                           "to use the first line of each text file as the title. [Y/N]\n")
            if repeat.lower() == "y" or repeat.lower() == "n":
                repeat = repeat.lower()
                break
            else:
                print("Error: You must enter 'Y' or 'N'!")
        while True:
            try:
                maxCharacters = int(input("If you would like to set a limit on the number of characters scanned,"
                                          "please enter that in the form of a whole number now.\n"
                                          "If you would not like to restrict this, enter 0:\n"))
                if maxCharacters >= 0:
                    # The count starts from one later on
                    maxCharacters -= 1
                    break
                else:
                    print("Error: You must input a whole number >= 0!")
            except ValueError:
                print("Error: Input not an integer")

    while True:
        try:
            fileName = "FileToScan (" + str(fileCounter) + ").txt"
            scanFile = open(fileName, 'r')
            # Read the first line of the file, minus the line break character at the end
            titleLine = (scanFile.readline())[:-1]
            break
        except FileNotFoundError:
            print("Error: The file '" + fileName + "' was not found. Make sure that the file that you want processed "
                  "is named '" + fileName + "'.\n"
                  "This error can also be triggered if the last file has been reached. In that case, input 'E' to "
                  "quit the program. Otherwise, input anything else to try again.")
            error = input()
            if error.lower() == "e":
                raise SystemExit
        except UnicodeDecodeError:
            print("==> Error: The file", fileName, "has corrupted text. Skipping to next file.")
            fileCounter += 1

    if repeat == "n":
        print("Do you want to use the first line of the file as the title of the document? It currently reads:\n"
              "'" + str(titleLine) + "'\n[Y/N]")
    else:
        print("Processing " + str(titleLine) + ".")

    while True:
        if repeat == "n":
            useLine = input()
        else:
            useLine = "y"

        if useLine.lower() == "y":
            docName = titleLine
            break
        elif useLine.lower() == "n":
            print("Enter the actual name of the document that you are processing (ie book title, etc.):")
            while True:
                docName = input()
                if docName != "":
                    break
                else:
                    print("Error: Name cannot be blank. Please input a name:")
            break
        else:
            print("Error: Invalid input - must be [Y/N]. Please try again:")

    # Put entire file into a single variable
    text = scanFile.read()
    wordList = []

    # Add Words to dictionary
    for word in text.split():
        word = word.lower()

        # Delete Useless Chars from the word
        # Here you can replace any punctuation mark you want with nothing, thus getting rid of them
        # in the format word.replace('whatever punctuation you want to get rid of','')

        # word = word.replace('.', '')
        wordList.append(word)

    # List of characters to count (ignores others)
    scanList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                't', 'u', 'v', 'w', 'x', 'y', 'z']

    letterList = []
    for word in wordList:
        # Separate words into letters
        letters = list(word)
        for letter in letters:
            # Keeps characters not in the list to be scanned out of the total count
            if letter in scanList:
                letterList.append(letter)

    # Very similar to a dictionary but provides a little more flexibility in terms of queries
    cnt = Counter()

    # Keep track of letters counted so far in case the user wants to restrict max characters scanned
    # Not starting at zero because that would mean that there wouldn't be a way to restrict max characters
    totalLettersCounted = 1

    for letter in letterList:
        if totalLettersCounted == maxCharacters:  # If max characters is reach
            break
        cnt[letter] += 1
        totalLettersCounted += 1

    print("Letter: Occurrences:")
    for letter in scanList:
        print(str(letter) + "       " + str(cnt[letter]))
    print("\nOutputting to sheet. Please wait. This may take longer than a minute.")

    # Initialize lists
    emptyRow = [""]
    titleRow = ["", ""]
    rowList = ["", ""]

    allRows = []

    # First row contains the time of output and document title
    titleRow[1] = docName  # Column 2 (B)
    titleRow[0] = str(datetime.now().strftime('%m/%d %H:%M:%S'))  # Column 1 (A)

    with open('outputRestricted.csv', 'a', newline='') as csvFile:

        write = csv.writer(csvFile, delimiter=',')
        write.writerow(titleRow)

        # A list is used to separate each row into two cells (the list is the row contents)
        for letter in scanList:
            rowList[0] = letter  # Column 1 (A)
            rowList[1] = cnt[letter]  # Column 2 (B)
            write.writerow(rowList)

        # Place a blank row at the bottom of the output so subsequent outputs will be easier to fine
        write.writerow(emptyRow)

    scanFile.close()

    while True:
        if repeat == "n":
            print("Operation completed. Run again? (Make sure you switch out the file first) [Y/N]")
            runAgain = input()
        else:
            runAgain = "y"
        if runAgain.lower() != "y" and runAgain.lower() != "n":
            print("Error: Invalid input - must be 'Y' or 'N'. Please try again:")
        else:
            break
    if runAgain.lower() == "n":
        break
