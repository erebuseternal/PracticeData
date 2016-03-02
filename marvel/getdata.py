from marvelscraper import action, postProcess
from marvelcrawler import teleport
import json

soup = teleport.Seed('http://marvel.com/universe/Scarlet_Witch_%28Wanda_Maximoff%29')
# we input our soup into the action
action.SetVillain(soup)
# we scrape the page
action.Act()
while soup:
    soup = teleport.Teleport()
    if not soup:
        continue
    # we input our soup into the action
    action.SetVillain(soup)
    # we scrape the page
    action.Act()
    # and now we grap the resulting dictionary
    beaten = action.DumpVillain()
    # post process
    beaten = postProcess(beaten)
    # we add an id
    id = teleport.current_link[10:]
    beaten['id'] = id
    try:
        print(id)
        print(beaten['realname'])
        export = beaten
        export = json.dumps(export, sort_keys=True, indent=4)
        file = open('solrdata/' + id + '.json', 'w')
        file.write(str(export))
    except:
        print('YIKES! Real Name was missing, didn\'t include')
