# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pychpp']

package_data = \
{'': ['*']}

install_requires = \
['Werkzeug>=1.0.1,<2.0.0', 'pytz>=2020.1,<2021.0', 'rauth>=0.7.3,<0.8.0']

setup_kwargs = {
    'name': 'pychpp',
    'version': '0.3.8',
    'description': 'framework created to use the API provided by the online game Hattrick',
    'long_description': '# pyCHPP\n\npyCHPP is an object-oriented python framework created to use the API provided by the online game Hattrick (www.hattrick.org).\n\n## Installation\n\npyCHPP can be installed using pip :\n\n    pip install pychpp\n\n## Usage\n\n### First connection\n```python\nfrom pychpp import CHPP\n    \n# Set consumer_key and consumer_secret provided for your app by Hattrick\nconsumer_key = \'\'\nconsumer_secret = \'\'\n    \n# Initialize CHPP instance\nchpp = CHPP(consumer_key, consumer_secret)\n    \n# Get url, request_token and request_token_secret to request API access\n# You can set callback_url and scope\nauth = chpp.get_auth(callback_url="www.mycallbackurl.com", scope="")\n  \n# auth[\'url\'] contains the url to which the user can grant the application\n# access to the Hattrick API\n# Once the user has entered their credentials,\n# a code is returned by Hattrick (directly or to the given callback url)\ncode = ""\n\n# Get access token from Hattrick\n# access_token[\'key\'] and access_token[\'secret\'] have to be stored\n# in order to be used later by the app\naccess_token = chpp.get_access_token(\n                request_token=auth["request_token"],\n                request_token_secret=auth["request_token_secret"],\n                code=code,\n                )\n```\n### Further connections\n```python\n# Once you have obtained access_token for a user\n# You can use it to call Hattrick API\nchpp = CHPP(consumer_key,\n            consumer_secret,\n            access_token[\'key\'],\n            access_token[\'secret\'],\n            )\n    \n# Now you can use chpp methods to get datas from Hattrick API\n# For example :\ncurrent_user = chpp.user()\nall_teams = current_user.teams\n\nbest_team_ever = chpp.team(ht_id=1165592)\nbest_team_ever # <HTTeam object : Les Poitevins de La Chapelle (1165592)>\n\nbest_team_arena = best_team_ever.arena\nbest_team_arena # <HTArena object : Stade de La Chapelle (1162154)>\nbest_team_arena.name # \'Stade de La Chapelle\'\n\nworth_team_ever = chpp.team(ht_id=1750803)\nworth_team_ever # <HTTeam object : Capdenaguet (1750803)>\n\nplayer = chpp.player(ht_id=6993859)\nplayer # <HTPlayer object : Pedro Zurita (6993859)>\nplayer.career_goals # 1163\n\nmatch = chpp.match(ht_id=68599186)\nmatch # <HTMatch object : Skou United - FC Barentin (68599186)>\nmatch.date # datetime.datetime(2006, 2, 23, 20, 0)\n```\n\n## Mapping table between classes and CHPP XML files\nThe following table shows the relationships between pyCHPP classes and CHPP XML files :\n\n|pyCHPP class|CHPP XML files|\n|:---:|:---:|\n|HTArena|`arenadetails.xml`|\n|HTChallengeManager|`challenges.xml`|\n|HTLeague|`leaguedetails.xml`|\n|HTLeagueFixtures|`leaguefixtures.xml`|\n|HTMatch|`matchdetails.xml`|\n|HTMatchLineup|`matchlineup.xml`|\n|HTMatchesArchive|`matchesarchive.xml`|\n|HTNationalTeam|`nationalteamdetails.xml`|\n|HTNationalTeams|`nationalteams.xml`|\n|HTPlayer|`playerdetails.xml`|\n|HTRegion|`regiondetails.xml`|\n|HTTeam|`teamdetails.xml`|\n|HTUser|`managercompendium.xml`|\n|HTWorld|`worlddetails.xml`|\n|HTWorldCupGroups|`worldcup.xml`|\n|HTWorldCupMatches|`worldcup.xml`|\n|HTYouthPlayer|`youthplayerdetails.xml`|\n|HTYouthTeam|`youthteamdetails.xml`|\n\n## License\npyCHPP is licensed under the Apache License 2.0.\n',
    'author': 'Pierre Gobin',
    'author_email': 'dev@pierregobin.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://framagit.org/Pierre86/pychpp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
