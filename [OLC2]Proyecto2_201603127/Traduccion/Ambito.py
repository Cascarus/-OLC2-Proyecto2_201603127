from Traduccion.Tabla_Sim_C import Tabla_Simbolos, Simbolo


class ambito():

    def __init__(self, padre):
      self.ts = Tabla_Simbolos()
      self.fun_ts = {}
      self.padre = padre

    def get_simbol(self, id):
      pivote = self

      while pivote != None:
        if pivote.ts.existe_id(id):
          return pivote.ts.get_simbolo(id)

        pivote = pivote.padre
      return False

    def agregar_funcion(self, id, simbolo):
        pivote = self

        while pivote.padre != None:
            pivote = pivote.padre

        if not id in pivote.fun_ts:
            pivote.fun_ts[id] = simbolo
            return True
        return False

    def get_funcion(self, id):
        pivote = self

        while pivote.padre != None:
            pivote = pivote.padre

        if id in pivote.fun_ts:
            return pivote.fun_ts[id]
        return None

    def existe_funcion(self, id):
        pivote = self
        while pivote.padre != None:
            pivote = pivote.padre

        if id in pivote.fun_ts:
            return True
        return False

    def exite_aqui(self, id):
      return self.ts.existe_id(id)

    def agregar_simbolo(self, simbolo):
      self.ts.add_simbolo(simbolo)