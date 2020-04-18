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

# XXX: curl https://api.covid19api.com/countries | jq '.[].Slug'
COUNTRIES = ["new-zealand", "palau", "bolivia", "ghana", "cook-islands", "guyana", "qatar", "seychelles", "bulgaria", "liberia", "montserrat", "oman", "saint-kitts-and-nevis", "lithuania", "mali", "papua-new-guinea", "benin", "cayman-islands", "chile", "brunei", "malawi", "nigeria", "saint-vincent-and-the-grenadines", "korea-north", "myanmar", "poland", "egypt", "trinidad-and-tobago", "hungary", "jordan", "macedonia", "antarctica", "djibouti", "french-polynesia", "honduras", "south-africa", "yemen", "malaysia", "mayotte", "namibia", "norfolk-island", "samoa", "albania", "british-indian-ocean-territory", "denmark", "lebanon", "svalbard-and-jan-mayen-islands", "saint-helena", "switzerland", "uzbekistan", "guadeloupe", "iran", "macao-sar-china", "morocco", "norway", "belarus", "ecuador", "jersey", "solomon-islands", "timor-leste", "zimbabwe", "czech-republic", "heard-and-mcdonald-islands", "hong-kong-sar-china", "malta", "new-caledonia", "bangladesh", "slovakia", "united-kingdom", "thailand", "andorra", "china", "croatia", "luxembourg", "south-sudan", "canada", "turkey", "senegal", "botswana", "french-guiana", "maldives", "marshall-islands", "réunion", "mongolia", "saudi-arabia", "sudan", "sweden", "french-southern-territories", "lao-pdr", "netherlands", "niue", "swaziland", "india", "panama", "tonga", "united-states", "vanuatu", "belgium", "cote-divoire", "montenegro", "portugal", "ukraine", "colombia", "cyprus", "faroe-islands", "singapore", "somalia", "turks-and-caicos-islands", "antigua-and-barbuda", "gibraltar", "greece", "korea-south", "aruba", "israel", "kenya", "south-georgia-and-the-south-sandwich-islands", "brazil", "congo-kinshasa", "fiji", "grenada", "syria", "el-salvador", "germany", "suriname",
             "guernsey", "martinique", "cameroon", "greenland", "serbia", "british-virgin-islands", "vietnam", "wallis-and-futuna-islands", "bosnia-and-herzegovina", "costa-rica", "mauritius", "saint-lucia", "guam", "russia", "slovenia", "sri-lanka", "cambodia", "gambia", "nepal", "nicaragua", "paraguay", "estonia", "guinea-bissau", "kuwait", "madagascar", "jamaica", "western-sahara", "angola", "austria", "ethiopia", "gabon", "mauritania", "saint-barthélemy", "azerbaijan", "burundi", "christmas-island", "kiribati", "pakistan", "saint-martin-french-part", "sao-tome-and-principe", "algeria", "mexico", "latvia", "libya", "romania", "bahrain", "belize", "central-african-republic", "indonesia", "saint-pierre-and-miquelon", "togo", "chad", "iraq", "niger", "taiwan", "holy-see-vatican-city-state", "japan", "mozambique", "netherlands-antilles", "turkmenistan", "uruguay", "argentina", "armenia", "bahamas", "rwanda", "anguilla", "dominican-republic", "kazakhstan", "sierra-leone", "tajikistan", "guatemala", "venezuela", "afghanistan", "australia", "cuba", "france", "georgia", "italy", "monaco", "american-samoa", "peru", "uganda", "burkina-faso", "moldova", "haiti", "micronesia", "united-arab-emirates", "northern-mariana-islands", "zambia", "isle-of-man", "san-marino", "cocos-keeling-islands", "kyrgyzstan", "barbados", "equatorial-guinea", "finland", "guinea", "tuvalu", "eritrea", "nauru", "spain", "ireland", "bermuda", "bhutan", "comoros", "dominica", "iceland", "palestine", "puerto-rico", "lesotho", "philippines", "tunisia", "ala-aland-islands", "congo-brazzaville", "pitcairn", "tokelau", "virgin-islands", "kosovo", "tanzania", "us-minor-outlying-islands", "bouvet-island", "cape-verde", "falkland-islands-malvinas", "liechtenstein"]

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
