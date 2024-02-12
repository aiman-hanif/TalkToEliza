""" 
Program: eliza.py
Author: Aiman Hanif
Date: 02/05/2024
Course: CMSC 416 Spring 2024

Problem Description: 
    Create an psychotherapist Eliza chatbot using regular expressions to spot key words in a sentence and transform user input into questions.

Usage:
    Run by typing "python3 ./Eliza.py" into the terminal. Make sure to move to the directory of the file. 
    Input whole sentences with proper punctuation to get the best results from Eliza. 
    
Example Run:
    ELIZA: Hi! My name is Eliza. I am a psychotherapist. What is your name?
    USER: My name is aiman.
    ELIZA: Hi Aiman! How can I help you today?
       Please note that you can exit this conversation at any time by typing in "EXIT".
    AIMAN: I am feeling overwhelmed.
    ELIZA: That sounds tough, Aiman. Why don't you tell me more about being overwhelmed?
    AIMAN: I want a vacation from work.
    ELIZA: How would it help you if you had a vacation from work?
    AIMAN: I think it would make me less stressful.
    ELIZA: Tell me more about why you think it would make you less stressful?
    AIMAN: I am not sure, I think I miss my friends.
    ELIZA: Your friends must mean a lot to you. Why do you miss them?
    AIMAN: EXIT
    ELIZA: Goodbye, Aiman!
    
Algorithm:
    1. Extract name from the first input
        -> remove punctuation
        -> set the default name as "Anon"
        -> if input is a single word, then use that as the user name
        -> Otherwise, search for "is" or "am" in the sentence to spot the name of the user
        -> extract the text after "is" or "am" and save it as name
    2. Create lists of phrases
        -> phrases for responding to negative and positve emotions
        -> phrases for responding to "never" or other absolutes
        -> phrases for respond to "can't"
        -> phrases for responding to a desire to do something
        -> random phrases for when none of the above specific situations match
        -> phrases for asking more clarirfication
    3. Create a list of transformations
        -> this list contains the pattern we will search for as well as the list of possible phrases Eliza could respond with
        -> the order of patterns in the list should be from most specific to least specific
    4. Create a list of intro sentences for catching words like "never" or "everyone"
        -> similar to the transformations list
    5. While user hasn't inputted "EXIT", do the following for every user input:
        -> check if the user entered "EXIT" and quit the program if so
        -> check if the user mentioned "panic". If so, lead them to taking 10 deep breaths. Prompt next input.
        -> remove phrases surrounded by commas from the user input to make the input simpler
        -> loop through the list of intro
            - search for the ith pattern in the user input
            - if pattern found, randomize the list of possible phrases from the transformations list
        -> loop through the list of transformations:
            - search for the ith pattern in the user input
            - if pattern found, randomize the list of possible phrases from the transformations list
            - extract key words such as any emotion mentioned
            - transform words like "i" into "you" and "my" into "your"
            - form the output using the randomized phrase and the extracted keyword
        -> if none of the patterns from the transformations list were matched, repear user input and output a sentence asking for more clarification
        -> prompt user input with the final formatted response           
    
"""

import re 
import time
import random

def extractName(input):
    """_summary_
    Extracts the name of the user given an input string
    Algorithm:
        1. Remove punctuation from the input
        2. Search for "is" or "am" in the input
        3. Extract the text after the match and return as the name of the user
    Args:
        input (str): input to parse

    Returns:
        str: name of the user
    """
    # Default name is ANON if no name found
    formattedName = "Anon"
    # remove punctuation
    cleanInput = re.sub(r"[!,\.?]", "", input)
    # if input is a single word, then use that as a name
    if not re.search(r"\s", cleanInput): 
        formattedName = cleanInput
    else:
        # search for "is" or "am"
        search = re.search(r"\.*\b(is|am)\b", cleanInput)
        # use the text after the match as a name
        if search:
            endInd = search.span()[1]
            foundName = cleanInput[endInd+1:]
            formattedName = foundName
    # properly capitalize the name before returning
    return formattedName[0].upper() + formattedName[1:].lower()

def transformBasic(input):
    """_summary_
    transform possessive words and remove punctuation
    Args:
        input (str): input to be formatted

    Returns:
        str: transformed string
    """
    transform = re.sub(r"[\.,!?]", "", input)
    # transform "i" into "you"
    transform = re.sub(r"\b(I|i)\b", "you", transform)
    # transform "am" into "are"
    transform = re.sub(r"\b((a|A)(m|M))\b", "are", transform)
    # transform "my" into "your"
    transform = re.sub(r"\b((m|M)(y|Y))\b", "your", transform)
    # transform "was" into "were"
    transform = re.sub(r"\b((w|W)(a|A)(s|S))\b", "were", transform)
    # transform "me" into "you"
    transform = re.sub(r"\b((m|M)(E|e))\b", "you", transform)
    return transform.lower()

def removeComma(input):
    """_summary_
    remove text surrounded by commas from the user input
    Args:
        input (str): string to be formatted

    Returns:
        str: formatted string
    """
    # find occurrences of commas
    punctuation = re.search(r".*, ", input)
    # remove text surrounded by commas
    if punctuation:
        endInd = punctuation.span()[1]
        remainingT = input[endInd:]
        return remainingT
    return input


# Send the first response asking for user input
askName = input('ELIZA: Hi! My name is Eliza. I am a psychotherapist. What is your name?\nUSER: ')

# get the user's name
name = extractName(askName)

# prompt user for input and print the note on how to exit the program
user_input = input("ELIZA: Hi " + name + "! How can I help you today?\n" + 
                   "       Please note that you can exit this conversation at any time by typing in \"EXIT\".\n" +
                   name.upper() + ": ")

# list of keywords such as emotions and loved ones
sadEmotions = ['overwhelmed', 'sad', 'depressed', 'upset', 'frustrated', 'scared', 'anxious', 'lonely', 'hopeless', 'dejected', 'bad']
happyEmotions = ['happy', 'excited', 'refreshed', 'joyful', 'thankful', 'grateful', 'better', 'good']
lovedOnes = ['family', 'mothers?', 'fathers?', 'sisters?', 'brothers?', 'grandmothers?', 'grandfathers?', 'aunts?', 'uncles?', 'pets?', 'cousins?', 'friends?', 'cats?', 'dogs?']
absolutes = ['all', 'everyone', 'always']

# list of possible responses for emotions and other keywords
happyPhrases = ['I am glad, {name}! What makes you feel {plug}', 'I am glad, {name}! Tell me more about why you feel {plug}', 'Amazing! How does being {plug} affect you', 'It seems that your day is going well, {name}! Why don\'t you tell me more about being {plug}']
sadPhrases = ['That sounds tough, {name}. Why don\'t you tell me more about being {plug}', 'I am sorry to hear that, {name}. Why do you feel {plug}', 'I am sorry to hear that, {name}. What led you to feel {plug}', 
              'I am sorry to hear that, {name}. How does being {plug} affect you', 'That sounds rough, {name}. What\'s the reason that you feel {plug}', 'I am sorry to hear that, {name}. How long have you been feeling {plug}']
cantPhrases = ['Can you never', 'Is it always that case that you can\'t', 'Why do you think that you can\'t', 'Let\'s try challenging that belief, {name}! Why do you think that you can\'t']
wantPhrases = ['How would it help you if you had', 'Why do you desire', 'Why do you {plug}', 'What makes you want']
randomPhrases = ['Why do you believe that you', 'Tell me more about why you', 'What makes you think that you']
neverPhrases = ['Let\'s challenge that belief!', 'Never say Never!', 'Have you truly never?']
absolutePhrases = ['Is it truly {plug}?']
uncertainPhrases = ['Do you mean to say that ', 'Are you sure you meant that ', 'I am not sure I understand. What do you mean by ', 'Please elaborate more. What do you mean by ']

# create patterns by combining the list of keywords
separator = '|'
patternSadEmo = rf".*\b({separator.join(sadEmotions)})\b"
patternHappyEmo = rf".*\b({separator.join(happyEmotions)})\b"
patternLovedOnes = f"{separator.join(lovedOnes)}"
patternAbsolutes = rf".*\b({separator.join(absolutes)})\b"

# set isEnd to false to start the loop
isEnd = False


# create the list of transformations
    # if a user is asking Eliza questions -> redirect the conversation
    # spot emotions
    # spot desire to do something
    # spot inability to do something through words like "can't"
    # spot the word "miss"
    # more general transformations like transforming sentences that start with "I" if the specific ones don't work
transform = [
    [r".*\b(are you)\b.*", ["Let's talk about you. How are you feeling today"]],
    [patternSadEmo, sadPhrases],
    [patternHappyEmo, happyPhrases],
    [rf".*\b(miss)\b.*\b({patternLovedOnes})\b", ["Your {plug} must mean a lot to you. Why do you miss them"]],
    [r".*\b(m|My)\b", ['Your']],
    [r".*\b(can't|can not)\b", cantPhrases],
    [r".*\b(don't|do not)\b",[ "Why do you not"]],
    [r".*\b(want|need|wish)", wantPhrases],
    [r".*\b(I)\b \b(think|guess|believe)", randomPhrases],
    [r".*\b(I am)\b", ["Why are you"]],
    [r".*\b(I was)\b", ["Why were you"]],
    [r".*\b(I)\b", randomPhrases],
    [r".*\b(they|he|she)\b", ["What makes you think that {plug}"]]
]

# create the list of intro patterns for absolutes
intro = [
    [r".*\b(never)\b", neverPhrases],
    [patternAbsolutes, absolutePhrases]
]

# start the loop for chatting
while not isEnd:
    # check if user entered "EXIT", and quit the program if so
    if re.search(r"\b(EXIT)\b", user_input, re.IGNORECASE):
        print("ELIZA: Goodbye, " + name + "!")
        isEnd = True
        break
    found = False
    # search for words related to panic
    findPanic = re.search(r".*\b(panic)", user_input, re.IGNORECASE)
    # if "panic" found,
    if findPanic:
        # prompt user to take deep breaths
        print("ELIZA: If you're feeling panicky, let's take 10 deep breaths.")
        count10 = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten']
        # count to 10 for the user with 5 sec intervals
        for i in range(10):
            print("       " + count10[i])
            time.sleep(5)
        # prompt the user for input
        user_input = input("You did great, " + name + "! How do you feel now?\n" + name.upper() + ": ")
        continue
    # for inputs besides "panic" and "exit":
    output = ""
    remainingT = ""
    # remove text surrounded by commas from the input to make it simpler to parse
    user_input = removeComma(user_input)
    introFound = False
    # go through the list of intro patterns
    for i in range(len(intro)):
        # if the ith pattern found in the user input then append an appropriate resposne to the output
        search = re.search(intro[i][0], user_input, re.IGNORECASE)
        if search:
            numCaptured = len(search.groups())
            plug = search.group(numCaptured).lower()
            phrase = random.choice(intro[i][1])
            output = phrase.format(plug = plug, name = name)
            introFound = True
            break
    # go through the list of transformations
    for i in range(len(transform)):
        # search for the ith pattern in the user input
        search = re.search(transform[i][0], user_input, re.IGNORECASE)
        if search:
            # if pattern found, then extract the keyword
            numCaptured = len(search.groups())
            plug = search.group(numCaptured).lower()
            endInd = search.span()[1]
            # get the remaining sentence 
            remainingT = user_input[endInd+1:]
            # randomize a phrase from the transformations list for the ith pattern
            phrase = random.choice(transform[i][1])
            # create the output
            output += " " if introFound else ""
            output += phrase.format(plug = plug, name = name)
            found = True
            break
    # if no pattern matched, then print statement asking for more clarification
    if not found and output == "":
        # randomize from the uncertain phrases list
        # ask for more clarification and repeat user input
        phrase = random.choice(uncertainPhrases)
        output = phrase + transformBasic(user_input)
    # call transformBasic() on user input to transform words like "I" into "you", etc.
    if not remainingT == "":
        remainingT = transformBasic(remainingT)
        output += " " + remainingT
    # remove any double punctuation     
    puntuation = ['.', ',', '!', '?']
    output += "" if output[-1] in puntuation else "?"
    # prompt the user for input
    user_input = input("ELIZA: " + output + "\n" + name.upper() + ": ")
    

