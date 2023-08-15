class Device:
    def __init__(self, device_id: str):
        self.device_id = device_id
        self.states_count = 0
        self.error_messages = []

    def check_state(self, state: str, sp1: str, sp2: str) -> None:
        if state == '02':
            if self.states_count is not None:
                self.states_count += 1
        else:
            self.states_count = None
            self.set_error_message(sp1, sp2)

    def set_error_message(self, sp1: str, sp2: str) -> None:
        errors = {
            1: 'Battery device error',
            2: 'Temperature device error',
            3: 'Threshold central error'
        }
        state = sp1[:-1] + sp2

        # split previous result into pairs and convert it to binary form
        errors_binaries = [bin(int(state[i:i + 2])) for i in range(0, len(state), 2)]

        # of the resulting bit fields, leaves only fifth flags
        device_errors = [i[-4] if len(i) > 5 else 0 for i in errors_binaries]

        # mapping errors with flags
        messages = [errors[i + 1] for i in range(3) if device_errors[i] == '1']

        for message in messages:
            if message not in self.error_messages:
                self.error_messages.append(message)

    def get_error_message(self) -> str:
        message = ', '.join(self.error_messages) if self.error_messages else 'Unknown device error'
        return message

    def __str__(self) -> str:
        if self.states_count is not None:
            return f'{self.device_id}: {self.states_count}'
        return f'{self.device_id}: {self.get_error_message()}'
