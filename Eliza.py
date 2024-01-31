import re 

def extractName(input):
    formattedName = "Anon"
    cleanInput = re.sub(r"[!,.?]", '', input)
    if not re.search(r"\s", cleanInput): 
        formattedName = input[0].upper() + input[1:].lower()
    else:
        search = re.search(r"\.*\b(is|am)\b", cleanInput)
        if search:
            endInd = search.span()[1]
            foundName = search.string[endInd+1:]
            formattedName = foundName[0].upper() + foundName[1:].lower()
    return formattedName

askName = input('Hi! My name is Eliza. What is your name?\n')

name = extractName(askName)
user_input = input('Hi ' + name + '! How can I help you today?\n')

negEmotions = ['angry', 'sad', 'depress', 'upset', 'frustrate', 'scare', 'disgust', 'annoy',
               'bore', 'afraid', 'anxious', 'bitter', 'lonely', 'jealous']

separator = '|'
patternNegEmo = rf".*\b({separator.join(negEmotions)}).*"

# while True:
checkNegEmo = re.search(patternNegEmo, user_input, re.IGNORECASE)
if checkNegEmo:
    print(f"I am sorry to hear that, {name}!\n")
