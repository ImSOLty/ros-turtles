#!/usr/bin/python3

import numpy as np
from dataclasses import dataclass, astuple


@dataclass
class TurtlePosition:
    x_position: float = None
    y_position: float = None
    z_rotation: float = None


@dataclass
class TurtleMovement:
    x_linear_velocity: float = None
    y_linear_velocity: float = None
    z_angular_velocity: float = None


class TurtleCommander:
    def __init__(self, speed: float):
        self._speed = speed
        self._position = TurtlePosition()
        self._target_position = TurtlePosition()
        self._rotation_speed = 4.0
        self._stop_distance = 0.25

    def update_position(self, position: TurtlePosition) -> None:
        self._position = position

    def update_target_position(self, position: TurtlePosition) -> None:
        self._target_position = position

    def calculate_movement(self) -> TurtleMovement:
        if not self._can_calculate_movement():
            return TurtleMovement(0.0, 0.0, 0.0)

        angular_velocity = self._calculate_angular_velocity()
        return TurtleMovement(0.0 if self._close_enough() else self._speed, 0.0,
                              self._rotation_speed * angular_velocity)

    def _can_calculate_movement(self) -> bool:
        return (astuple(self._position) + astuple(self._target_position)).count(None) == 0

    def _close_enough(self):
        d = np.array([self._target_position.x_position - self._position.x_position,
                      self._target_position.y_position - self._position.y_position])
        return np.linalg.norm(d) < self._stop_distance

    def _calculate_target_direction(self) -> np.array:
        v = np.array([self._target_position.x_position - self._position.x_position,
                      self._target_position.y_position - self._position.y_position])
        v = v / np.linalg.norm(v)
        return v

    def _calculate_self_direction(self) -> np.array:
        v = np.array([-1.0, 0.0])
        rotation_matrix = np.array([[np.cos(self._position.z_rotation), -np.sin(self._position.z_rotation)],
                                    [np.sin(self._position.z_rotation), np.cos(self._position.z_rotation)]])
        v = np.dot(rotation_matrix, v)
        v = v / np.linalg.norm(v)
        return v

    def _calculate_angular_velocity(self) -> float:
        x = self._calculate_self_direction()
        v = self._calculate_target_direction()
        return ((np.arctan2(x[0] * v[1] - v[0] * x[1], x[0] * v[0] + x[1] * v[1])) % (2 * np.pi)) - np.pi