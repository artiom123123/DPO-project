import numpy as np
class atom:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.coordinates = [self.x, self.y, self.z]
    
    def change_coordinates(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.coordinates = [self.x, self.y, self.z]

class Supercell:
    def __init__(self, x_zero_index, y_zero_index, z_zero_index, typ='Face_centered_cubic'):
        if typ =='Face_centered_cubic':
            cells = 7
            size = cells * 2 + 1
            self.atoms = []#[[x_zero_index + x, y_zero_index + y, z_zero_index + z] for x in range(size) for y in range(size) for z in range(size) if sum((x,y,z))%2 != 1]
            
            for x in range(x_zero_index, x_zero_index + size):
                for y in range(y_zero_index, y_zero_index + size):
                    for z in range(z_zero_index, z_zero_index + size):
                        if sum((x, y, z))%2 != 1:
                            self.atoms.append(atom(x, y, z))

            self.atom_coordinates = [i.coordinates for i in self.atoms]
    
    def change_atom(self, atom:atom):
        if atom.coordinates in self.atom_coordinates:
            index = self.atom_coordinates.index(atom.coordinates)
            self.atoms[index] = atom
            self.atom_coordinates = [i.coordinates for i in self.atoms]
        
    def get_atom(self, x, y, z) -> atom:
        return self.atoms[self.atom_coordinates.index([x, y, z])]

    def refresh_atom_coordinates(self):
        self.atom_coordinates = [i.coordinates for i in self.atoms]

def iscross(a:Supercell, b:Supercell):
    for atom in a.atoms:
        if atom.coordinates in b.atom_coordinates:
            b.change_atom(atom)

def Force(coordinates=np.array([1,1])):
    e = 8.85 * 10**-12
    sigma = 3.8 * 10**-10
    def U(distance: np.ndarray)-> np.ndarray: 
        return 4*e * (sigma**12 / distance**12 - sigma**6 / distance**6)
    def dU(distance: np.ndarray)-> np.ndarray:
        return 24*e * (sigma**6 / distance**13 - 2 * sigma**12 / distance**13)
    def VecModule(vectors: np.array)-> np.array: # Длина векторов
        return np.sqrt(np.sum(vectors**2, 1))
    def VecDir(vectors: np.array)-> np.array: # Сонаправленные вектора длиной 1 (Их напраления)
        module = VecModule(vectors)
        return vectors / module.reshape(module.size, 1)
    dUvectors = dU(VecModule(coordinates))
    return np.sum(dUvectors.reshape(dUvectors.size, 1) * VecDir(coordinates))

# a = Supercell(0, 0, 0)
# b = Supercell(0, 0, 2)
# iscross(a, b)
# a.get_atom(2,2,2).change_coordinates(2, 2, 3)
# # print(a.atom_coordinates)
# a.refresh_atom_coordinates()
# b.refresh_atom_coordinates()

# print(a.atom_coordinates,'\n', b.atom_coordinates)

# print(Force())
a = np.array([[1, 2, 1],[1, 3, 1]])

print(Force(a))

