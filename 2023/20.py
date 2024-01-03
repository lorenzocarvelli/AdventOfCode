from base import DailyPuzzle


MODULES = []
QUEUE = []
TOTAL_LOW_PULSES = 0
TOTAL_HIGH_PULSES = 0


def get_module(module_name: str):
    try:
        return [m for m in MODULES if m.name == module_name][0]
    except IndexError:
        return None


class Module(object):

    def __init__(self, name: str, receivers: list):
        self.name: str = name
        self.receivers: list = receivers

    def receive(self, p: int, connected_input):
        pass

    def send(self, p: int):

        for rr in self.receivers:
            if type(get_module(rr)) == Conjunction:
                QUEUE.append((rr, p, self.name))
                self.record_pulse(p)

                continue
            QUEUE.append((rr, p))
            self.record_pulse(p)

    @staticmethod
    def record_pulse(p):
        global TOTAL_LOW_PULSES, TOTAL_HIGH_PULSES

        if p == 0:
            TOTAL_LOW_PULSES += 1
        elif p == 1:
            TOTAL_HIGH_PULSES += 1


class FlipFlop(Module):
    def __init__(self, name: str, receivers: list):
        super().__init__(name, receivers)
        self.state: int = 0

    def flip(self):
        if self.state == 0:
            self.state = 1
        else:
            self.state = 0

        self.send(self.state)

    def receive(self, p: int, connected_input=None):
        if p == 1:
            return
        self.flip()


class Conjunction(Module):
    def __init__(self, name: str, receivers: list):
        super().__init__(name, receivers)
        self.inputs_connected: list = []
        self.memory = dict()

    def add_connected_inputs(self, inputs_connected: list):
        self.inputs_connected = inputs_connected
        self.memory = self.reset()

    def reset(self) -> dict:
        return {ic: 0 for ic in self.inputs_connected}

    def receive(self, p: int, connected_input):
        self.memory[connected_input] = p

        all_high = True
        for ci, pulse in self.memory.items():
            if pulse == 0:
                all_high = False
                break

        if all_high:
            self.send(0)
            return
        self.send(1)


class Broadcaster(Module):
    def __init__(self, name: str, receivers: list):
        super().__init__(name, receivers)

    def receive(self, p: int, connected_input=None):
        self.send(p)


class Button(Module):
    def __init__(self, name: str, receivers: list):
        super().__init__(name, receivers)

    def push(self):
        self.send(0)


class Day20(DailyPuzzle):
    def __init__(self):
        super().__init__("2023", "20")
        self.rx_first_low_pulse_counter: int = -100
        self.mock_data = [
            "broadcaster -> a, b, c",
            "%a -> b",
            "%b -> c",
            "%c -> inv",
            "&inv -> a"
        ]

    def solve(self):
        global QUEUE
        button = Button("button", ["broadcaster"])

        # Parsing data
        for ll in self.data:
            name_receivers = ll.split(" -> ")
            m_name = name_receivers[0]
            receivers = [f.strip() for f in name_receivers[1].split(",")]

            if m_name == "broadcaster":
                MODULES.append(Broadcaster(m_name, receivers))

            elif m_name.startswith("%"):
                MODULES.append(FlipFlop(m_name[1:], receivers))

            elif m_name.startswith("&"):
                MODULES.append(Conjunction(m_name[1:], receivers))

            else:
                raise

        # Getting connected inputs for conjunction modules
        conjunction_modules = [m.name for m in MODULES if type(m) == Conjunction]
        for cm in conjunction_modules:
            c_module = get_module(cm)
            input_modules = []
            for mm in MODULES:
                if cm in mm.receivers:
                    input_modules.append(mm.name)

            c_module.add_connected_inputs(input_modules)

        for iii in range(100000000):
            # Processing for a button push
            button.push()
            while len(QUEUE):
                current_iteration = QUEUE
                QUEUE = []
                for iter_tuple in current_iteration:
                    if len(iter_tuple) == 2:
                        receiver, pulse = iter_tuple
                        self.check_for_rx_low_pulse(receiver, pulse, iii)
                        module_receiver = get_module(receiver)
                        if module_receiver is not None:
                            module_receiver.receive(pulse)
                        continue

                    receiver, pulse, sender = iter_tuple
                    self.check_for_rx_low_pulse(receiver, pulse, iii)

                    module_receiver = get_module(receiver)
                    if module_receiver is not None:
                        module_receiver.receive(pulse, sender)

            if iii == 1000:
                print(TOTAL_HIGH_PULSES * TOTAL_LOW_PULSES)  # Part 1

            if self.rx_first_low_pulse_counter != -100:
                break

        print(self.rx_first_low_pulse_counter)  # Part 2

    def check_for_rx_low_pulse(self, receiver: str, pulse: int, iteration: int):
        if receiver == "rx" and pulse == 0 and self.rx_first_low_pulse_counter == -100:
            self.rx_first_low_pulse_counter = iteration


if __name__ == "__main__":
    day_20 = Day20()
    day_20.solve()
