from Traduccion.Tabla_Sim_C import Tabla_Simbolos, Simbolo


class ambito():
  def __init__(self, padre):
    self.ts = Tabla_Simbolos()
    #self.ts.clear()
    self.padre = padre

  def get_simbol(self, id):
    pivote = self

    while pivote != None:
      if pivote.ts.existe_id(id):
        return pivote.ts.get_simbolo(id)

      pivote = pivote.padre

  def exite_aqui(self, id):
    return self.ts.existe_id(id)

  def agregar_simbolo(self, simbolo):
    self.ts.add_simbolo(simbolo)