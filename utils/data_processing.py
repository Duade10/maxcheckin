from datetime import datetime


def calculate_time_difference(start_date_str, start_time_str, end_date_str, end_time_str):
    # Parse date and time strings into datetime objects
    start_datetime = datetime.strptime(start_date_str + ' ' + start_time_str, '%d/%m/%Y %H:%M')
    end_datetime = datetime.strptime(end_date_str + ' ' + end_time_str, '%d/%m/%Y %H:%M')

    # Calculate the difference in hours
    time_difference = (end_datetime - start_datetime).total_seconds() / 3600

    return time_difference


def get_correct_fault(fault):
    result = None
    fault = str(fault).lower()
    if fault == 'inst oc (disco)':
        result = 'INST OC'
    elif fault == 'ef (disco)':
        result = 'E/F'
    elif fault == 'oc (disco)':
        result = 'O/C'
    elif fault == 'inst oc/ef (disco)':
        result = 'INST OC/EF'
    elif fault == 'oc/ef (disco)':
        result = 'OC/EF'
    elif fault == 'inst ef (disco)':
        result = 'INST E/F'
    return result


def is_contain_value(value):
    if value is None or value == '':
        return False
    else:
        return True


def join_time(time1, time2):
    time1 = str(time1).split(":")[0]
    time2 = str(time2).split(":")[1]
    result = f"{time1}:{time2}"
    return result


def format_substation_name(substation: str) -> str:
    substation = substation.lower()
    if '132kv' in substation:
        result = substation.replace("132kv", "")
    else:
        result = substation
    result = make_excel_correction_substation(result)
    return f"{result.upper()} T.S"


def format_subregion_name(subregion: str) -> str:
    return subregion.upper()


def format_line_name(line: str) -> str:
    line = line.lower()
    if '33kv' in line:
        result = line.replace('33kv', "")
    else:
        result = line
    return make_excel_correction(result.upper())


def make_excel_correction(data: str):
    if 'EDE WATER' in data:
        data = 'WWKS EDE'
    elif data == 'OSOGBO/IKIRUN':
        data = 'OSOGBO/ IKIRUN'
    elif 'STEEL ROLLING MILL' in data:
        data = 'SRM'
    elif data == 'NIGERIA MACHINE TOOLS':
        data = 'NMT'
    elif 'POWER LINE' in data:
        data = 'POWERLINE'
    elif 'IBOKUN' in data:
        data = 'IBOKUN'
    elif 'IPETU-IJESA' in data:
        data = 'IPETU-JESA'
    return data


def make_excel_correction_substation(substation: str) -> str:
    data = str(substation).upper()
    print(data)
    if 'OSHOGBO' in data:
        substation = 'OSOGBO'
        print(substation)
    elif 'ILESHA' in data:
        substation = 'ILESA'
    elif 'ADO EKITI' in data:
        substation = 'ADO'
    return substation
