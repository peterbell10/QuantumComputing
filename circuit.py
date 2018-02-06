
class basis_gates:
    had = 0  # Hadamard
    c_V = 1  # Controlled-V

    @staticmethod
    def to_string(gate):
        return {
            basis_gates.had:"Hadamard",
            basis_gates.c_V:"Controlled-V"
        }[gate]

class gate:
    def __init__(self, gate_type, operand_qbits):
        self.gate_type = int(gate_type)
        self.qbits = list(operand_qbits)

    def __str__(self):
        string = basis_gates.to_string(self.gate_type)
        string += '('
        string += ', '.join(str(q) for q in self.qbits)
        string += ')'
        return string

class circuit:
    
    def __init__(self):
        self.gates = []

    def __or__(self, other):
        """Concatenate another circuit onto this"""
        self.gates = self.gates + other.gates
        return self

    def __mul__(self, repeat_times):
        """Repeat this circuit multiple times"""
        self.gates = self.gates * repeat_times
        return self

    def __str__(self):
        return ' |\n'.join(str(g) for g in self.gates)
    
    
    def add_gate(self, gate_type, operand_qbits):
        """Add a single gate to the end of the circuit"""
        self.gates.append(gate(gate_type, operand_qbits))
        return self

def hadamard(qbit):
    return circuit().add_gate(basis_gates.had, [qbit])
        
def c_V(control_qbit, V_qbit):
    return circuit().add_gate(basis_gates.c_V, [control_qbit, V_qbit])

def c_not(control_qbit, not_qbit):
    return (
        hadamard(not_qbit) |
        c_V(control_qbit, not_qbit) |
        c_V(control_qbit, not_qbit) |
        hadamard(not_qbit))

def toffoli(control_1_qbit, control_2_qbit, not_qbit):
    return (
        hadamard(not_qbit) |
        c_V(control_2_qbit, not_qbit) |
        c_not(control_1_qbit, control_2_qbit) |
        c_V(control_2_qbit, not_qbit) * 3 |
        c_not(control_1_qbit, control_2_qbit) |
        c_V(control_1_qbit, not_qbit) |
        hadamard(not_qbit))

def adder(x_qbit, y_qbit, carry_qbit):
    return (
        toffoli(x_qbit, y_qbit, carry_qbit) |
        c_not(x_qbit, y_qbit))

if __name__ == '__main__':
    print(str(adder(1, 2, 3)))
