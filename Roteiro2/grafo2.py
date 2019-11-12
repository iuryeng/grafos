class VerticeInvalidoException(Exception):
    pass

class ArestaInvalidaException(Exception):
    pass

class Grafo:

    QTDE_MAX_SEPARADOR = 1
    SEPARADOR_ARESTA = '-'

    def __init__(self, N=[], A={}):
        '''
        Constrói um objeto do tipo Grafo. Se nenhum parâmetro for passado, cria um Grafo vazio.
        Se houver alguma aresta ou algum vértice inválido, uma exceção é lançada.
        :param N: Uma lista dos vértices (ou nodos) do grafo.
        :param V: Uma dicionário que guarda as arestas do grafo. A chave representa o nome da aresta e o valor é uma string que contém dois vértices separados por um traço.
        '''
        for v in N:
            if not(Grafo.verticeValido(v)):
                raise VerticeInvalidoException('O vértice ' + v + ' é inválido')

        self.N = N

        for a in A:
            if not(self.arestaValida(A[a])):
                raise ArestaInvalidaException('A aresta ' + A[a] + ' é inválida')

        self.A = A

    def arestaValida(self, aresta=''):
        '''
        Verifica se uma aresta passada como parâmetro está dentro do padrão estabelecido.
        Uma aresta é representada por um string com o formato a-b, onde:
        a é um substring de aresta que é o nome de um vértice adjacente à aresta.
        - é um caractere separador. Uma aresta só pode ter um único caractere como esse.
        b é um substring de aresta que é o nome do outro vértice adjacente à aresta.
        Além disso, uma aresta só é válida se conectar dois vértices existentes no grafo.
        :param aresta: A aresta que se quer verificar se está no formato correto.
        :return: Um valor booleano que indica se a aresta está no formato correto.
        '''

        # Não pode haver mais de um caractere separador
        if aresta.count(Grafo.SEPARADOR_ARESTA) != Grafo.QTDE_MAX_SEPARADOR:
            return False

        # Índice do elemento separador
        i_traco = aresta.index(Grafo.SEPARADOR_ARESTA)

        # O caractere separador não pode ser o primeiro ou o último caractere da aresta
        if i_traco == 0 or aresta[-1] == Grafo.SEPARADOR_ARESTA:
            return False

        # Verifica se as arestas antes de depois do elemento separador existem no Grafo
        if not(self.existeVertice(aresta[:i_traco])) or not(self.existeVertice(aresta[i_traco+1:])):
            return False

        return True

    @classmethod
    def verticeValido(self, vertice=''):
        '''
        Verifica se um vértice passado como parâmetro está dentro do padrão estabelecido.
        Um vértice é um string qualquer que não pode ser vazio e nem conter o caractere separador.
        :param vertice: Um string que representa o vértice a ser analisado.
        :return: Um valor booleano que indica se o vértice está no formato correto.
        '''
        return vertice != '' and vertice.count(Grafo.SEPARADOR_ARESTA) == 0

    def existeVertice(self, vertice=''):
        '''
        Verifica se um vértice passado como parâmetro pertence ao grafo.
        :param vertice: O vértice que deve ser verificado.
        :return: Um valor booleano que indica se o vértice existe no grafo.
        '''
        return Grafo.verticeValido(vertice) and self.N.count(vertice) > 0

    def existeAresta(self, aresta=''):
        '''
        Verifica se uma aresta passada como parâmetro pertence ao grafo.
        :param aresta: A aresta a ser verificada
        :return: Um valor booleano que indica se a aresta existe no grafo.
        '''
        existe = False
        if Grafo.arestaValida(self, aresta):
            for k in self.A:
                if aresta == self.A[k]:
                    existe = True

        return existe

    def adicionaVertice(self, v):
        '''
        Adiciona um vértice no Grafo caso o vértice seja válido e não exista outro vértice com o mesmo nome
        :param v: O vértice a ser adicionado
        :raises: VerticeInvalidoException se o vértice passado como parâmetro não puder ser adicionado
        '''
        if self.verticeValido(v) and not self.existeVertice(v):
            self.N.append(v)
        else:
            raise VerticeInvalidoException('O vértice ' + v + ' é inválido')

    def adicionaAresta(self, nome, a):
        '''
        Adiciona uma aresta no Grafo caso a aresta seja válida e não exista outra aresta com o mesmo nome
        :param v: A aresta a ser adicionada
        :raises: ArestaInvalidaException se a aresta passada como parâmetro não puder ser adicionada
        '''
        if self.arestaValida(a):
            self.A[nome] = a
        else:
            ArestaInvalidaException('A aresta ' + self.A[a] + ' é inválida')

    def vertices_nao_adjacentes(self):
        lista_de_valores = self.A.values()
        resultado = []
        for i in self.N:
            for j in self.N:
                indo = '{}-{}'.format(i, j)
                vindo = '{}-{}'.format(j, i)
                if indo not in lista_de_valores and vindo not in lista_de_valores:
                    resultado.append(indo)
        return resultado

    def ha_laco(self):
        lista_de_valores = self.A.values()
        for i in self.N:
            for j in self.N:
                aresta = '{}-{}'.format(i, j)
                if(i==j) and aresta in lista_de_valores:
                    return True
        return False

    def ha_paralelas(self):
        count = 0
        lista_de_valores = self.A.values()
        for i in lista_de_valores:
            for j in lista_de_valores:
                i1, i2 = i.split('-')
                j1, j2 = j.split('-')
                if i1 == j1:
                    if i2 == j2:
                        count += 1
                elif i1 == j2:
                    if i2 == j1:
                        count += 1
            if count == 2:
                return True
            count = 0
        return False

    def grau(self, vertice):
        count = 0
        lista_de_valores = self.A.values()
        for i in lista_de_valores:
            i1, i2 = i.split('-')
            if(vertice == i1) or (vertice == i2):
                count += 1
        return count

    def arestas_sobre_vertice(self,vertice):
        resultado = []
        for i in self.A.keys():
            aresta = self.A.get(i)
            a1, a2 = aresta.split('-')
            if a1 == vertice or a2 == vertice:
                resultado.append(i)
        return resultado

    def eh_completo(self):
        for i in self.N:
            for j in self.N:
                aresta = '{}-{}'.format(i, j)
                aresta2 = '{}-{}'.format(j, i)
                if self.existeAresta(aresta) or self.existeAresta(aresta2):
                    pass
                elif(i == j):
                    pass
                else:
                    return False
        return True

    def vertices_adjacentes(self, vertice):
        resultado = []
        arestas_sobre_vertice = self.arestas_sobre_vertice(vertice)
        for i in range(0, len(arestas_sobre_vertice)):
            resultado.append(self.A.get(arestas_sobre_vertice[i]))
            i1, i2 = resultado[i].split('-')
            if i1 == vertice:
                resultado[i] = i2
            elif i2 == vertice:
                resultado[i] = i1
        return resultado

    def dfs(self,vertice):
        retorno = [vertice]
        return self.recursao(vertice,retorno)

    def recursao(self, vertice, retorno):
        arestas_sobre_vertice = self.arestas_sobre_vertice(vertice)
        vertices_adjacentes = self.vertices_adjacentes(vertice)
        for i in range(0, len(vertices_adjacentes)):
                if vertices_adjacentes[i] not in retorno:
                    retorno.append(arestas_sobre_vertice[i])
                    retorno.append(vertices_adjacentes[i])
                    retorno = self.recursao(vertices_adjacentes[i], retorno)
        return retorno

    def __str__(self):
        '''
        Fornece uma representação do tipo String do grafo.
        O String contém um sequência dos vértices separados por vírgula, seguido de uma sequência das arestas no formato padrão.
        :return: Uma string que representa o grafo
        '''
        grafo_str = ''

        for v in range(len(self.N)):
            grafo_str += self.N[v]
            if v < (len(self.N) - 1):  # Só coloca a vírgula se não for o último vértice
                grafo_str += ", "

        grafo_str += '\n'

        for i, a in enumerate(self.A):
            grafo_str += self.A[a]
            if not(i == len(self.A) - 1): # Só coloca a vírgula se não for a última aresta
                grafo_str += ", "

        return grafo_str































