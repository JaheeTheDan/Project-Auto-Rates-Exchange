'''Can read input from keyboard and do calculations of exchangerate based on what is inputed'''
from os import system
from requests import get
import keyboard
system('cls')

# API needed for getting date of exchangerate
API_KEY='3e05c0498d440842ab943450'

def get_exchange_rate_data()->dict:
    '''Get exchange rate data from api and convert to a dictionary'''
    repsonse= get(f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/JMD')
    data=repsonse.json()
    return data.get('conversion_rates')


def from_jmd_to(curreny: str):
    '''Exchange from jmd to curreny enter and print the result'''
    print('From JMD',conversion_rates['JMD'])
    print(f'To {curreny}',conversion_rates[curreny])
    print(round(conversion_rates[curreny]*money,2))


def to_jmd_from(curreny: str):
    '''Exchange to jmd from curreny enter and print the result'''
    print('To JMD',conversion_rates['JMD'])
    print(f'From {curreny}',conversion_rates[curreny])
    print(round(money/conversion_rates[curreny],2))


conversion_rates = get_exchange_rate_data()


print('Welcome')
convertion=input('From JMD or to JMD\n')
money=float(input('How much\n'))
req_curreny = input('What curreny\n').upper()

if convertion == 'from':
    from_jmd_to(req_curreny)
else:
    to_jmd_from(req_curreny)


# recorded = keyboard.record(until='esc')
# # Then replay back at three times the speed.
# keyboard.play(recorded, speed_factor=3)

# def record():
#     r=keyboard.get_typed_strings(keyboard.stop_recording())
#     print(''.join(r))
#     keyboard.start_recording()


# keyboard.start_recording()
# keyboard.add_word_listener('hello',record, ['space'])

# keyboard.wait()
