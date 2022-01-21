"""
This file includes a number of helper functions for the main loop of the carla simulator.
This includes printing measurements and steering.0
"""

from carla import VehicleControl

try:
    from pygame.locals import K_DOWN
    from pygame.locals import K_LEFT
    from pygame.locals import K_RIGHT
    from pygame.locals import K_SPACE
    from pygame.locals import K_UP
    from pygame.locals import K_a
    from pygame.locals import K_d
    from pygame.locals import K_p
    from pygame.locals import K_q
    from pygame.locals import K_r
    from pygame.locals import K_s
    from pygame.locals import K_w
except ImportError:
    raise RuntimeError(
        'cannot import pygame, make sure pygame package is installed')

# Copyright (c) 2017 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import datetime
import sys

from contextlib import contextmanager


@contextmanager
def make_connection(client_type, *args, **kwargs):
    """Context manager to create and connect a networking client object."""
    client = None
    try:
        client = client_type(*args, **kwargs)
        client.connect()
        yield client
    finally:
        if client is not None:
            client.disconnect()


class StopWatch(object):
    def __init__(self):
        self.start = datetime.datetime.now()
        self.end = None

    def restart(self):
        self.start = datetime.datetime.now()
        self.end = None

    def stop(self):
        self.end = datetime.datetime.now()

    def seconds(self):
        return (self.end - self.start).total_seconds()

    def milliseconds(self):
        return 1000.0 * self.seconds()


def to_hex_str(header):
    return ':'.join('{:02x}'.format(ord(c)) for c in header)


if sys.version_info >= (3, 3):

    import shutil

    def print_over_same_line(text):
        terminal_width = shutil.get_terminal_size((80, 20)).columns
        empty_space = max(0, terminal_width - len(text))
        sys.stdout.write('\r' + text + empty_space * ' ')
        sys.stdout.flush()

else:

    # Workaround for older Python versions.
    def print_over_same_line(text):
        line_length = max(print_over_same_line.last_line_length, len(text))
        empty_space = max(0, line_length - len(text))
        sys.stdout.write('\r' + text + empty_space * ' ')
        sys.stdout.flush()
        print_over_same_line.last_line_length = line_length
    print_over_same_line.last_line_length = 0
    

    
class KeyboardHelper:

    def get_keyboard_control(keys, is_on_reverse, enable_autopilot):
        if keys[K_r]:
            return None
        control = VehicleControl()
        if keys[K_LEFT] or keys[K_a]:
            control.steer = -1.0
        if keys[K_RIGHT] or keys[K_d]:
            control.steer = 1.0
        if keys[K_UP] or keys[K_w]:
            control.throttle = 1.0
        if keys[K_DOWN] or keys[K_s]:
            control.brake = 1.0
        if keys[K_SPACE]:
            control.hand_brake = True
        if keys[K_q]:
            is_on_reverse = not is_on_reverse
        if keys[K_p]:
            enable_autopilot = not enable_autopilot
        control.reverse = is_on_reverse
        return control, is_on_reverse, enable_autopilot


class MeasurementsDisplayHelper:
    def print_player_measurements_map(player_measurements, map_position, lane_orientation, timer):
        message = 'Step {step} ({fps:.1f} FPS): '
        message += 'Map Position ({map_x:.1f},{map_y:.1f}) '
        message += 'Lane Orientation ({ori_x:.1f},{ori_y:.1f}) '
        message += '{speed:.2f} km/h, '
        message += '{other_lane:.0f}% other lane, {offroad:.0f}% off-road'
        message = message.format(
            map_x=map_position[0],
            map_y=map_position[1],
            ori_x=lane_orientation[0],
            ori_y=lane_orientation[1],
            step=timer.step,
            fps=timer.ticks_per_second(),
            speed=player_measurements.forward_speed * 3.6,
            other_lane=100 * player_measurements.intersection_otherlane,
            offroad=100 * player_measurements.intersection_offroad)
        print_over_same_line(message)

    def print_player_measurements(player_measurements, timer):
        message = 'Step {step} ({fps:.1f} FPS): '
        message += '{speed:.2f} km/h, '
        message += '{other_lane:.0f}% other lane, {offroad:.0f}% off-road'
        message = message.format(
            step=timer.step,
            fps=timer.ticks_per_second(),
            speed=player_measurements.forward_speed * 3.6,
            other_lane=100 * player_measurements.intersection_otherlane,
            offroad=100 * player_measurements.intersection_offroad)
        print_over_same_line(message)
