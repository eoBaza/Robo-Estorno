from BancoDados.Database import Database
from Script_Estorno.Pix import Token
from BancoDados.Queryes import *
import certifi

class ExtrairTXID:
    def __init__(self, host=None):
        self.token = Token()
        self.db = Database()
        if host:
            self.db.host = host
        self.cupom = None
        self.pedido = None
        self.saque = None
        self.txid = None

    @staticmethod
    def extrair_cupom(txid, filial):
        if len(filial) == 3:
            return txid[15:21]
        elif len(filial) == 2:
            return txid[16:22]
        elif len(filial) == 1:
            return txid[18:23]
        else:
            return None

    def validacao_cupom(self, txid, filial):
        self.txid = txid
        self.cupom = self.extrair_cupom(txid, filial)
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            query, parametros = get_cupom(self.cupom)
            cursor.execute(query, parametros)
            result = cursor.fetchone()
            if result:
                print(f"O cupom associado ao número {self.cupom} está finalizado" if result[2] else f"O cupom associado ao numero {self.cupom} não está finalizado.")
                return result
            else:
                print(f"O cupom associado ao número {self.cupom} não foi encontrado.")
                return False
        except Exception as e:
            print(f"Erro Cupom:{e}")
        finally:
            self.db.desconectar()

    def validacao_pedido(self, txid):
        self.txid = txid
        self.pedido = self.txid[15:24]
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            query, parametros = get_pedido(self.pedido)
            cursor.execute(query, parametros)
            result = cursor.fetchone()
            if result:
                print(f"O pedido associado ao número {self.pedido} está finalizado." if result[2] else f"O pedido associado ao número {self.pedido} não está finalizado.")
                return result
            else:
                print(f"O pedido associado ao número {self.pedido} não foi encontrado.")
                return False
        except Exception as e:
            print(f"Erro Pedido:{e}")
        finally:
            self.db.desconectar()

    def validacao_saque(self, txid):
        self.txid = txid
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            query, parametros = get_saque(self.txid)
            cursor.execute(query, parametros)
            result = cursor.fetchall()
            if result:
                print("\n=============================================")
                for i in result:
                    registro = {
                        "valor": i[0],
                        "nsu": i[1],
                        "tx_id": i[2],
                        "data_inicio": i[3],
                        "Data_fim": i[4]
                    }
                    print(registro)
                print("=============================================")

                data_fim = result[0][4]
                valor = result[0][0]
                nsu = result[0][1]

                if data_fim:
                    print(f"""====== RESPOSTA FINAL DO ROBO=============\nFoi verificado que os Saques-Pix foram efetuados e Recebidos na conta da Quero-Quero, e os cupons finalizaram:\nTXID: {self.txid}\nNSU: {nsu}\nValor: R${valor}
                        """)
                else:
                    print(f"""====== RESPOSTA FINAL DO ROBO=============\nFoi verificado que o Saque-Pix foi efetuado e Recebido na conta da Quero-Quero, porém não finalizou o Cupom no PDV. Favor validar se será necessário o estorno do valor.\nTXID: {self.txid}\nNSU: {nsu}\nValor: R${valor}""")

                return {
                    "valor": valor,
                    "nsu": nsu,
                    "txid": self.txid,
                    "data_fim": data_fim
                }

            else:
                print("\n==============================\nNAO FOI ENCONTRADO NA TABELA SAQUE PIX, PROCURANDO NA TABELA PAGAMENTO PIX......")
                query, parametros = get_saque_pagamento_pix(self.txid)
                cursor.execute(query, parametros)
                result_pagpix = cursor.fetchall()
                for i in result_pagpix:
                    print(f"\n ====== Resultados Pagamento Pix ======\n",
                          f"Valor: {i[0]}\n",
                          f"Data Inclusao: {i[1]}\n=========================\n")
                if result_pagpix:
                    valor_pagamentopix = result_pagpix[0][0]
                    data_inclusao = result_pagpix[0][1]
                    query, parametros = get_saque_cupom(data_inclusao, valor_pagamentopix)
                    cursor.execute(query, parametros)
                    result_cupom = cursor.fetchone()
                    if result_cupom:
                        self.token.txid = self.txid
                        detalhes_pix = self.token.obter_detalhes_pix()
                        if detalhes_pix:
                            nsu = detalhes_pix["end_to_end"]
                        else:
                            nsu = "NAO ENCONTRADO NA API"
                        print(f"Esta finalizado na cupom: {result_cupom[0]}")
                        print(f"""====== RESPOSTA FINAL DO ROBO=============\nFoi verificado que o Saque-Pix foi efetuado e Recebido na conta da Quero-Quero, porém não finalizou o Cupom no PDV. Favor validar se será necessário o estorno do valor.\nTXID: {self.txid}\nNSU: {nsu}\nValor: {valor_pagamentopix}""")
                        return {
                            "valor": valor_pagamentopix,
                            "nsu": nsu,
                            "txid": self.txid,
                            "data_fim": None
                        }
                    else:
                        print("Nenhum cupom encontrado. Favor validar manualmente este saque pix")
        except Exception as e:
            print(f"Erro Saque:{e}")
        finally:
            self.db.desconectar()