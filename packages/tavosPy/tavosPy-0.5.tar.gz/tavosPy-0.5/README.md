# tavosPy
Processes water outages from Tavos and provides them in a object with proper types

# Example usage

## Print raw data

```
tavospy = TavosPy()
tavospy.update()
print(tavospy.getData())
```

## Print data in human readable format

```
tavospy = TavosPy()
tavospy.update()

for waterOutage in tavospy.getData():
    printString = ""
    if(waterOutage['date']['start']):
        printString = printString + waterOutage['date']['start'].strftime("%d.%m.%Y %H:%M")
    if(waterOutage['date']['end']):
        printString = printString + " - " + waterOutage['date']['end'].strftime("%d.%m.%Y %H:%M")
    
    printString = printString + ": "
    if(waterOutage['city'] != ""):
        printString = printString + waterOutage['city']
    if(waterOutage['street'] != ""):
        printString = printString + " (" + waterOutage['street'] + ")"
    if(waterOutage['typeOfDefect'] != ""):
        printString = printString + " - " + waterOutage['typeOfDefect']
    if(waterOutage['notes'] != ""):
        printString = printString + " (" + waterOutage['notes'] + ")"
    print(printString)
```


# Disclaimer

Project and/or author is in no way associated with Tavos and provides this code completely free, according to LICENSE file.