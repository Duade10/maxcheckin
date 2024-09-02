from datetime import datetime
import re


def make_excel_correction_substation(substation: str) -> str:
    """
    Make a correction to the given data by replacing it with a predefined value.

    Parameters:
        data (str): The data to be corrected.

    Returns:
        str: The corrected data.

    Description:
        This function takes a string `data` as input and checks if it matches any of the keys in the `corrections` dictionary.
        If a match is found, the corresponding value is returned. Otherwise, the original `data` is returned.

        The `corrections` dictionary contains key-value pairs where the keys are the original values and the values are the corrected values.

        Example usage:
        ```
        corrected_data = make_excel_correction_substation('oshogbo')
        print(corrected_data)  # Output: 'OSOGBO'
        ```
        :param substation:
    """
    corrections = {
        'oshogbo': 'OSOGBO',
        'ilesha': 'ILESA',
        'ado ekiti': 'ADO',
    }

    return corrections.get(substation.lower(), substation)


def make_excel_correction_132(data: str):
    """
    Make a correction to the given data by replacing it with a predefined value.

    Parameters:
        data (str): The data to be corrected.

    Returns:
        str: The corrected data.

    Description:
        This function takes a string `data` as input and checks if it matches any of the keys in the `corrections` dictionary.
        If a match is found, the corresponding value is returned. Otherwise, the original `data` is returned.

        The `corrections` dictionary contains key-value pairs where the keys are the original values and the values are the corrected values.

        Example usage:
        ```
        corrected_data = make_excel_correction_132('EDE WATER')
        print(corrected_data)  # Output: 'WWKS EDE'
        ```
    """
    corrections = {
        'EDE WATER': 'WWKS EDE',
        'OSOGBO/IKIRUN': 'OSOGBO/ IKIRUN',
        'STEEL ROLLING MILL': 'SRM',
        'NIGERIA MACHINE TOOLS': 'NMT',
        'POWER LINE': 'POWERLINE',
        'IBOKUN': 'IBOKUN',
        'IPETU-IJESA': 'IPETU-JESA'
    }

    return corrections.get(data, data)


def calculate_time_difference(start_date_str, start_time_str, end_date_str, end_time_str):
    # Parse date and time strings into datetime objects
    start_datetime = datetime.strptime(start_date_str + ' ' + start_time_str, '%d/%m/%Y %H:%M')
    end_datetime = datetime.strptime(end_date_str + ' ' + end_time_str, '%d/%m/%Y %H:%M')

    # Calculate the difference in hours
    time_difference = (end_datetime - start_datetime).total_seconds() / 3600

    return time_difference


def get_correct_fault(fault) -> str | None:
    """
    Returns the correct fault code based on the given fault string.

    Parameters:
        fault (str): The fault string to be checked.

    Returns:
        str or None: The corresponding correct fault code if found, otherwise None.
    """
    fault_dict = {
        'inst oc (disco)': 'INST OC',
        'ef (disco)': 'E/F',
        'oc (disco)': 'O/C',
        'inst oc/ef (disco)': 'INST OC/EF',
        'oc/ef (disco)': 'OC/EF',
        'inst ef (disco)': 'INST E/F'
    }
    return fault_dict.get(str(fault).lower(), None)


def format_remarks(remarks: str) -> str:
    remarks_dict = {
        'TRIAL RECLOSURE': 'A TRIAL RECLOSURE WAS MADE AND STAYED',
    }

    return remarks_dict.setdefault(remarks.upper(), remarks.upper())


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
    """
    Format the substation name by removing '132kv' if present and converting to uppercase.

    Args:
        substation (str): The substation name to be formatted.

    Returns:
        str: The formatted substation name.
    """
    result = make_excel_correction_132(substation.lower().replace('132kv', '').upper())

    return result


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


def extract_google_sheet_id(url):
    pattern = r'^https?://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None
