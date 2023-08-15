from device.device import Device


def build_report(filename: str) -> dict:
    with open(filename) as f:
        devices = {}
        for line in f.readlines():
            if 'BIG' in line:
                data_part = line.split("'")[1]
                elements = data_part.split(';')
                device_id = elements[2]
                if device_id not in devices:
                    devices[device_id] = Device(device_id)
                device = devices[device_id]
                device.check_state(state=elements[-2], sp1=elements[6], sp2=elements[-6])

    return devices


def print_report(data: dict) -> None:
    print(f'All big messages:{len(data)}')

    error_devices = {
        device_id: data.pop(device_id)
        for device_id, device in data.copy().items()
        if not device.states_count
    }

    print(f'Successful big messages:{len(data)}')
    print(f'Failed big messages:{len(error_devices)}\n')

    if error_devices:
        for device in error_devices.values():
            print(device)

    if data:
        print('\nSuccess messages count:')
        for device in data.values():
            print(device)


def main():
    parsed_data = build_report('app_2.log')
    print_report(parsed_data)


if __name__ == '__main__':
    main()
