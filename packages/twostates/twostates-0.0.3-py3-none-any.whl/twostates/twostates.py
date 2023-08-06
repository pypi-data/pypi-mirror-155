import numpy as np
import scipy.linalg as lina
import scipy.constants as sc
import log







def detectState(input):
    if isinstance(input, TwoState):
        vec = input.get2dVector()
    elif isinstance(input, MultiState):
        vec = input.getVector()
    elif isinstance(input, np.ndarray):
        vec = input
    else:
        log.fail("Could not detect input data type for detectState()")
        return ""

    if len(vec) == 2:
        known = np.array([1, 0])
        state = "|0>"
        if not check(vec, known, state) == "":
            return check(vec, known, state)

        known = np.array([0, 1])
        state = "|1>"
        if not check(vec, known, state) == "":
            return check(vec, known, state)


        known = np.array([1/np.sqrt(2), 1/np.sqrt(2)])
        state = "|+>"
        if not check(vec, known, state) == "":
            return check(vec, known, state)

        known = np.array([1/np.sqrt(2), -1/np.sqrt(2)])
        state = "|->"
        if not check(vec, known, state) == "":
            return check(vec, known, state)

        known = np.array([1/np.sqrt(2), 1j/np.sqrt(2)])
        state = "|+_y>"
        if not check(vec, known, state) == "":
            return check(vec, known, state)

        known = np.array([1/np.sqrt(2), -1j/np.sqrt(2)])
        state = "|-_y>"
        if not check(vec, known, state) == "":
            return check(vec, known, state)



    if len(vec) == 4:
        known = np.array([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)])
        state = "|Phi^+>"
        if not check(vec, known, state) == "":
            return check(vec, known, state)

        known = np.array([1/np.sqrt(2), 0, 0, -1/np.sqrt(2)])
        state = "|Phi^->"
        if not check(vec, known, state) == "":
            return check(vec, known, state)
        
        known = np.array([0, 1/np.sqrt(2), 1/np.sqrt(2), 0])
        state = "|Psi^+>"
        if not check(vec, known, state) == "":
            return check(vec, known, state)

        known = np.array([0, 1/np.sqrt(2), -1/np.sqrt(2), 0])
        state = "|Psi^->"
        if not check(vec, known, state) == "":
            return check(vec, known, state)
    


    if len(vec) == 8:
        known = 1/np.sqrt(2)*np.array([1, 0, 0, 0, 0, 0, 0, 1])
        state = "|GHZ>"
        if not check(vec, known, state) == "":
            return check(vec, known, state)

        known = 1/np.sqrt(3) * np.array([0, 1, 1, 0, 1, 0, 0, 0])
        state = "|W>"
        if not check(vec, known, state) == "":
            return check(vec, known, state)
        
    # for larger check whether it contains one 1
    if 1 in abs(vec):
        known = np.zeros_like(vec)
        known[np.argmax(vec)] = 1
        phase = getPhase(known, input)
        value = np.exp(1j*getPhase(known, input))
        phaseText = "(%.4f%.4fj)"%(value.real, value.imag) if value.imag<0 else "(%.4f+%.4fj)"%(value.real, value.imag)
        phaseText = "exp(%fj)" % phase

        state = bin(np.argmax(vec))[2:]
        while len(state) < np.log2(len(vec)):
            state = "0"+state
        return phaseText + "|%s>" % state

    return ""

def check(input, known, state:str):
    if abs(getDistance(input, known) - 1) < 1e-9:
        if areEqual(input, known):
            return state
        else:
            phase = np.exp(1j*getPhase(known, input))
            phaseText = "(%.4f%.4fj)"%(phase.real, phase.imag) if phase.imag<0 else "(%.4f+%.4fj)"%(phase.real, phase.imag)
            return phaseText + state 
    return ""


def areEqual(in1, in2):
    if not isinstance(in1, np.ndarray):
        in1 = in1.getMatrix()
    if not isinstance(in2, np.ndarray):
        in2 = in2.getMatrix()
    return np.all(abs(in1.real-in2.real) < 1e-10) and np.all(abs(in1.imag-in2.imag) < 1e-10)

def getDistance(in1, in2):
    if not isinstance(in1, np.ndarray):
        in1 = in1.getMatrix()
    if not isinstance(in2, np.ndarray):
        in2 = in2.getMatrix()
    return np.abs(np.dot(np.transpose(in1.conjugate()), in2))

def getPhase(in1, in2):
    if not isinstance(in1, np.ndarray):
        in1 = in1.getMatrix()
    if not isinstance(in2, np.ndarray):
        in2 = in2.getMatrix()

    scalar = np.dot(np.transpose(in1.conjugate()), in2)
    if abs(scalar.real) < 1e-15:
        phi1 = np.pi/2 if scalar.imag>1e-10 else -np.pi/2
    else:
        phi = np.angle(scalar)
    return phi







class Operator:

    def __init__(self, matrix:np.ndarray):
        self.matrix = matrix
        if not isinstance(matrix, np.ndarray):
            log.fail("You need to pass a matrix to create an operator.")
            self.matrix = np.eye(2)

    def getMatrix(self):
        return self.matrix

    def isUnitary(self):
        return np.all(abs(np.eye(len(self.matrix)) - np.dot(self.matrix, np.conjugate(self.matrix.transpose()))) < 1e-10)

    def isHermitian(self):
        return np.all(abs(self.matrix - np.conjugate(self.matrix.transpose())) < 1e-10)

    def isProjector(self):
        return np.all(self.matrix@self.matrix - self.matrix < 1e-10)

    def dagger(self):
        self.matrix = np.transpose(self.getMatrix().conjugate())
        return self

    def copy(self):
        return Operator(self.matrix.copy())

    def printbraket(self):
        output = "O = "
        first = 2
        for i in range(0, len(self.matrix)):
            for j in range(0, len(self.matrix[0])):
                elem = self.matrix[i, j]
                if abs(elem) > 1e-10:
                    first -= 1
                    if abs(elem.real) > 1e-10:
                        if abs(elem.real - 1) < 1e-10:
                            if first <= 0:
                                output += " +"
                            pass
                        elif abs(elem.real + 1) < 1e-10:
                            output += " -"
                        else:
                            if elem.real > 0:
                                if first > 0:
                                    output += str(elem.real)
                                else:
                                    output += " +" + str(elem.real)
                            else:
                                output += " -" + str(-elem.real)
                    if abs(elem.imag) > 1e-10:
                        if elem.imag > 0:
                            if first > 0:
                                output += str(elem.imag)+"j"
                            else:
                                output += " +" + str(elem.imag)+"j"
                        else:
                            output += " - " + str(-elem.imag)+"j"
                    output += "|%d><%d|" % (i,j)
        return output

    def __mul__(self, o):
        if isinstance(o, Operator):
            if len(o.getMatrix()) == len(self.getMatrix()):
                return Operator(np.dot(self.getMatrix(), o.getMatrix()))
            else:
                log.error("Operators have different dimension!")
                return self

        if isinstance(o, float):
            if o == 0:
                return 0
            return Operator(o*self.getMatrix())

    def __rmul__(self, o):
        if isinstance(o, Operator):
            if len(o.getMatrix()) == len(self.getMatrix()):
                return Operator(np.dot(o.getMatrix(), self.getMatrix()))
            else:
                log.error("Operators have different dimension!")
                return self

        if isinstance(o, float):
            if o == 0:
                return 0
            return Operator(o*self.getMatrix())

    def __add__(self, o):
        if not isinstance(o, Operator):
            log.error("An Operator can only be added with another Operator!")
            return self
        if len(o.getMatrix()) != len(self.getMatrix()):
            log.error("Hamiltonians have different dimension!")
            return self
        return Operator(self.getMatrix() + o.getMatrix())

    def __str__(self):
        string = "This is a Operator with matrix representation\n" + str(self.matrix)
        return string



class Hamiltonian(Operator):

    def __init__(self, matrix:np.ndarray):
        if not np.all(matrix - np.conjugate(matrix) < 1e-9):
            log.fail("This Hamiltonian is not hermitian!!!")
            log.fail("given:")
            log.fail(matrix)
            log.fail("conjugate:")
            log.fail(np.conjugate(matrix))
        self.matrix = matrix

    def getax(self):
        return np.trace(np.dot(Pauli.x(), self.matrix))
    def getay(self):
        return np.trace(np.dot(Pauli.y(), self.matrix))
    def getaz(self):
        return np.trace(np.dot(Pauli.z(), self.matrix))


    def geth0(self):
        return 0.5*np.trace(self.matrix).real


    def getBlochVector(self):
        return 0.5*np.array([self.getax(), self.getay(), self.getaz()]).real

    def getMatrix(self):
        return self.matrix


    def __mul__(self, o):
        if isinstance(o, Hamiltonian):
            if len(o.getMatrix()) == len(self.getMatrix()):
                return Hamiltonian(np.dot(self.getMatrix(), o.getMatrix()))
            else:
                log.error("Hamiltonians have different dimension!")
                return self

        if isinstance(o, float):
            if o == 0:
                return 0
            return Hamiltonian(o*self.getMatrix())

    def __rmul__(self, o):
        if isinstance(o, Hamiltonian):
            if len(o.getMatrix()) == len(self.getMatrix()):
                return Hamiltonian(np.dot(o.getMatrix(), self.getMatrix()))
            else:
                log.error("Hamiltonians have different dimension!")
                return self

        if isinstance(o, float):
            if o == 0:
                return 0
            return Hamiltonian(o*self.getMatrix())

    def __add__(self, h):
        if not isinstance(h, Hamiltonian):
            log.error("A Hamiltonian can only be added with another Hamiltonian!")
            return self
        if len(h.getMatrix()) != len(self.getMatrix()):
            log.error("Hamiltonians have different dimension!")
            return self
        return Hamiltonian(self.getMatrix() + h.getMatrix())

    def __str__(self):
        string = "This is a Hamilton-Operator with matrix representation\n" + str(self.matrix)
        return string




class Unitary(Operator):

    def __init__(self, matrix:np.ndarray):
        super().__init__(matrix)
        if not self.isUnitary():
            log.fail("The given matrix for the operator is not unitary!")


class Projector(Operator):

    def __init__(self, matrix:np.ndarray):
        super().__init__(matrix)
        if not self.isProjector():
            log.fail("The given matrix for the operator is not a projector!!")



class RotationOperator(Unitary):
    def __init__(self, vector: np.array, angle):
        if not len(vector) == 3:
            log.fail("Vector to rotation Operator has to have 3 entries!")
        matrix = np.cos(angle/2) * np.array([[1,0],[0,1]]) - 1j* np.sin(angle/2) * (vector[0] * Pauli.x() + vector[1] * Pauli.y() + vector[2] * Pauli.z())
        super().__init__(matrix)



class Rx(RotationOperator):
    def __init__(self, angle):
        super().__init__(np.array([1,0,0]), angle)

class Ry(RotationOperator):
    def __init__(self, angle):
        super().__init__(np.array([0,1,0]), angle)

class Rz(RotationOperator):
    def __init__(self, angle):
        self.matrix = RotationOperator(np.array([0,0,1]), angle).getMatrix()



class TwoState:

    def __init__(self, koeff1, koeff2):
        self.k1 = koeff1
        self.k2 = koeff2
        if not (koeff1*np.conjugate(koeff1) + koeff2*np.conjugate(koeff2) - 1) < 1e-9:
            log.warn("This state is not normalized!!!")
            log.warn("koeff1^2 + koeff2^2 = " + str(koeff1*np.conjugate(koeff1) + koeff2*np.conjugate(koeff2)))
            self.k2 = np.sqrt(1-koeff1**2)


    def get2dVector(self):
        return np.array([self.k1, self.k2])

    def getVector(self):
        return np.array([self.k1, self.k2])


    def printVector(self):
        self.print2dVector()
    def print2dVector(self):
        log.green("My state vector is: %s" % (self.get2dVector()))

    def getDensityMatrix(self):
        return DensityMatrix(np.outer(self.get2dVector(), np.conjugate(self.get2dVector())))

    def getax(self):
        return np.dot(np.transpose(np.conjugate(self.get2dVector())), np.dot(Pauli.x(), self.get2dVector()))
    def getay(self):
        return np.dot(np.transpose(np.conjugate(self.get2dVector())), np.dot(Pauli.y(), self.get2dVector()))
    def getaz(self):
        return np.dot(np.transpose(np.conjugate(self.get2dVector())), np.dot(Pauli.z(), self.get2dVector()))

    def getBlochVector(self):
        res = np.array([self.getax(), self.getay(), self.getaz()])
        if np.any(abs(res.imag) > 1e-9):
            log.warn("Bloch vector did contain imaginary components!")
        if not abs(np.dot(np.transpose(res), res) - 1) < 1e-10:
            log.fail("Absolute of bloch vector is unequal to 1!!")
        return res.real

    
    def applyOperator(self, op:Operator):
        res = np.dot(op.getMatrix(), self.get2dVector())
        self.k1, self.k2 = res
        return self

    def getTimeEvolution(self, hamiltonian:Hamiltonian, t, hbar=sc.hbar):
        hvec = hamiltonian.getBlochVector()
        habs = np.sqrt(np.dot(hvec, np.conjugate(hvec)))


        currstate = self.get2dVector()

        one = np.cos(habs*t/hbar)*currstate
        two = -1j/habs * np.sin(habs*t/hbar) * (hvec[0] * np.dot(Pauli.x(), currstate) + hvec[1] * np.dot(Pauli.y(), currstate) + hvec[2] * np.dot(Pauli.z(), currstate))
        
        res = np.exp(-1j*hamiltonian.geth0()*t/hbar) * (one + two)
        return TwoState(res[0], res[1])

    def project(self, ts):
        k1, k2 = ts.get2dVector()
        return self.k1*np.conjugate(k1) + self.k2*np.conjugate(k2)

    def expectationValue(self, op:Operator):
        res = np.dot(np.transpose(self.get2dVector().conjugate()), np.dot(op.getMatrix(), self.get2dVector()))
        if abs(res.imag) > 1e-10:
            log.fail("Expectation value has imaginary part!!!\nInternal error!")
        return res.real

    def __str__(self):
        name = detectState(self.get2dVector())
        if name == "":
            name = "%.6f+%.6fj |0> + %.6f+%.6fj |1>" % (self.k1.real, self.k1.imag, self.k2.real, self.k2.imag)
        string = "This is a Two-State described by |Psi> = %s" % name
        return string



class MultiState:

    def __init__(self, vec:np.ndarray):
        if not (np.transpose(vec.conjugate()) @ vec - 1) < 1e-9:
            log.warn("This state is not normalized!!!")
        self.vec = vec


    def copy(self):
        return MultiState(self.vec)

    def getVector(self):
        return self.vec


    def printVector(self):
        log.green("My state vector is: %s" % (self.get2dVector()))

    def getDensityMatrix(self):
        return DensityMatrix(np.outer(self.getVector(), np.conjugate(self.getVector())))

    def getax(self):
        return np.dot(np.transpose(np.conjugate(self.getVector())), np.dot(Pauli.x(), self.getVector()))
    def getay(self):
        return np.dot(np.transpose(np.conjugate(self.getVector())), np.dot(Pauli.y(), self.getVector()))
    def getaz(self):
        return np.dot(np.transpose(np.conjugate(self.getVector())), np.dot(Pauli.z(), self.getVector()))

    def getBlochVector(self):
        res = np.array([self.getax(), self.getay(), self.getaz()])
        if np.any(abs(res.imag) > 1e-9):
            log.warn("Bloch vector did contain imaginary components!")
        if not abs(np.dot(np.transpose(res), res) - 1) < 1e-10:
            log.fail("Absolute of bloch vector is unequal to 1!!")
        return res.real

    
    def applyOperator(self, op:Operator):
        if len(self.getVector()) != len(op.getMatrix()[0]):
            log.fail("Operator does not match qubit state dimension!")
        res = np.dot(op.getMatrix(), self.getVector())
        self.vec = res
        return self

    def getTimeEvolution(self, hamiltonian:Hamiltonian, t, hbar=sc.hbar):
        hvec = hamiltonian.getBlochVector()
        habs = np.sqrt(np.dot(hvec, np.conjugate(hvec)))


        currstate = self.getVector()

        one = np.cos(habs*t/hbar)*currstate
        two = -1j/habs * np.sin(habs*t/hbar) * (hvec[0] * np.dot(Pauli.x(), currstate) + hvec[1] * np.dot(Pauli.y(), currstate) + hvec[2] * np.dot(Pauli.z(), currstate))
        
        res = np.exp(-1j*hamiltonian.geth0()*t/hbar) * (one + two)
        return TwoState(res[0], res[1])

    def project(self, ms):
        return np.dot(np.conjugate(self.getVector()).T, ms.getVector())

    def expectationValue(self, op):
        res = np.dot(np.transpose(self.getVector().conjugate()), np.dot(op, self.getVector()))
        if abs(res.imag) > 1e-10:
            log.fail("Expectation value has imaginary part!!!\nInternal error!")
        return res.real
  
    def __str__(self):
        name = detectState(self.getVector())
        if detectState(self.getVector()) == "":
            name = str(self.vec)
        string = "This is a %d-Qubit-state described by\n\t|Psi> = %s" % (np.log2(len(self.vec)), name)
        return string

if __name__ == "__main__":
    ghz = MultiState(1j/np.sqrt(2)*np.array([1,0,0,0,0,0,0,1]))
    log.green(ghz)


class DensityMatrix:

    def __init__(self, matrix:np.array):
        self.matrix = matrix
        if not np.trace(matrix) - 1 < 1e-10:
            log.warn("This matrix does not have unit trace!!!")
            self.matrix = matrix/np.trace(matrix)
        if not self.isHermitian():
            log.warn("This matrix is not hermitian!!!")
        if not matrix.shape[0] == matrix.shape[1]:
            log.fail("rho is not square!")



    def getax(self):
        return np.trace(np.dot(Pauli.x(), self.matrix)).real
    def getay(self):
        return np.trace(np.dot(Pauli.y(), self.matrix)).real
    def getaz(self):
        return np.trace(np.dot(Pauli.z(), self.matrix)).real


    def getBlochVector(self):
        return np.array([self.getax(), self.getay(), self.getaz()])


    def isPure(self):
        return np.all(np.dot(self.matrix, self.matrix) - self.matrix < 1e-15)

    def printIsPure(self):
        if self.isPure():
            log.green("This is a pure state!")
        else:
            log.warn("This is a mixed state")

    def isHermitian(self):
        return np.all(self.matrix == np.transpose(np.conjugate(self.matrix)))

    def getMatrix(self):
        return self.matrix

    def applyOperator(self, op:Operator):
        if not len(op.getMatrix()) == len(self.matrix):
            log.warn("Operator has different dimension than density matrix! (length op: %d, matrix: %d)" % (len(op.getMatrix()), len(self.matrix)))
            return self
        matrix = np.dot(op.getMatrix(), np.dot(self.matrix, np.transpose(np.conjugate(op.getMatrix()))))
        return DensityMatrix(matrix)
        #self.matrix = matrix
        #return self


    def copy(self):
        return DensityMatrix(self.matrix.copy())


    def getTimeEvolution(self, hamiltonian:Hamiltonian, t, hbar=sc.hbar):
        U = Operator(lina.expm(-1j*hamiltonian.getMatrix()*t/hbar))
        return self.applyOperator(U)


    
    def expectationValue(self, op:Operator):
        return np.trace(np.dot(self.matrix, op.getMatrix()))
                
    def project(self, proj:Projector):
        return self.probability(proj)

    def probability(self, proj:Projector):
        return np.trace(np.dot(np.dot(proj.getMatrix(), self.matrix), proj.getMatrix()))

    def partialTrace(self, dimA:int, dimB:int, debug=False):
        if not self.matrix.shape[0] == dimA*dimB:
            log.fail("Dimension of density matrix did not match A and B")
            log.fail("dim(rho) = %d, dimA=%d, dimB=%d" % (self.matrix.shape[0], dimA, dimB))
            return (np.eye(dimA), np.eye(dimB))

        # reshape
        temp = np.reshape(self.matrix, (dimA, dimB, dimA, dimB))
        if debug:
            log.debug(temp)

        # trace
        rhoA = np.trace(temp, axis1=1, axis2=3)
        rhoB = np.trace(temp, axis1=0, axis2=2)
        if debug:
            log.debug(rhoA)

        return (rhoA, rhoB)
        

    def __mul__(self, o):
        if isinstance(o, DensityMatrix):
            if len(o.getMatrix()) == len(self.getMatrix()):
                return DensityMatrix(np.dot(self.getMatrix(), o.getMatrix()))
            else:
                log.error("DensityMatrices have different dimension!")
                return self

        if isinstance(o, float):
            if o == 0:
                return 0
            return DensityMatrix(o*self.getMatrix())

    def __rmul__(self, o):
        if isinstance(o, DensityMatrix):
            if len(o.getMatrix()) == len(self.getMatrix()):
                return DensityMatrix(np.dot(o.getMatrix(), self.getMatrix()))
            else:
                log.error("DensityMatricies have different dimension!")
                return self

        if isinstance(o, float):
            if o == 0:
                return 0
            return Operator(o*self.getMatrix())

    def __add__(self, o):
        if not isinstance(o, DensityMatrix):
            log.error("A DensityMatrix can only be added with another DensityMatrix!")
            return self
        if len(o.getMatrix()) != len(self.getMatrix()):
            log.error("DensityMatrices have different dimension!")
            return self
        return DensityMatrix(self.getMatrix() + o.getMatrix())

    def __str__(self):
        return str(self.matrix)




class MultiDensityMatrix(DensityMatrix):

    def __init__(self, matrix:np.array):
        self.matrix = matrix
        if not np.trace(matrix) - 1 < 1e-10:
            log.warn("This matrix does not have unit trace!!!")
        if not self.isHermitian():
            log.warn("This matrix is not hermitian!!!")
        if not matrix.shape[0] == matrix.shape[1]:
            log.fail("rho is not square!")



    def getax(self):
        return np.trace(np.dot(Pauli.x(), self.matrix))
    def getay(self):
        return np.trace(np.dot(Pauli.y(), self.matrix))
    def getaz(self):
        return np.trace(np.dot(Pauli.z(), self.matrix))


    def getBlochVector(self):
        return np.array([self.getax(), self.getay(), self.getaz()])


    def isPure(self):
        return np.all(np.dot(self.matrix, self.matrix) - self.matrix < 1e-15)

    def isSeperable(self):
        return np.all(np.dot(self.matrix, self.matrix) - self.matrix < 1e-15)

    def isHermitian(self):
        return np.all(self.matrix == np.transpose(np.conjugate(self.matrix)))

    def getMatrix(self):
        return self.matrix

    

        
    def partialTranspose():
        pass
 





class Pauli:
    x=np.array([[0, 1], [1, 0]])
    y=np.array([[0, -1j], [1j, 0]])
    z=np.array([[1, 0], [0, -1]])

    @staticmethod
    def x():
        return np.array([[0, 1], [1, 0]])

    @staticmethod
    def y():
        return np.array([[0, -1j], [1j, 0]])

    @staticmethod
    def z():
        return np.array([[1, 0], [0, -1]])



class Bell:
    v_phi_p=MultiDensityMatrix(1/2*np.array([[1,0,0,1],[0,0,0,0],[0,0,0,0],[1,0,0,1]]))
    v_phi_m=MultiDensityMatrix(1/2*np.array([[1,0,0,-1],[0,0,0,0],[0,0,0,0],[-1,0,0,1]]))
    v_psi_p=MultiDensityMatrix(1/2*np.array([[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]]))
    v_psi_m=MultiDensityMatrix(1/2*np.array([[0,0,0,0],[0,1,-1,0],[0,-1,1,0],[0,0,0,0]]))

    @staticmethod
    def phi_p():
        return Bell.v_phi_p

    @staticmethod
    def phi_m():
        return Bell.v_phi_m

    @staticmethod
    def psi_p():
        return Bell.v_psi_p

    @staticmethod
    def psi_m():
        return MultiDensityMatrix(np.array([[0,0,0,0],[0,1,-1,0],[0,-1,1,0],[0,0,0,0]]))




if __name__ == "__main__":
    ts = TwoState(1j, 0)
    log.green(ts)
    t = DensityMatrix(np.array([[0.5,0],[0,0.5]]))

    print(t.getax())

    ts = TwoState(0.2+0.4j, np.sqrt(1-(0.2+0.4j)*(0.2-0.4j)))
    print(ts.getBlochVector())
    print(np.dot(ts.getBlochVector(),ts.getBlochVector().conjugate()))




class Channel:

    def __init__(self):
        pass




class KrausChannel(Channel):
    def __init__(self, operators):
        self.operators = operators
        if not self.isKraus(operators):
            log.fail("The operators given are not a valid set of Kraus operators")
            

    def isKraus(self, ops):
        res = np.zeros_like(ops[0])
        for op in ops:
            res += np.transpose(op.conjugate()) @ op
        return np.all(abs(res - np.eye(2)) < 1e-10)

    def apply(self, rho:DensityMatrix):
        matrix = rho.getMatrix()
        temp = np.zeros_like(matrix)
        for op in self.operators:
            temp += op @ matrix @ np.transpose(op.conjugate())
        return DensityMatrix(temp)




# some operators
class H(Operator):
    def __init__(self):
        matrix = 1/np.sqrt(2)*np.array([[1,1],[1,-1]])
        super().__init__(matrix)


iSWAP = Operator(np.array([[1,0,0,0],[0,0,1j,0],[0,1j,0,0],[0,0,0,1]]))
CNOT_default = Operator(np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]]))


def CNOT(control:int, target:int, Nqubits:int):
    """
    Apply the gate `U` to the qubits in `idx`, controlled by the c-th qubit.
    """
    assert 0 <= control < Nqubits
    assert 0 <= target < Nqubits
    assert 2 <= Nqubits

    down = np.array([1,0])
    up = np.array([0,1])
    mini = min(control, target)
    maxi = max(control, target)

    id1 = np.eye(2**mini)
    id2 = np.eye(2**(maxi - mini - 1))
    id3 = np.eye(2**(Nqubits - maxi-1))

    if mini == control:
        res = np.kron(id1, np.kron(np.outer(up, up), np.kron(id2, np.kron(Pauli().x(), id3)))) + np.kron(id1, np.kron(np.outer(down, down), np.eye(2**(Nqubits - mini - 1))))
    else:
        res = np.kron(id1, np.kron(Pauli().x() , np.kron(id2, np.kron(np.outer(up, up), id3)))) + np.kron(id1, np.kron(np.eye(2), np.kron(id2, np.kron(np.outer(down, down), id3))))
    return res



def toefeli(control1:int, control2:int, target:int, Nqubits:int):
    assert not control1 == control2, log.errorStr("Control1 and 2 have to be different qubits!")
    assert not control2 == target, log.errorStr("Control2 and target have to be different qubits!")
    assert 0 <= control1 < Nqubits, log.errorStr("Number of qubits has to be larger than the control1 qubit!")
    assert 0 <= control2 < Nqubits, log.errorStr("Number of qubits has to be larger than the control2 qubit!")
    assert 0 <= target < Nqubits, log.errorStr("Number of qubits has to be larger than the target qubit!")
    assert Nqubits >= 3, log.errorStr("Number of qubits has to be larger or equal 3!")

    down = np.array([1,0])
    up = np.array([0,1])
    mini = min(control1, control2, target)
    maxi = max(control1, control2, target)
    middle = control1 if not (mini==control1 or maxi==control1) else control2 if not (mini==control2 or maxi==control2) else target

    id1 = np.eye(2**mini)
    if middle > mini:
        id2 = np.eye(2**(middle - mini - 1))
    else:
        id2 = 1
    if maxi > middle:
        id3 = np.eye(2**(maxi - middle - 1))
    else:
        id3 = 1
    id4 = np.eye(2**(Nqubits - maxi-1))

    if not (mini == control1 or mini == control2):
        res = np.kron(id1, np.kron(Pauli().x(), np.kron(id2, np.kron(np.outer(up, up), np.kron(id3, np.kron(np.outer(up, up), id4))))))
        res += np.kron(np.eye(2**middle), np.kron(np.outer(down, down), np.kron(id3, np.kron(np.outer(down, down), id4))))
        res += np.kron(np.eye(2**middle), np.kron(np.outer(up, up), np.kron(id3, np.kron(np.outer(down, down), id4))))
        res += np.kron(np.eye(2**middle), np.kron(np.outer(down, down), np.kron(id3, np.kron(np.outer(up, up), id4))))
    elif not (middle == control1 or middle == control2):
        res = np.kron(id1, np.kron(np.kron(up, up), np.kron(id2, np.kron(Pauli.x(), np.kron(id3, np.kron(np.outer(up, up), id4))))))
        res += np.kron(id1, np.kron(np.outer(down, down), np.kron(id2, np.kron(np.eye(2), np.kron(id3, np.kron(np.outer(down, down), id4))))))
        res += np.kron(id1, np.kron(np.outer(down, down), np.kron(id2, np.kron(np.eye(2), np.kron(id3, np.kron(np.outer(up, up), id4))))))
        res += np.kron(id1, np.kron(np.outer(up, up), np.kron(id2, np.kron(np.eye(2), np.kron(id3, np.kron(np.outer(down, down), id4))))))
    else:
        res = np.kron(id1, np.kron(np.outer(up, up), np.kron(id2, np.kron(np.outer(up, up), np.kron(id3, np.kron(Pauli().x(), id4))))))
        res += np.kron(id1, np.kron(np.outer(down, down), np.kron(id2, np.kron(np.outer(down, down), np.eye(2**(Nqubits - middle - 1))))))
        res += np.kron(id1, np.kron(np.outer(up, up), np.kron(id2, np.kron(np.outer(down, down), np.eye(2**(Nqubits - middle - 1))))))
        res += np.kron(id1, np.kron(np.outer(down, down), np.kron(id2, np.kron(np.outer(up, up), np.eye(2**(Nqubits - middle - 1))))))
        
        

    # else:
    #     id2 = np.eye(2**(maxi - mini - 1))
    #     id3 = np.eye(2**(Nqubits - maxi-1))

    #     if mini == control:
    #         res = np.kron(np.outer(up, up), np.kron(id2, np.kron(Pauli().x(), id3))) + np.kron(np.outer(down, down), np.kron(id2, np.kron(np.eye(2), id3)))
    #     else:
    #         res = np.kron(Pauli().x() , np.kron(id2, np.kron(np.outer(up, up), id3))) + np.kron(np.eye(2), np.kron(id2, np.kron(np.outer(down, down), id3)))

    return res



ghz = MultiState(1/np.sqrt(2)*np.array([1, 0, 0, 0, 0, 0, 0, 1]))
W = MultiState(1/np.sqrt(3) * np.array([0, 1, 1, 0, 1, 0, 0, 0]))

def kron(op1, op2):
    m1 = op1
    m2 = op2
    if isinstance(op1, Operator):
        m1 = op1.getMatrix()
    if isinstance(op2, Operator):
        m2 = op2.getMatrix()
    return Operator(np.kron(m1, m2))



def getOperator(op, pos:int, n_qubits:int):
    assert 0<=pos<n_qubits, log.errorStr("Position of Operator must be lower than number of qubits and greater than 0!")
    if isinstance(op, Operator):
        op = op.getMatrix()
    opLen = int(np.log2(op.shape[0]))
    assert pos+opLen<=n_qubits, log.errorStr("Operator dimension is too large!")

    if pos > 0:
        before = np.eye(2**(pos))
    else:
        before = 1
    after = np.eye(2**(n_qubits-pos-opLen))
    return kron(before, kron(op, after))




if __name__ == "__main__":
    ep = 0.1245
    em = .3450

    k1 = np.sqrt((1+ep)/2) * 1/np.sqrt(2)*np.array([[1, 1], [0,0]])
    k2 = np.sqrt((1-ep)/2) * 1/np.sqrt(2)*np.array([[0, 0], [1,1]])
    k3 = np.sqrt((1+em)/2) * 1/np.sqrt(2)*np.array([[1, -1], [0,0]])
    k4 = np.sqrt((1-em)/2) * 1/np.sqrt(2)*np.array([[0, 0], [1,-1]])

    channel = KrausChannel([k1, k2, k3, k4])

    rho = DensityMatrix(np.array([[0.5 + 0.25*(ep+em), 0], [0, 0.5 - 0.25*(ep+em)]]))