from jess import Action
import re
from copy import copy

# Here are our extraction functions

def bold(tag):
    # this gets the content from the bold tag
    try:
        return tag.b.get_text().strip()
    except:
        return 'None'

def unmarkedtext(tag):
    # this gets the text from all of the children
    # of the paragraph (strings are counted as children) from
    # after the second tag onwards (the second child is a bold tag for
    # the paragraphs we will be extracting data from with
    # this function)
    string = ''
    count = 0
    for child in tag.children:
        if count > 1:
            try:
                string = string + child.get_text()
            except:
                string = string + child
        count += 1
    return string

def text(tag):
    # just grabs all of the text
    return tag.get_text().strip()

def blocks(tag):
    # this will get the number of blocks diplayed in this tag
    styling = tag.attrs['style']
    # styling in the page is of the form width:[numbers]px;
    # we want to just get the number of pixels so we know
    # how wide it is.
    width = styling[6:-3]
    # now depending on the width, we return the number of blocks
    if width == '21':
        return 1
    elif width == '42':
        return 2
    elif width == '63':
        return 3
    elif width == '84':
        return 4
    elif width == '105':
        return 5
    elif width == '126':
        return 6
    else:
        return 7

def firstchild(tag):
    for child in tag.children:
        # have to do this to actually make it a string
        return str(child)


def content(tag):
    # this simply returns the constant string 'Content'
    return 'Content'

# here is our function dictionary
weapons = {'firstchild' : firstchild, 'bold': bold, 'unmarkedtext': unmarkedtext, 'text': text, 'blocks': blocks, 'content': content}

# here is our action
action = Action('marvelscraper.css', weapons)

def concatenateContent(dumped_villain):
    if not 'Content' in dumped_villain:
        dumped_villain['Content'] = ''
        return
    content_string = ''
    for string in dumped_villain['Content']:
        content_string = content_string + string
    dumped_villain['Content'] = content_string

def splitValuesSemi(dumped_villain):
    keys = ['Significant Issues']
    for key in dumped_villain:
        # we make sure we are grabbing something from the sidebar
        if key in keys:
            string = dumped_villain[key][0] # remember all values are a list, even if it
                                # is a list of one element
            strings = string.split(';')
            new_strings = []
            # we just want to strip whitespace now
            for string in strings:
                string = string.strip()
                new_strings.append(string)
            # now we assign these new values to the key
            dumped_villain[key] = new_strings

def splitValueBoth(dumped_villain):
    keys = ['Occupation', 'Aliases', 'Place of Birth', 'Universe', 'Identity', 'Citizenship', 'Origin', 'Group Affiliation']
    for key in dumped_villain:
        # we make sure we are grabbing something from the sidebar
        if key in keys:
            string = dumped_villain[key][0] # remember all values are a list, even if it
                                # is a list of one element
            string = string.replace(';',',')
            strings = string.split(',')
            new_strings = []
            # we just want to strip whitespace now
            for string in strings:
                string = string.strip()
                new_strings.append(string)
            # now we assign these new values to the key
            dumped_villain[key] = new_strings

def removePhysicalAttributes(dumped_villain):
    if 'Physical Attributes' in dumped_villain:
        del dumped_villain['Physical Attributes']

weight_expre = re.compile('[0-9]{1,}')
def getWeight(dumped_villain):
    if 'Weight' in dumped_villain:
        match = re.search(weight_expre, dumped_villain['Weight'][0])
        if match:
            weight = int(match.group(0))
            dumped_villain['Weight'] = [weight]

height_expre = re.compile('(?:([0-9]*)\')?(?:([0-9]*)\")?')
def getHeight(dumped_villain):
    if 'Height' in dumped_villain:
        match = re.search(height_expre, dumped_villain['Height'][0])
        if match:
            inches = 0
            feet = 0
            try:
                inches = int(match.group(2))
            except:
                pass
            try:
                feet = int(match.group(1))
            except:
                pass
            height = feet*12 + inches
        dumped_villain['Height'] = [height]

un_expre = re.compile('(?i)unrevealed')
unk_expre = re.compile('(?i)unknown')
def removeUnrevealed(dumped_villain):
    keys = ['Height', 'Weight']
    for key in keys:
        if not key in dumped_villain:
            continue
        if re.search(un_expre, dumped_villain[key][0]) or re.search(unk_expre, dumped_villain[key][0]):
            del dumped_villain[key]

def removeFields(dumped_villain):
    keys = ['Content', 'Universe', 'Real Name', 'Aliases', 'Identity', 'Citizenship', 'Place of Birth', 'First Appearance',
    'Origin', 'Significant Issues', 'Occupation', 'Known Relatives', 'Group Affiliation',
    'Education', 'Powers', 'durability', 'energy', 'fighting', 'intelligence', 'speed',
    'strength', 'Height', 'Weight', 'Eyes', 'Hair']
    villain = copy(dumped_villain)
    for key in villain:
        if not key in keys:
            del dumped_villain[key]

def lowerCaseNoSpaces(dumped_villain):
    villain = {}
    for key in dumped_villain:
        new_key = key.lower().replace(' ', '')
        villain[new_key] = dumped_villain[key]
    return villain

def removeBadArrays(dumped_villain):
    # will have to change this for mongo
    for key in dumped_villain:
        if len(dumped_villain[key]) == 1:
            dumped_villain[key] = dumped_villain[key][0]

def stripName(dumped_villain):
    if 'Real Name' in dumped_villain:
        dumped_villain['Real Name'] = dumped_villain['Real Name'][0].strip()

def postProcess(dumped_villain):
    postprocessing = [removeFields, removeUnrevealed, stripName, getWeight, getHeight,
    concatenateContent, splitValuesSemi, splitValueBoth, removeBadArrays]
    for function in postprocessing:
        function(dumped_villain)
    return lowerCaseNoSpaces(dumped_villain)
