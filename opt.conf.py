from configparser import ConfigParser

config = ConfigParser()

config['Hearbeat'] = {
    'KeepALive': 'true',
    'Time': 3
}

config['Maximum'] = {
    'MaximumPackages': 25,
    'Start': 'false'
}

with open('con.ini', 'w') as configfile:
    config.write(configfile)
