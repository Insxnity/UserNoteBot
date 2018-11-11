# pytbun v0 by /u/Insxnity
# Interface for working with Reddit Mod Toolbox Usernotes v6 over PRAW.
# Would not have been possible without /u/sjrsimac
#    https://www.reddit.com/r/RequestABot/comments/6xhfmk/would_like_a_bot_to_monitor_the_various_free/dmvk8xp/
import praw
import zlib
import base64
import json
import time

def getModeratorIndex(r,sub,mod):
    # TODO Handle more gracefully when a mod doesn't exist in the usernotes
    return PullandUnzipUsernotes(r,sub)[0]['constants']['users'].index(mod)

def getWarningIndex(r,sub,warning):
    # Not conditioned to deal with a warning bla bla bla ^^^
    return PullandUnzipUsernotes(r,sub)[0]['constants']['warnings'].index(warning)

# Huge thanks to /u/sjrsimac for the below code

def makeNewNote(blob, redditor, notetext, moderatornumber, link, warningNumber):
    newnote = {
    'n':notetext, # The displayed note.
    't':int(time.time()), # The time the note is made.
    'm':moderatornumber, # The moderator number that made the note.
    'l':link, # The attached link, which will be blank for now.
    'w':warningNumber # The warning number.
    }
    try:
        blob[redditor]['ns'] = [newnote] + blob[redditor]['ns']
    except:
        blob[redditor] = {'ns':list()}
        blob[redditor]['ns'] = [newnote]
    return blob

def PullandUnzipUsernotes(reddit, OurSubreddit):
    # Extract the whole usernotes page and turns it into a dictionary.
    allusernotes = json.loads(reddit.subreddit(OurSubreddit).wiki['usernotes'].content_md)
    # Get the blob in the usernotes and convert the base64 number into a binary (base2) number.
    blob = base64.b64decode(allusernotes['blob'])
    # Convert the blob binary number into a string.
    blob = zlib.decompress(blob).decode()
    # Convert blob string into a dictionary.
    blob = json.loads(blob)
    
    # Print the blob in a user readable form.
    # print(blob)
    
    return [allusernotes, blob]

def CompileandZipUsernotes(reddit, allusernotes, blob, ourSubreddit):
    # This is the debugging code. Disable or delete this when you're done debugging.
    # print(allusernotes)
    # print(blob)
   
    blob = json.dumps(blob)
    blob = blob.encode()
    blob = zlib.compress(blob)
    rewrittenblob = base64.b64encode(blob).decode()
    allusernotes['blob'] = str(rewrittenblob)
    allusernotes = json.dumps(allusernotes)
    reddit.subreddit(ourSubreddit).wiki['usernotes'].edit(allusernotes)
