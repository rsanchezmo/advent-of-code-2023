from collections import deque
from abc import abstractmethod
import math 

class Module:
    def __init__(self, name, type_, forward_modules):
        self.name = name
        self.type = type_
        self.forward_modules = forward_modules
        
    @abstractmethod
    def send_signal(self, modules, signal_counter, value, sender_name, queue_pulses):
        pass



class ConjuctionModule(Module):
    def __init__(self, forward_modules, name):
        super().__init__(name, 'conjunction_module', forward_modules)
        self._memory = {}
        self._multi_input_size = 1

    def set_multi_input_size(self, size):
        self._multi_input_size = size

    def send_signal(self, modules, signal_counter, value, sender_name, queue):
        self._memory[sender_name] = value # update the value of that sender memory

        if sum(self._memory.values()) == self._multi_input_size:
            for module in self.forward_modules:
                # print(f'{self.name} [{self.type}] -> {module}: {False}')
                signal_counter['low'] += 1
                if modules.get(module, None) is not None:
                    queue.append((True, self.name, module, False))
                else:
                    queue.append((False, self.name, module, False))
        else:
            for module in self.forward_modules:
                # print(f'{self.name} [{self.type}] -> {module}: {True}')
                signal_counter['high'] += 1

                if modules.get(module, None) is not None:
                   queue.append((True, self.name, module, True))
                else:
                    queue.append((False, self.name, module, True))


class FlipFlopModule(Module):
    def __init__(self, forward_modules, name):
        super().__init__(name, 'flip_flop_module', forward_modules)

        self._status = False # OFF

    def send_signal(self,  modules, signal_counter, value, sender_name, queue):
        if value:
            return
        
        self._status = not self._status # toggle the status

        for module in self.forward_modules:
            # print(f'{self.name} [{self.type}] -> {module}: {self._status}')
            if self._status:
                signal_counter['high'] += 1
            else:
                signal_counter['low'] += 1
            
            if modules.get(module, None) is not None:
                queue.append((True, self.name, module, self._status))
            else:
                queue.append((False, self.name, module, self._status))

class BroadcastModule(Module):
    def __init__(self, forward_modules, name):
        super().__init__(name, 'broadcast_module', forward_modules)

    def send_signal(self, modules, signal_counter, value, sender_name, queue):

        # for module in self.forward_modules:
        #     print(f'{self.name} [{self.type}]-> {module}: {value}')

        for module in self.forward_modules:
            if value:
                signal_counter['high'] += 1
            else:
                signal_counter['low'] += 1

            if modules.get(module, None) is not None:
                queue.append((True, self.name, module, value))
            else:
                queue.append((False, self.name, module, value))

def main():
    with open("./december_20/input.txt") as f:
        lines = f.readlines()


    modules = {}
    for line in lines:
        splitted_line = line.strip().split(' -> ')

        if 'broadcaster' in splitted_line[0]:
            forward_modules = splitted_line[1].split(', ') 
            modules['broadcaster'] = BroadcastModule(forward_modules=forward_modules, name='broadcaster')

        elif '%' in splitted_line[0]:
            name = splitted_line[0].replace('%', '')
            forward_modules = splitted_line[1].split(', ') 
            modules[name] = FlipFlopModule(forward_modules=forward_modules, name=name)

        elif '&' in splitted_line[0]:
            forward_modules = splitted_line[1].split(', ')
            name = splitted_line[0].replace('&', '')
            modules[name] = ConjuctionModule(forward_modules=forward_modules, name=name)

    rx_prev_module = None
    for module in modules.keys():
        if isinstance(modules[module], ConjuctionModule):
            count = 0
            for values in modules.values():
                if module in values.forward_modules:
                    count += 1
            modules[module].set_multi_input_size(count)

        if modules[module].forward_modules == ['rx']:
            rx_prev_module = module

    signal_counter = {'low': 0, 'high': 0}
    initial_module = 'broadcaster'
    queue_pulses = deque()
    for _ in range(1000):
        signal_counter['low'] += 1
        sender = 'init_button'
        queue_pulses.append((True, sender, initial_module, False))
        # print(f'button [initial_module] -> {initial_module}: {False}')

        while queue_pulses:
            process, sender, module_name, value = queue_pulses.popleft()
            if process:
                modules[module_name].send_signal(modules, signal_counter, value, sender, queue_pulses) # press button once
                

    print(f'Part 1: {signal_counter["low"] * signal_counter["high"]}, L: {signal_counter["low"]}, H: {signal_counter["high"]}, Total: {signal_counter["low"] + signal_counter["high"]}')
    

    # Part 2
    print("rx_prev_module", rx_prev_module)
    print(modules[rx_prev_module]._multi_input_size)  # as it is a conjuction module
    # if i want to receive a low signal in rx, then the prev module, as it is a conjunction module, must have all the inputs low
    # i should count when i get a 1 on each an then compute the GCD

    count_presses = 0
    signal_counter = {'low': 0, 'high': 0}
    initial_module = 'broadcaster'
    queue_pulses = deque()
    stop = False

    senders = {}  # there are actually four senders to the rx_prev_module
    while not stop:
        count_presses += 1
        signal_counter['low'] += 1
        sender = 'init_button'
        queue_pulses.append((True, sender, initial_module, False))
        # print(f'button [initial_module] -> {initial_module}: {False}')

        while queue_pulses:
            process, sender, module_name, value = queue_pulses.popleft()

            if module_name == rx_prev_module and value:

                if sender not in senders.keys():
                    senders[sender] = count_presses + 1000

                if len(senders) == modules[rx_prev_module]._multi_input_size:
                    lcm = math.lcm(*senders.values())
                    print(f'Part 2: Cycles {lcm}')
                    exit(0)

            if process:
                modules[module_name].send_signal(modules, signal_counter, value, sender, queue_pulses) # press button once
            else:
                if module_name == 'rx' and not value:
                    stop = True  # brute force solution

    print(f'Part 2: Cycles {count_presses}')

if __name__ == "__main__":
    main()