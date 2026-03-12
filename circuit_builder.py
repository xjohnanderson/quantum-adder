from qiskit.circuit import QuantumCircuit, QuantumRegister

def create_rfa_gate():
    """Defines the Reversible Full Adder gate."""
    qa = QuantumRegister(1, 'A')
    qb = QuantumRegister(1, 'B')
    qcin = QuantumRegister(1, 'Cin')
    qs = QuantumRegister(1, 'S')
    qcout = QuantumRegister(1, 'Cout')
    
    rfa_circuit = QuantumCircuit(qa, qb, qcin, qs, qcout, name='RFA')
    rfa_circuit.cx(qa[0], qs[0])
    rfa_circuit.cx(qb[0], qs[0])
    rfa_circuit.ccx(qa[0], qb[0], qcout[0])
    rfa_circuit.ccx(qcin[0], qs[0], qcout[0])
    rfa_circuit.cx(qcin[0], qs[0])
    
    return rfa_circuit.to_gate(label='RFA')

RFA_GATE = create_rfa_gate()

def n_bit_adder(n_bits):
    qa = QuantumRegister(n_bits, 'A')
    qb = QuantumRegister(n_bits, 'B')
    qcin_qcout = QuantumRegister(n_bits + 1, 'C_IO')
    qsum = QuantumRegister(n_bits, 'S')
    q_ancilla = QuantumRegister(1, 'Ancilla')

    adder_circuit = QuantumCircuit(qa, qb, qcin_qcout, qsum, q_ancilla, name=f'{n_bits}-bit_Adder')

    # Forward computation
    for i in range(n_bits):
        adder_circuit.append(RFA_GATE, [qa[i], qb[i], qcin_qcout[i], qsum[i], qcin_qcout[i+1]])

    adder_circuit.barrier(label='Uncomputation_Start')

    # Reverse computation
    for i in range(n_bits - 2, -1, -1):
        adder_circuit.cx(qsum[i], q_ancilla[0])
        adder_circuit.cx(qcin_qcout[i], q_ancilla[0])
        adder_circuit.ccx(qcin_qcout[i], q_ancilla[0], qcin_qcout[i+1])
        adder_circuit.ccx(qa[i], qb[i], qcin_qcout[i+1])
        adder_circuit.cx(qcin_qcout[i], q_ancilla[0])
        adder_circuit.cx(qsum[i], q_ancilla[0])

    adder_circuit.barrier(label='Uncomputation_End')
    return adder_circuit