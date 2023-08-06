# Copyright 2021 qclib project.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
These classes are adaptations of Qiskit's RawFeatureVector and RawParameterizedInitialize
classes.
https://github.com/Qiskit/qiskit-machine-learning/blob/main/qiskit_machine_learning/circuit/library/raw_feature_vector.py

The correct approach is to create a RawFeatureVector base class that implements
only the common routines. Other classes, such as BaaFeatureVector, would
inherit from this new class implementing at least the __init__ and _build
functions. The current RawFeatureVector class would have to be renamed.
"""

from typing import Optional, List
import numpy as np
from qiskit.exceptions import QiskitError
from qiskit.circuit import QuantumRegister, ParameterVector, Instruction
from qiskit.circuit.library import BlueprintCircuit
from ..state_preparation.bdsp import initialize as bdsp # pylint: disable=relative-beyond-top-level

class BdspFeatureVector(BlueprintCircuit):
    """The BDSP schmidt feature vector circuit.

    This circuit acts as parameterized initialization for statevectors with ``feature_dimension``
    dimensions, thus with ``(split+1)*(feature_dimension/2**split)-1`` qubits. The circuit
    contains a placeholder instruction that can only be synthesized/defined when all parameters
    are bound.

    In ML, this circuit can be used to load the training data into qubit amplitudes. It does not
    apply an kernel transformation (therefore, it is a "raw" feature vector).

    This circuit can't be used with gradient based optimizers.

    Examples:

    .. code-block::

        from qclib.machine_learning.bdsp_feature_vector import BdspFeatureVector
        circuit = BdspFeatureVector(4)
        print(circuit.num_qubits)
        # prints: 2

        print(circuit.draw(output='text'))
        # prints:
        #      ┌────────────────────────────────────────┐
        # q_0: ┤0                                              ├
        #      │  PARAMETERIZEDINITIALIZE(x[0],x[1],x[2],x[3]) │
        # q_1: ┤1                                              ├
        #      └────────────────────────────────────────┘

        print(circuit.ordered_parameters)
        # prints: [Parameter(p[0]), Parameter(p[1]), Parameter(p[2]), Parameter(p[3])]

        import numpy as np
        state = np.array([1, 0, 0, 1]) / np.sqrt(2)
        bound = circuit.assign_parameters(state)
        print(bound.draw())
        # prints:
        #      ┌────────────────────────────────────────┐
        # q_0: ┤0                                              ├
        #      │  PARAMETERIZEDINITIALIZE(0.70711,0,0,0.70711) │
        # q_1: ┤1                                              ├
        #      └────────────────────────────────────────┘

    """

    def __init__(self, feature_dimension: Optional[int], split: int = 1) -> None:
        """
        Args:
            feature_dimension: The feature dimension from which the number of
                    qubits is inferred as ``n_qubits = (split+1)*(feature_dim/2**split)-1``

        """
        super().__init__()

        self._ordered_parameters = ParameterVector("x")
        self._split = split
        if feature_dimension is not None:
            self.feature_dimension = feature_dimension

    def _build(self):
        super()._build()

        placeholder = BdspParameterizedInitialize(self._ordered_parameters[:],
                                                  self._split)
        self.append(placeholder, self.qubits)
        
    def _unsorted_parameters(self):
        if self.data is None:
            self._build()
        return super()._unsorted_parameters()

    def _check_configuration(self, raise_on_failure=True):
        if isinstance(self._ordered_parameters, ParameterVector):
            self._ordered_parameters.resize(self.feature_dimension)
        elif len(self._ordered_parameters) != self.feature_dimension:
            if raise_on_failure:
                raise ValueError("Mismatching number of parameters and feature dimension.")
            return False
        return True

    @property
    def num_qubits(self) -> int:
        """Returns the number of qubits in this circuit.

        Returns:
            The number of qubits.
        """
        return super().num_qubits

    @num_qubits.setter
    def num_qubits(self, num_qubits: int) -> None:
        """Set the number of qubits for the n-local circuit.

        Args:
            The new number of qubits.
        """
        if self.num_qubits != num_qubits:
            # invalidate the circuit
            self._invalidate()
            self.qregs: List[QuantumRegister] = []
            if num_qubits is not None and num_qubits > 0:
                self.qregs = [QuantumRegister(num_qubits, name="q")]

    @property
    def feature_dimension(self) -> int:
        """Return the feature dimension.

        Returns:
            The feature dimension.
        """
        return int(((self.num_qubits+1)/(self._split+1))*(2**self._split))

    @feature_dimension.setter
    def feature_dimension(self, feature_dimension: int) -> None:
        """Set the feature dimension.

        Args:
            feature_dimension: The new feature dimension. Must be a power of 2.

        Raises:
            ValueError: If ``feature_dimension`` is not a power of 2.
        """
        num_qubits = int((self._split+1)*(feature_dimension/(2**self._split))-1)
        if int(num_qubits) != num_qubits:
            raise ValueError("feature_dimension must be a power of 2!")

        if num_qubits != self.num_qubits:
            self._invalidate()
            self.num_qubits = int(num_qubits)

class BdspParameterizedInitialize(Instruction):
    """A normalized parameterized initialize instruction."""

    def __init__(self, amplitudes, split):
        num_qubits = (split+1)*(len(amplitudes)/(2**split))-1
        if int(num_qubits) != num_qubits:
            raise ValueError("feature_dimension must be a power of 2!")

        super().__init__("BdspParameterizedInitialize", int(num_qubits), 0, amplitudes)

        self._split = split

    def _define(self):
        # cast ParameterExpressions that are fully bound to numbers
        cleaned_params = []
        for param in self.params:
            if len(param.parameters) == 0:
                cleaned_params.append(complex(param))
            else:
                print('param', param)
                raise QiskitError(
                    "Cannot define a BdspParameterizedInitialize with unbound parameters"
                )

        # normalize
        normalized = np.array(cleaned_params) / np.linalg.norm(cleaned_params)

        circuit = bdsp(normalized, split=self._split)

        self.definition = circuit
