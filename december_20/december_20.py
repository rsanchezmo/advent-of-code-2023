
from abc import abstractmethod

class Module:
    def __init__(self, name, type_, forward_modules):
        self.name = name
        self.type = type_
        self.forward_modules = forward_modules
        
    @abstractmethod
    def send_signal(self, modules, signal_counter, value, sender_name):
        pass



class ConjuctionModule(Module):
    def __init__(self, forward_modules, name):
        super().__init__(name, 'conjunction_module', forward_modules)
        self._memory = {}

    def send_signal(self, modules, signal_counter, value, sender_name):
        self._memory[sender_name] = value # update the value of that sender memory

        if sum(self._memory.values()) == len(self._memory.keys()):
            for module in self.forward_modules:
                print(f'{self.name} [{self.type}] -> {module}: {False}')
                signal_counter['low'] += 1
                if modules.get(module, None) is not None:
                    modules[module].send_signal(modules, signal_counter, False, self.name)
        else:
            for module in self.forward_modules:
                print(f'{self.name} [{self.type}] -> {module}: {True}')
                signal_counter['high'] += 1

                if modules.get(module, None) is not None:
                    modules[module].send_signal(modules, signal_counter, True, self.name)


class FlipFlopModule(Module):
    def __init__(self, forward_modules, name):
        super().__init__(name, 'flip_flop_module', forward_modules)

        self._status = False # OFF

    def send_signal(self,  modules, signal_counter, value, sender_name):
        if value:
            return
        
        self._status = not self._status # toggle the status

        for module in self.forward_modules:
            print(f'{self.name} [{self.type}] -> {module}: {self._status}')
            if self._status:
                signal_counter['high'] += 1
            else:
                signal_counter['low'] += 1
            
            if modules.get(module, None) is not None:
                modules[module].send_signal(modules, signal_counter, self._status, self.name)  # send the new signal to the next module


class BroadcastModule(Module):
    def __init__(self, forward_modules, name):
        super().__init__(name, 'broadcast_module', forward_modules)

    def send_signal(self, modules, signal_counter, value, sender_name):

        for module in self.forward_modules:
            print(f'{self.name} [{self.type}]-> {module}: {value}')

        for module in self.forward_modules:
            if value:
                signal_counter['high'] += 1
            else:
                signal_counter['low'] += 1

            if modules.get(module, None) is not None:
                modules[module].send_signal(modules, signal_counter, value, self.name)

def main():
    with open("./december_20/test2.txt") as f:
        lines = f.readlines()


    modules = {}
    signal_counter = {'low': 0, 'high': 0}
    initial_module = None
    for line in lines:
        splitted_line = line.strip().split(' -> ')

        if 'broadcaster' in splitted_line[0]:
            forward_modules = splitted_line[1].split(', ') 
            modules['broadcaster'] = BroadcastModule(forward_modules=forward_modules, name='broadcaster')

            if initial_module is None:
                initial_module = 'broadcaster'
        elif '%' in splitted_line[0]:
            name = splitted_line[0].replace('%', '')
            forward_modules = splitted_line[1].split(', ') 
            modules[name] = FlipFlopModule(forward_modules=forward_modules, name=name)

            if initial_module is None:
                initial_module = name

        elif '&' in splitted_line[0]:
            forward_modules = splitted_line[1].split(', ')
            name = splitted_line[0].replace('&', '')
            modules[name] = ConjuctionModule(forward_modules=forward_modules, name=name)

            if initial_module is None:
                initial_module = name


    for _ in range(1):
        signal_counter['low'] += 1
        modules[initial_module].send_signal(modules, signal_counter, False, 'init')  # press button once

    print(f'Part 1: {signal_counter["low"] * signal_counter["high"]}, L: {signal_counter["low"]}, H: {signal_counter["high"]}, Total: {signal_counter["low"] + signal_counter["high"]}')


if __name__ == "__main__":
    main()