

ijournals = ['source:"European Journal of Information Systems"',
             'source:"Information Systems Journal"',
             'source:"Information Systems Research"',
             'source:"Journal of the Association for Information Systems"',
             'source:"Journal of Information Technology" - source:"International Journal of Information Technology" - source: "Journal of Information Technology &" - source:"Journal of Information Technology and"',
             'source:"Journal of Management information systems"',
             'source:"Journal of Strategic Information Systems"',
             'source:"MIS quarterly"']

isearch = 'organisation OR organization OR company OR enterprise AND intext:"artificial intelligence" AND "adoption"'

for ijournal in ijournals:
    print(isearch + ijournal)