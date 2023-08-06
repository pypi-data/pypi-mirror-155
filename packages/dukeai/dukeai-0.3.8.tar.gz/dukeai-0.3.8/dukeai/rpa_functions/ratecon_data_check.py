from colorama import Fore
import traceback


def check_rate_con_data(rate_con):
    try:
        data_check_passed = True
        if type(rate_con['shipment']) == dict:
            if rate_con['shipment']['charges'] is None:
                print(Fore.RED + f"[FAILED]['DATA-CHECK'][SHIPMENT-CHARGES][{type(rate_con['shipment']['charges'])}]" + Fore.BLACK)
                data_check_passed = False

            if rate_con['shipment']['distance'] is None:
                print(Fore.RED + f"[FAILED]['DATA-CHECK'][SHIPMENT-DISTANCE][{type(rate_con['shipment']['distance'])}]" + Fore.BLACK)
                data_check_passed = False

            if rate_con['shipment']['volume'] is None:
                print(Fore.RED + f"[FAILED]['DATA-CHECK'][SHIPMENT-VOLUME][{type(rate_con['shipment']['volume'])}]" + Fore.BLACK)
                data_check_passed = False

        if type(rate_con['shipment']) != dict:
            print(Fore.RED + f"[FAILED]['DATA-CHECK'][SHIPMENT][{type(rate_con['shipment'])}]" + Fore.BLACK)
            data_check_passed = False

        if type(rate_con['receiver']) != dict:
            print(Fore.RED + f"[FAILED]['DATA-CHECK'][RECEIVER][{type(rate_con['receiver'])}]" + Fore.BLACK)
            data_check_passed = False

        if type(rate_con['sender']) != str:
            print(Fore.RED + f"[FAILED]['DATA-CHECK'][SENDER][{type(rate_con['sender'])}]" + Fore.BLACK)
            data_check_passed = False

        if type(rate_con['client']) != str:
            print(Fore.RED + f"[FAILED]['DATA-CHECK'][CLIENT][{type(rate_con['client'])}]" + Fore.BLACK)
            data_check_passed = False

        if type(rate_con['entities']) == list:
            for entity in rate_con['entities']:
                if type(entity['name']) != str:
                    print(Fore.RED + f"[FAILED]['DATA-CHECK'][ENTITIES][NAME][{type(entity['name'])}]" + Fore.BLACK)
                    data_check_passed = False

                if type(entity['city']) != str:
                    print(Fore.RED + f"[FAILED]['DATA-CHECK'][ENTITIES][CITY][{type(entity['city'])}]" + Fore.BLACK)
                    data_check_passed = False

                if type(entity['state']) != str:
                    print(Fore.RED + f"[FAILED]['DATA-CHECK'][ENTITIES][STATE][{type(entity['state'])}]" + Fore.BLACK)
                    data_check_passed = False

                if type(entity['postal']) != str:
                    print(Fore.RED + f"[FAILED]['DATA-CHECK'][ENTITIES][POSTAL][{type(entity['postal'])}]" + Fore.BLACK)
                    data_check_passed = False

        if type(rate_con['stops']) == list:
            if len(rate_con['stops']) > 0:
                for stop in rate_con['stops']:
                    if type(stop['_stoptype']) != str:
                        print(Fore.RED + f"[FAILED]['DATA-CHECK'][STOP][_STOP-TYPE][{type(stop['_stoptype'])}]" + Fore.BLACK)
                        data_check_passed = False

                    if type(stop['stoptype']) != str:
                        print(Fore.RED + f"[FAILED]['DATA-CHECK'][STOP][STOP-TYPE][{type(stop['stoptype'])}]" + Fore.BLACK)
                        data_check_passed = False

                    if type(stop['order_detail']) == list:
                        if len(stop['order_detail']) < 1:
                            print(Fore.RED + f"[FAILED]['DATA-CHECK'][STOP][NO-order_detail][{len(stop['order_detail'])}]" + Fore.BLACK)
                            data_check_passed = False

                    if type(stop['dates']) == list:
                        if len(stop['dates']) < 1:
                            print(Fore.RED + f"[FAILED]['DATA-CHECK'][STOP][NO-STOP-DATES][{len(stop['dates'])}]" + Fore.BLACK)
                            data_check_passed = False

                    for entity in stop['entities']:
                        # if type(entity['address']) == list:
                        #     if len(entity['address']) == 0:
                        #         print(Fore.RED + f"[FAILED]['DATA-CHECK'][ENTITIES][Address-Length][{type(entity['address'])}]" + Fore.BLACK)
                        #         data_check_passed = False

                        if type(entity['name']) != str:
                            print(Fore.RED + f"[FAILED]['DATA-CHECK'][ENTITIES][NAME][{type(entity['name'])}]" + Fore.BLACK)
                            data_check_passed = False

                        if type(entity['city']) != str:
                            print(Fore.RED + f"[FAILED]['DATA-CHECK'][ENTITIES][CITY][{type(entity['city'])}]" + Fore.BLACK)
                            data_check_passed = False

                        if type(entity['state']) != str:
                            print(Fore.RED + f"[FAILED]['DATA-CHECK'][ENTITIES][STATE][{type(entity['state'])}]" + Fore.BLACK)
                            data_check_passed = False

                        if type(entity['postal']) != str:
                            print(Fore.RED + f"[FAILED]['DATA-CHECK'][ENTITIES][POSTAL][{type(entity['postal'])}]" + Fore.BLACK)
                            data_check_passed = False
            else:
                print(Fore.RED + f"[FAILED]['DATA-CHECK'][STOP][NO-STOPS-FOUND][{len(rate_con['stops'])}]" + Fore.BLACK)
                data_check_passed = False

        if type(rate_con['stops']) == list:
            for stop in rate_con['stops']:
                for refs in stop['references']:
                    underscore_idtype = refs['_idtype']
                    if type(underscore_idtype) == str:
                        if len(underscore_idtype) != 2:
                            print(Fore.RED + f"[FAILED]['DATA-CHECK'][STOP][references][Make _idtype two letter word]" + Fore.BLACK)
                    else:
                        print(Fore.RED + f"[FAILED]['DATA-CHECK'][STOP][references][_idtype is not a string]" + Fore.BLACK)

            for stop in rate_con['stops']:
                for note in stop['notes']:
                    underscore_notetype = note['_notetype']
                    if type(underscore_notetype) == str:
                        if len(underscore_notetype) != 2:
                            print(Fore.RED + f"[FAILED]['DATA-CHECK'][STOP][notes][Make _notetype two letter word]" + Fore.BLACK)
                    else:
                        print(Fore.RED + f"[FAILED]['DATA-CHECK'][STOP][notes][_notetype is not a string]" + Fore.BLACK)

        if type(rate_con['notes']) == list:
            for note in rate_con['notes']:
                underscore_notetype = note['_notetype']
                if type(underscore_notetype) == str:
                    if len(underscore_notetype) != 2:
                        print(Fore.RED + f"[FAILED]['DATA-CHECK'][STOP][notes][Make _notetype two letter word]" + Fore.BLACK)
                else:
                    print(Fore.RED + f"[FAILED]['DATA-CHECK'][STOP][notes][_notetype is not a string]" + Fore.BLACK)

        if type(rate_con['references']) == list:
            for refs in rate_con['references']:
                underscore_idtype = refs['_idtype']
                if type(underscore_idtype) == str:
                    if len(underscore_idtype) != 2:
                        print(Fore.RED + f"[FAILED]['DATA-CHECK'][STOP][references][Make _idtype two letter word]" + Fore.BLACK)
                else:
                    print(Fore.RED + f"[FAILED]['DATA-CHECK'][STOP][references][_idtype is not a string]" + Fore.BLACK)

        if data_check_passed is True:
            print(Fore.GREEN + f"[PASSED][ALL-DATA-CHECK]" + Fore.BLACK)
        else:
            print(Fore.RED + f"[FAILED][DATA-CHECK]" + Fore.BLACK)

        return data_check_passed
    except Exception as e:
        data_check_passed = False
        print(Fore.RED + f"[FAILED][RateCon-DataCheck-Error][{e}][{traceback.format_exc()}]" + Fore.BLACK)
        return data_check_passed
