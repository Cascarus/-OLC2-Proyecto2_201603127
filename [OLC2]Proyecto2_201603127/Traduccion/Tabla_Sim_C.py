class Simbolo():
    def __init__(self, id, tipo, rol, ambito, parametros, tam, var_aug):
        self.id = id
        self.tipo = tipo
        self.rol = rol
        self.ambito = ambito
        self.parametros = parametros
        self.tam = tam
        self.var_aug = var_aug

class Tabla_Simbolos():
    def __init__(self):
        self.simbolos = {}

    def add_simbolo(self, simbolo):
        self.simbolos[simbolo.id] = simbolo

    def get_simbolo(self, id):
        if not id in self.simbolos:
            print("no existe el simbolo")
            return Simbolo(None, None, None, None, None, None, None)
        return self.simbolos[id]
        # imprimir error

    def update_simbolo(self, simbolo):
        if simbolo.id in self.simbolos:
            self.simbolos[simbolo.id] = simbolo


    def existe_simbolo(self, simbolo):
        if simbolo.id in self.simbolos:
            return True
        return False

    def existe_id(self, id):
        if id in self.simbolos:
            return True
        return False

    def clear(self):
        self.simbolos.clear()

    def get_all(self):
        return self.simbolos

    def delete_simbolo(self, id):
        if id in self.simbolos:
            texto = self.simbolos.pop(id)
            return True
        return False

    def print_tabla(self):
        for simbolo in self.simbolos:
            temp = self.get_simbolo(simbolo)
            print("simbolo: ", str(temp.id), " tipo: ", str(temp.tipo), " Valor: ", str(temp.valor))