from collections import OrderedDict

from pathlib import Path

import toml

from panda3d.core import InputDevice
from panda3d.core import ButtonRegistry
from panda3d.core import Vec2
from panda3d.core import Vec3

from direct.showbase.DirectObject import DirectObject


axis_names = [axis.name for axis in InputDevice.Axis]


class Sensor:
    """A button or axis, and its post-processing flags."""
    mouse_sensors = [
        "mouse_x",
        "mouse_y",
        "mouse_x_delta",
        "mouse_y_delta",
    ]
    delta_sensors = [
        "mouse_x_delta",
        "mouse_y_delta",
    ]

    def __init__(self, config):
        """
        config:
            [sensor]
            [sensor, (flag, argument)]
            [sensor, (flag, argument), <other flags>, ...]
        """
        sensor = config[0]
        flags = config[1:]

        self.sensor = sensor
        if self.sensor in axis_names:
            self.axis = True
        else:
            self.axis = False
        self.mouse_pos = Vec2(0,0)
        self.mouse_delta = Vec2(0,0)

        self.flags = OrderedDict()
        for flag in flags:
            name, arg = flag
            assert name in ['flip', 'scale', 'button<', 'button>', 'exp', 'deadzone']
            if name in ['scale', 'button<', 'button>', 'exp', 'deadzone']:
                arg = float(arg)
            else:
                assert arg == ''
                arg = None
            self.flags[name] = arg

    def get_config(self):
        flags = []
        for (name, arg) in self.flags.items():
            if arg is None:
                arg = ''
            arg = str(arg)
            flags.append((name, arg))
        return [self.sensor] + flags

    def read_raw(self, device):
        """Read the sensor's current state."""
        if not device is None:  # Not a keyboard
            if self.axis:
                axis = device.find_axis(InputDevice.Axis[self.sensor])
                state = axis.value
            else:
                button = device.find_button(self.sensor)
                state = button.pressed
        else:  # Keyboard
            if self.sensor in self.mouse_sensors:
                # Do the actual reading
                if self.sensor in self.mouse_sensors:
                    if base.mouseWatcherNode.has_mouse():
                        mouse_pos = base.mouseWatcherNode.get_mouse()
                        self.mouse_delta = mouse_pos - self.mouse_pos
                        self.mouse_pos = Vec2(mouse_pos)
                print(self.mouse_delta)

                # Interpretation
                if self.sensor in self.delta_sensors:
                    if self.sensor == "mouse_x_delta":
                        state = self.mouse_delta.x
                    else:
                        state = self.mouse_delta.y
                else:
                    if self.sensor == "mouse_x":
                        state = self.mouse_pos.x
                    else:
                        state = self.mouse_pos.y
            else:
                button = ButtonRegistry.ptr().find_button(self.sensor)
                state = base.mouseWatcherNode.is_button_down(button)
        return state

    def read(self, device):
        """Read and post-process the sensor's current state."""
        state = self.read_raw(device)
        if state is not None:
            for name, arg in self.flags.items():
                if name == 'flip':
                    state *= -1
                elif name == 'scale':
                    state *= arg
                elif name == 'button<':
                    state = state <= arg
                elif name == 'button>':
                    state = state >= arg
                elif name == 'exp':
                    state = (abs(state) ** arg) * (state / abs(state))
                elif name == 'deadzone':
                    if abs(state) < arg:
                        state = 0.0

        return state


class Mapping:
    """
    A mapping is a set of sensors, and corresponds to an input
    definition line in the configuration file, e.g.

        spatial_mouse   yaw:flip:scale=3,pitch:scale=2
    """
    def __init__(self, config):
        sensor_configs = list(config)
        self.sensors = [Sensor(s_config) for s_config in sensor_configs]

    def get_config(self):
        return tuple(sensor.get_config() for sensor in self.sensors)

    def read(self, device):
        states = [sensor.read(device) for sensor in self.sensors]
        return states

    def freeze_state(self, device):
        for sensor in self.sensors:
            sensor.freeze_state(device)


class VirtualInput:
    """
    A game logic input within an input context. It has a name, a type
    (e.g. `button` or `axis2d´), and an order in which devices will be
    checked for their current state. In a configuration file, it looks
    like this...

        [context.name_of_virtual_input]
        _type = "button"
        _device_order = ["gamepad", "keyboard"]

    ...followed by the mappings for the devices mentioned in the device
    order, and their sensors.
    """
    def __init__(self, config):
        (_type, _device_order) = config
        self.type = _type
        if _type.startswith('repeater'):  # Decompose
            specs = _type.partition(':')
            assert len(specs) == 3
            assert specs[0] == 'repeater'
            self.type = 'repeater'
            specs = specs[2].partition(',')
            assert len(specs) == 3
            assert float(specs[0]) > 0.0
            assert float(specs[2]) > 0.0
            self.first_cooldown = float(specs[0])
            self.later_cooldown = float(specs[2])
        self.mappings = [
            (device, Mapping(filters))
            for device, filters in _device_order
        ]

        self.last_state = None  # Stored state for triggers
        self.cooldown = None  # Remaining time for repeaters
        self.initial = None  # Is this first period for the repeater?

    def get_config(self):
        if not self.type.startswith('repeater'):
            type_string = self.type
        else:
            type_string = f'{self.type}:{self.first_cooldown}:{self.later_cooldown}'
        mappings = [(device, mapping.get_config()) for (device, mapping) in self.mappings]
        return (type_string, mappings)

    def read(self, devices, dt=None):
        final_state = None
        for device, mapping in self.mappings:
            input_state = None
            input_active = False

            # Read the device
            if device in devices:
                input_state = mapping.read(devices[device])
            elif device == 'keyboard':
                input_state = mapping.read(None)
            else:
                continue

            # Process the input state
            if input_state is not None:
                if all(s is None for s in input_state):
                    input_state = None
                elif self.type in ['button', 'trigger', 'repeater']:
                    if len(input_state) == 1 and isinstance(input_state[0], bool):
                        input_state = input_state[0]
                    else:
                        raise Exception("Uninterpretable virtual state")
                    if input_state:
                        input_active = True
                elif self.type == 'axis':
                    if len(input_state) == 1 and isinstance(input_state[0], float):
                        input_state = input_state[0]
                    elif isinstance(input_state, list):
                        # [bool, bool] -> float
                        assert len(input_state) == 2
                        assert all(isinstance(e, bool) for e in input_state)
                        v = 0
                        if input_state[0]:
                            v -= 1
                        if input_state[1]:
                            v += 1
                        input_state = v
                    else:
                        raise Exception("Uninterpretable virtual state")
                    if input_state != 0.0:
                        input_active = True
                elif self.type == 'axis2d':
                    if len(input_state) == 2:
                        input_state = Vec2(*input_state)
                    elif len(input_state) == 4:
                        assert all(isinstance(e, bool) for e in input_state)
                        x, y = 0, 0
                        if input_state[0]:
                            x -= 1
                        if input_state[1]:
                            x += 1
                        if input_state[2]:
                            y -= 1
                        if input_state[3]:
                            y += 1
                        input_state = Vec2(x, y)
                    else:
                        raise Exception("Uninterpretable virtual state")
                    if input_state != Vec2(0.0, 0.0):
                        input_active = True
                elif self.type == 'axis3d':
                    if len(input_state) == 3:
                        input_state = Vec3(*input_state)
                    elif len(input_state) == 6:
                        assert all(isinstance(e, bool) for e in input_state)
                        x, y,z = 0, 0, 0
                        if input_state[0]:
                            x -= 1
                        if input_state[1]:
                            x += 1
                        if input_state[2]:
                            y -= 1
                        if input_state[3]:
                            y += 1
                        if input_state[4]:
                            z -= 1
                        if input_state[5]:
                            z += 1
                        input_state = Vec3(x, y, z)
                    else:
                        raise Exception("Uninterpretable virtual state")
                    if input_state != Vec3(0.0, 0.0, 0.0):
                        input_active = True
                else:
                    raise Exception("Uninterpretable virtual state")

            # What do with this input state?
            if input_active:
                final_state = input_state
                break
            else:
                if final_state is None:
                    final_state = input_state

        # Input types that depend on previous information need to be
        # processed further.
        if self.type == 'trigger':
            button_state = final_state
            final_state = None
            if button_state is not None:
                if button_state and not self.last_state:
                    final_state = True  # Trigger has been pressed
                elif button_state and self.last_state:
                    final_state = False  # Trigger held pressed
                elif not button_state:
                    final_state = False  # Trigger released or idle
            self.last_state = button_state
        elif self.type == 'repeater':
            if self.cooldown is not None:
                self.cooldown -= dt
            button_state = final_state
            final_state = None

            if button_state is None or not button_state:
                self.cooldown = None
                final_state = button_state
            else:
                if self.cooldown is None:
                    self.cooldown = self.first_cooldown
                    final_state = True
                elif self.cooldown <= 0.0:
                    self.cooldown += self.later_cooldown
                    final_state = True
                else:
                    final_state = False

        # NOW we are done.
        return final_state


class Context:
    def __init__(self, config):
        self.virtual_inputs = {
            input_name: VirtualInput(config[input_name])
            for input_name in config.keys()
        }

    def get_config(self):
        return {
            name: virtual_input.get_config()
            for name, virtual_input in self.virtual_inputs.items()
        }

    def read(self, devices, dt=None):
        result = {
            name: virtual_input.read(devices, dt=dt)
            for name, virtual_input in self.virtual_inputs.items()
        }
        return result

    def freeze_state(self, devices):
        for _name, virtual_input in self.virtual_inputs.items():
            virtual_input.freeze_state(devices)


class LastConnectedAssigner:
    def __init__(self):
        self.device = None

    def connect(self, device):
        if self.device is None:
            self.device = device
            base.attach_input_device(device, prefix="")
            print("Assigned {}".format(device))

    def disconnect(self, device):
        if device == self.device:
            self.device = None
            base.detach_input_device(device)
            print("No assigned devices")

    def get_devices(self, user=None):
        if self.device is None:
            return [] # FIXME: keyboard
        else:
            full_id = self.device.device_class.name
            return {full_id: self.device}

    def get_users(self):
        return [None]


class SinglePlayerAssigner:
    def __init__(self):
        self.devices = {}
        for device in base.devices.get_devices():
            self.connect(device)

    def connect(self, device):
        dev_class = device.device_class.name
        if dev_class in self.devices:
            self.disconnect(self.devices[dev_class])
        base.attach_input_device(device, prefix="")
        self.devices[dev_class] = device

    def disconnect(self, device):
        dev_class = device.device_class.name
        print(dev_class, self.devices[dev_class])
        if device == self.devices[dev_class]:
            base.detach_input_device(device)
            del self.devices[dev_class]
        from pprint import pprint
        pprint(self.devices)

    def get_devices(self, user=None):
        return self.devices

    def get_users(self):
        return [None]


class DeviceListener(DirectObject):
    """
    Receives connection / disconnection events and informs the assigner

    :assigner:
        FIXME
    :task:
        Creates a task on creation (at sort -10) that reads the state.
    """
    def __init__(self, assigner, config=None, config_file='keybindings.config',
                 task=True, task_args=None,
                 debug=False):
        self.state = {}  # user: state
        self.debug = debug

        self.config_file = None
        if config is None:
            self.config_file = config_file
            main_dir = Path(base.main_dir)
            config_file = Path(config_file)
            with open(main_dir / config_file, 'r') as f:
                config = parse_config(f.read())
        self.read_config(config)
        self.assigner = assigner
        self.accept("connect-device", self.connect)
        self.accept("disconnect-device", self.disconnect)

        if task:
            if task_args is None:
                task_args = dict(sort=-10)
            base.task_mgr.add(
                self.freeze_state,
                "device_listener",
                **task_args,
            )

    def connect(self, device):
        """Event handler that is called when a device is discovered."""

        if self.debug:
            print("{} found".format(device.device_class.name))
        self.assigner.connect(device)

    def disconnect(self, device):
        """Event handler that is called when a device is removed."""

        if self.debug:
            print("{} disconnected".format(device.device_class.name))
        self.assigner.disconnect(device)

    def read_config(self, config):
        self.contexts = {
            context_name: Context(config[context_name])
            for context_name in config.keys()
        }

    def write_config(self):
        config = serialize_config(self.get_config())
        if self.config_file is not None:
            main_dir = Path(base.main_dir)
            config_file = Path(self.config_file)
            with open(main_dir / config_file, 'w') as f:
                f.write(config)
            print("config file written")

    def get_config(self):
        return {name: context.get_config() for name, context in self.contexts.items()}

    def read(self, user=None, dt=None):
        """
        Read the current state of all contexts, and store the result.
        """
        if dt is None:
            dt = globalClock.dt
        devices = self.assigner.get_devices(user)
        user_state = {
            context_name: context.read(devices, dt=dt)
            for context_name, context in self.contexts.items()
        }
        self.state[user] = user_state

    def read_context(self, context, user=None):
        """
        Retrieve a context's stored state.
        """
        assert context in self.contexts
        return self.state[user][context]

    def freeze_state(self, task, dt=None):
        users = self.assigner.get_users()
        contexts = self.contexts.keys()
        for user in users:
            self.read(user=user, dt=dt)
        return task.cont


def parse_config(config_text):
    input_types = [
        'button',
        'trigger',
        'repeater',
        'axis',
        'axis2D',
        'axis3D',
    ]
    config = {}
    config_lines = config_text.splitlines()
    context_name = None
    virtual_input_name = None
    virtual_input_type = None
    for config_line in config_lines:
        if config_line.startswith('context '):
            _, _, context_name = config_line.partition(' ')
            context_name = context_name.strip()
            assert context_name not in config, f"Context name '{context_name}' used multiple times."
            config[context_name] = {}
        elif any(config_line.startswith(f'  {it}') for it in input_types):
            config_line = config_line.strip()
            virtual_input_type, _, virtual_input_name = config_line.partition(' ')
            virtual_input_name = virtual_input_name.strip()
            assert context_name is not None, f"Virtual input {virtual_input_name} declared before any context."
            config[context_name][virtual_input_name] = (virtual_input_type, [])
        else:
            assert config_line.startswith('    '), f"Indentation on mapping: {config_line}"
            config_line = config_line.strip()
            device_name, _, mapping_string = config_line.partition(' ')
            sensor_strings = [sensor_string.strip()
                              for sensor_string in mapping_string.strip().split(' ')]
            sensors = []
            for sensor_string in sensor_strings:
                elements = sensor_string.split(':')
                sensor = [elements[0]]
                for element in elements[1:]:
                    flag, _, arg = element.partition('=')
                    sensor.append((flag, arg))
                sensors.append(sensor)
            (_, mappings) = config[context_name][virtual_input_name]
            mappings.append((device_name, tuple(sensors)))
    return config


def serialize_config(config):
    config_string = ''
    for context, virtual_input in config.items():
        config_string += f'Context {context}\n'
        for virtual_input_name, (virtual_input_type, mappings) in virtual_input.items():
            config_string += f'  {virtual_input_type} {virtual_input_name}\n'
            for (device, sensors) in mappings:
                sensors_strings = []
                for sensor in sensors:
                    sensor_strings = [sensor[0]]
                    for (flag, arg) in sensor[1:]:
                        sensor_strings.append('='.join([flag, arg]))
                    sensors_strings.append(':'.join(sensor_strings))
                sensors_string = ' '.join(sensors_strings)
                config_string += f'    {device:15}    {sensors_string}\n'
    return config_string


def add_device_listener(assigner=None, config=None,
                        task=None, task_args=None):
    if assigner is None:
        assigner = LastConnectedAssigner()
    args = {}
    if config is not None:
        args['config'] = config
    if task is not None:
        args['task'] = task
    if task_args is not None:
        args['task_args'] = task_args
    base.device_listener = DeviceListener(assigner, **args)
