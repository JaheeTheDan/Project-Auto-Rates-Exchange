'''Can read input from keyboard presses and do calculations of exchange rates based on what the user
entered, and received the result as keyboard key presses.
'''
import re
from os import system
from requests import get, exceptions
import keyboard as kb
system('cls')

# The print statements are for debugging purposes


# API needed for getting date of exchangerate
API_KEY = '3e05c0498d440842ab943450'
LOCAL_REGION_CURRENCY = 'JMD'


def output_error(error_text: str = ''):
    '''Function that outputs an error message, staring with \'!errorr \' '''
    bs_count = 4
    kb.press_and_release(','.join(['backspace' for i in range(bs_count)]))
    kb.write('!error '+error_text)


def get_exchange_rate_data(region_currency: str) -> dict:
    '''Get the exchange rate data from the given region from the API'''
    tries = 0
    # If there an error to get the data, it tries again. And at the 3rd try,
    # An error message is returned to user.
    while tries < 3:
        try:
            response = get(
                f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{region_currency}')
            return response.json().get('conversion_rates')
        except (exceptions.ConnectionError, exceptions.HTTPError):
            tries += 1

    try:
        response = get(
            f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{region_currency}')
        return response.json().get('conversion_rates')
    except exceptions.HTTPError:
        output_error('Can\'t get exchange rates from API.')
    except exceptions.ConnectionError:
        output_error('Can\'t get connection to Internet.')
    except Exception:
        output_error('There was an error.')


def from_currency_to(to_currency_name: str, from_currency_value: float, from_currency_name: str) -> float | None:
    '''Exchange from one currency to another requested by the user and return the result'''
    exchange_rate_data = get_exchange_rate_data(from_currency_name)

    try:
        print(f'From {from_currency_name}',exchange_rate_data[from_currency_name])
        print(f'To {to_currency_name}', exchange_rate_data[to_currency_name])
        result = round(from_currency_value * exchange_rate_data[to_currency_name], 2)
    except KeyError:
        output_error('Invalid currency code, Try again.')
    else:
        print(result)
        return result


def to_local_from(currency_value: float, currency_name: str) -> float | None:
    '''Exchange from requested currency to JMD and return the result'''
    try:
        print(f'To {LOCAL_REGION_CURRENCY}', local_exchange_rate[LOCAL_REGION_CURRENCY])
        print(f'From {currency_name}', local_exchange_rate[currency_name])
        result = round(currency_value/local_exchange_rate[currency_name], 2)
    except KeyError:
        output_error('Invalid currency code, Try again.')
    else:
        print(result)
        return result


def from_local_to(currency_name: str, currency_value: float) -> float | None:
    '''Exchange from JMD to requested currency and return the result'''
    try:
        print(f'To {LOCAL_REGION_CURRENCY}', local_exchange_rate[LOCAL_REGION_CURRENCY])
        print(f'From {currency_name}', local_exchange_rate[currency_name])
        print(round(currency_value*local_exchange_rate[currency_name]))
    except KeyError:
        output_error('Invalid currency code, Try again.')
    else:
        return round(currency_value*local_exchange_rate[currency_name], 2)


def exchange():
    '''Does all the necessary reading of text inputs reading and output the result to the user '''

    def output_result(result: str, currency_name: str):
        '''Returns the result to the user as text (as keyboard presses)'''
        bs_count = 8
        kb.press_and_release(','.join(['backspace' for i in range(bs_count)]))
        kb.write(result+' '+currency_name)

    global local_exchange_rate
    # Check if local exchange rate is available and if not a requested is made to get them
    if local_exchange_rate is None:
        local_exchange_rate = get_exchange_rate_data(LOCAL_REGION_CURRENCY)

    # The keyboard recording is stop to get the inputed text and start to record
    inputed_text = ''.join(kb.get_typed_strings(kb.stop_recording()))
    print(inputed_text)
    inputed_text_list = inputed_text.strip().split()
    print(inputed_text_list)
    kb.start_recording()

    print(re.findall(r'\w{3} to \w{3}', inputed_text))

    # Check if there is from and to currency code, and if there is one of a pair of them.
    if 0 < len(re.findall(r'\w{3} to \w{3}', inputed_text)) < 2:
        index = inputed_text_list.index('to')

        try:
            # Check for if there any popular currency in text and make adjustments for it
            from_currency_value = inputed_text_list[index-2]
            for symbol in ('$', '£', '€', '¥', '₩'):
                if symbol in from_currency_value:
                    from_currency_value = float(from_currency_value[from_currency_value.find(symbol)+1:])
                    break
            else:
                from_currency_value = float(inputed_text_list[index-2])

            from_currency_name = inputed_text_list[index-1].upper()
            to_currency_name = inputed_text_list[index+1].upper()

            print(from_currency_value, from_currency_name, to_currency_name)

        except ValueError:
            output_error('Please try again.')

        else:
            # Check if local currency exchange rate data is ask for
            if to_currency_name == LOCAL_REGION_CURRENCY:
                print(1)
                result = to_local_from(from_currency_value, from_currency_name)

            elif from_currency_name == LOCAL_REGION_CURRENCY:
                print(1)
                result = from_local_to(to_currency_name, from_currency_value)

            # If not local exchange rate data is not ask for then,
            # a new request is made for required exchange rate
            else:
                print(0)
                result = from_currency_to(
                    to_currency_name, from_currency_value, from_currency_name)

            if result is not None:
                output_result(str(result), to_currency_name)

    else:
        output_error('More than one request was readed, try again.')


# Create local exchange rate dictionary so that one request can be made at start up
local_exchange_rate = get_exchange_rate_data(LOCAL_REGION_CURRENCY)

kb.start_recording()

# Trigger word used to trigger the exchange funtion to start
TRIGGER_WORD = '!er'
kb.add_word_listener(TRIGGER_WORD, exchange, ['space'], timeout=3)

kb.wait('esc')
