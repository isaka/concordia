# Copyright 2023 DeepMind Technologies Limited.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A component that ignores the action spec in the `pre_act` method."""

import abc

from concordia.typing import component_v2
from concordia.typing import entity as entity_lib


class ActionSpecIgnored(component_v2.EntityComponent, metaclass=abc.ABCMeta):
  """A component that ignores the action spec in the `pre_act` method.
  
  As a consequence, its `pre_act` state can be accessed safely by other
  components. This is useful for components that need to condition their
  `pre_act` state on the state of other components. Derived classes should
  implement `make_pre_act_context` instead of `pre_act`. The pre_act context
  will be cached and returned by `get_pre_act_context` and `pre_act`, and
  cleaned up by `update`.
  """

  def __init__(self):
    """Initializes the component."""
    self._pre_act_context: str | None = None

  @abc.abstractmethod
  def make_pre_act_context(self) -> str:
    """Creates the pre-act context."""
    raise NotImplementedError()

  def set_pre_act_context(self, pre_act_context: str) -> None:
    """Creates the pre-act context."""
    if self._pre_act_context is not None:
      raise ValueError('pre_act_context is already set.')
    self._pre_act_context = pre_act_context

  def get_pre_act_context(self) -> str:
    """Creates the pre-act context."""
    if self._pre_act_context is None:
      self._pre_act_context = self.make_pre_act_context()
    return self._pre_act_context

  def pre_act(
      self,
      action_spec: entity_lib.ActionSpec,
  ) -> str:
    del action_spec
    return self.get_pre_act_context()

  def update(self) -> None:
    self._pre_act_context = None