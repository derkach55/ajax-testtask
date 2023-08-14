LOG_FILE = 'app_2.log'

ERRORS_MAP = {
    1: 'Battery device error',
    2: 'Temperature device error',
    3: 'Threshold central error'
}


def get_error_message(sp1: str, sp2: str) -> str:
    state = sp1[:-1] + sp2
    errors_binaries = [bin(int(state[i:i + 2])) for i in range(0, len(state), 2)]
    errors = [i[-4] if len(i) > 5 else 0 for i in errors_binaries]
    return [ERRORS_MAP[i + 1] for i in range(3) if errors[i] == '1']


def build_report(filename: str) -> dict:
    with open(filename) as f:
        devices = {}

        for line in f.readlines():
            if 'BIG' in line:
                data_part = line.split("'")[1]
                elements = data_part.split(';')
                device_id = elements[2]
                state = elements[-2]

                if state == '02':
                    if device_id not in devices:
                        devices[device_id] = 1
                    elif isinstance(devices[device_id], int):
                        devices[device_id] += 1
                else:
                    devices[device_id] = get_error_message(elements[6], elements[-6])

    return devices


def print_report(data: dict) -> None:
    print(f'All big messages:{len(data)}')

    error_devices = {
        device: data.pop(device)
        for device, states_count in data.copy().items()
        if not isinstance(states_count, int)
    }

    print(f'Successful big messages:{len(data)}')
    print(f'Failed big messages:{len(error_devices)}\n')

    if error_devices:
        for device, errors in error_devices.items():
            errors = ', '.join(errors) if errors else 'Unknown device error'
            print(f"{device}: {errors}")

    if data:
        print('\nSuccess messages count:')
        for device, states_count in data.items():
            print(f'{device}: {states_count}')


def main():
    parsed_data = build_report(LOG_FILE)
    print_report(parsed_data)


if __name__ == '__main__':
    main()
