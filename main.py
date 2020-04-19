#!/usr/local/bin/python3
# coding=utf-8

# <bitbar.title>Covid 19 Tracking by Country</bitbar.title>
# <bitbar.version>v0.1</bitbar.version>
# <bitbar.author>Anthony Jackson</bitbar.author>
# <bitbar.author.github>expelledboy</bitbar.author.github>
# <bitbar.desc>Show statistics of Covid 19 in your selected country</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/expelledboy/bitbar-covid</bitbar.abouturl>

import base64
import json
import sys
import os.path

from urllib.request import Request, urlopen

# XXX: curl https://api.covid19api.com/countries | jq '.[].Slug' | sort
COUNTRIES = ['afghanistan', 'ala-aland-islands', 'albania', 'algeria', 'american-samoa', 'andorra', 'angola', 'anguilla', 'antarctica', 'antigua-and-barbuda', 'argentina', 'armenia', 'aruba', 'australia', 'austria', 'azerbaijan', 'bahamas', 'bahrain', 'bangladesh', 'barbados', 'belarus', 'belgium', 'belize', 'benin', 'bermuda', 'bhutan', 'bolivia', 'bosnia-and-herzegovina', 'botswana', 'bouvet-island', 'brazil', 'british-indian-ocean-territory', 'british-virgin-islands', 'brunei', 'bulgaria', 'burkina-faso', 'burundi', 'cambodia', 'cameroon', 'canada', 'cape-verde', 'cayman-islands', 'central-african-republic', 'chad', 'chile', 'china', 'christmas-island', 'cocos-keeling-islands', 'colombia', 'comoros', 'congo-brazzaville', 'congo-kinshasa', 'cook-islands', 'costa-rica', 'cote-divoire', 'croatia', 'cuba', 'cyprus', 'czech-republic', 'denmark', 'djibouti', 'dominica', 'dominican-republic', 'ecuador', 'egypt', 'el-salvador', 'equatorial-guinea', 'eritrea', 'estonia', 'ethiopia', 'falkland-islands-malvinas', 'faroe-islands', 'fiji', 'finland', 'france', 'french-guiana', 'french-polynesia', 'french-southern-territories', 'gabon', 'gambia', 'georgia', 'germany', 'ghana', 'gibraltar', 'greece', 'greenland', 'grenada', 'guadeloupe', 'guam', 'guatemala', 'guernsey', 'guinea', 'guinea-bissau', 'guyana', 'haiti', 'heard-and-mcdonald-islands', 'holy-see-vatican-city-state', 'honduras', 'hong-kong-sar-china', 'hungary', 'iceland', 'india', 'indonesia', 'iran', 'iraq', 'ireland', 'isle-of-man', 'israel', 'italy', 'jamaica', 'japan', 'jersey', 'jordan', 'kazakhstan', 'kenya', 'kiribati', 'korea-north', 'korea-south', 'kosovo', 'kuwait', 'kyrgyzstan', 'lao-pdr', 'latvia', 'lebanon', 'lesotho', 'liberia', 'libya', 'liechtenstein',
             'lithuania', 'luxembourg', 'macao-sar-china', 'macedonia', 'madagascar', 'malawi', 'malaysia', 'maldives', 'mali', 'malta', 'marshall-islands', 'martinique', 'mauritania', 'mauritius', 'mayotte', 'mexico', 'micronesia', 'moldova', 'monaco', 'mongolia', 'montenegro', 'montserrat', 'morocco', 'mozambique', 'myanmar', 'namibia', 'nauru', 'nepal', 'netherlands', 'netherlands-antilles', 'new-caledonia', 'new-zealand', 'nicaragua', 'niger', 'nigeria', 'niue', 'norfolk-island', 'northern-mariana-islands', 'norway', 'oman', 'pakistan', 'palau', 'palestine', 'panama', 'papua-new-guinea', 'paraguay', 'peru', 'philippines', 'pitcairn', 'poland', 'portugal', 'puerto-rico', 'qatar', 'romania', 'russia', 'rwanda', 'réunion', 'saint-barthélemy', 'saint-helena', 'saint-kitts-and-nevis', 'saint-lucia', 'saint-martin-french-part', 'saint-pierre-and-miquelon', 'saint-vincent-and-the-grenadines', 'samoa', 'san-marino', 'sao-tome-and-principe', 'saudi-arabia', 'senegal', 'serbia', 'seychelles', 'sierra-leone', 'singapore', 'slovakia', 'slovenia', 'solomon-islands', 'somalia', 'south-africa', 'south-georgia-and-the-south-sandwich-islands', 'south-sudan', 'spain', 'sri-lanka', 'sudan', 'suriname', 'svalbard-and-jan-mayen-islands', 'swaziland', 'sweden', 'switzerland', 'syria', 'taiwan', 'tajikistan', 'tanzania', 'thailand', 'timor-leste', 'togo', 'tokelau', 'tonga', 'trinidad-and-tobago', 'tunisia', 'turkey', 'turkmenistan', 'turks-and-caicos-islands', 'tuvalu', 'uganda', 'ukraine', 'united-arab-emirates', 'united-kingdom', 'united-states', 'uruguay', 'us-minor-outlying-islands', 'uzbekistan', 'vanuatu', 'venezuela', 'vietnam', 'virgin-islands', 'wallis-and-futuna-islands', 'western-sahara', 'yemen', 'zambia', 'zimbabwe']


COVID_API_URL = 'https://api.covid19api.com/live/country/'
BITBAR_CONFIG_FILE = f'{os.environ["HOME"]}/.config/bitbar/covid.json'
DEFAULT_CONFIG = {'country': 'south-africa'}


def load_config():
    try:
        with open(BITBAR_CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return DEFAULT_CONFIG


def save_config(config):
    os.makedirs(os.path.dirname(BITBAR_CONFIG_FILE), exist_ok=True)
    with open(BITBAR_CONFIG_FILE, 'w') as f:
        json.dump(config, f)


def make_call(prog, *args):
    res = []
    res.append('bash="{0}"'.format(prog))
    for i, arg in enumerate(args):
        res.append('param{0}="{1}"'.format(i + 1, arg))
    return " ".join(res)


def get_stats_for_country(country):
    recent_updates = json.loads(urlopen(Request(
        COVID_API_URL + country,
        headers={"Accept": 'application/json'}
    )).read())
    return recent_updates[-1]


def show_title(stats):
    deaths = stats["Deaths"]
    active = stats["Active"]
    print(f'{active}🤢 {deaths}💀')


def show_change_country_menu(stats):
    print('---')
    print('Change Country')
    for country in COUNTRIES:
        text = f'-- {country}'
        action = make_call(sys.argv[0], "set_country", country)
        print("%s|%s terminal=false refresh=true" % (text, action))


def main():
    config = load_config()

    if len(sys.argv) == 3 and sys.argv[1] == 'set_country':
        config['country'] = sys.argv[2]
        save_config(config)
        print('Config saved')
        return

    stats = get_stats_for_country(config['country'])
    show_title(stats)
    show_change_country_menu(COUNTRIES)


if __name__ == "__main__":
    main()
