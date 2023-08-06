from datetime import datetime
import this
import numpy as np
from .utils.io_container_data import IOContainerData
from .banco_dados.conexao_banco import ConexaoBanco
import pandas as pd
import os
import logging
import threading


class Util():

    def get_path_file_bronze(path_file, sub_dir, is_date=True):
        return Util.get_path_file(path_file, 'incoming', sub_dir, is_date)


    def get_path_file_silver(path_file, sub_dir, is_date=True):
        return Util.get_path_file(path_file, 'input', sub_dir, is_date)

    def get_path_file(path_file, sub_dir_origem , sub_dir_destino, is_date=True):
        path = os.path.dirname(path_file).replace(sub_dir_origem, sub_dir_destino)
        if(is_date):
            return path + str( datetime.today().strftime('%Y-%m-%d') )
        else:
            return path

    def get_name_file(path_file,is_hora=True):

        name = os.path.basename(path_file)
        if(is_hora):
            return str( datetime.today().strftime('%H.%M.%S_') ) + name
        else:
            return name

    def get_chunksize():
        return 100000


class Bronze():

    def __init__(self, path_file, sep=',',  header=0, dtype=None) :
    
        self.ioContainerData = IOContainerData()
        self.path_file = path_file
        self.sep = sep
        self.sep_processado = ';'
        self.header = header
        self.dtype = dtype

    def start(self):

        msg = ""
        sucesso = True

        try:
            logging.info(f"Arquivo {self.path_file}")
            self.__break_file()
            self.__backup()
        except Exception as e:
            logging.error(f"Falha no processo {e}")
            msg = msg +  f"\nFalha no processo {e}. "
            sucesso = False
        finally:
            logging.info("Fim do processo")
            msg = msg + "\nFim do processo. "

        return sucesso, msg


    def __break_file(self):

        df_data = self.ioContainerData.load(
            self.path_file, 
            self.ioContainerData.name_container_bronze, 
            sep=self.sep, 
            header=self.header,  
            dtype=self.dtype,
            chunksize = Util.get_chunksize()
        )

        extensao = self.ioContainerData.get_extension(self.path_file)

        logging.info(f"Extensão do arquivo {extensao}")

        file_name = Util.get_name_file(self.path_file, 
                                        is_hora=False)

        path_input_enrichment_input = Util.get_path_file_bronze(self.path_file,
                                        self.ioContainerData.dir_input_enrichment_input,
                                        is_date=False)


        if extensao == ".xlsx" or extensao == ".xls":

            file_input_enrichment_input = os.path.join(path_input_enrichment_input, file_name + "_1.csv")

            self.ioContainerData.download(df_data, 
                                        file_input_enrichment_input,
                                        self.ioContainerData.name_container_silver,
                                        self.sep_processado)
        else:
            count = 1
            for chunk in df_data:
        
                logging.info(f"Iniciando quebra do arquivo {self.path_file} do lote {count}")

                if isinstance(chunk, pd.DataFrame):
                    _df_data = chunk
                else:
                   _df_data = next(chunk)

                file_input_enrichment_input = os.path.join(path_input_enrichment_input, file_name + "_"+str(count)+".csv")


                #threading.Thread(
                #        target=self.ioContainerData.download, 
                #        args=(_df_data,
                #                file_input_enrichment_input,
                #                self.ioContainerData.name_container_silver,
                #                self.sep_processado)).start()

               

                self.ioContainerData.download(_df_data, 
                            file_input_enrichment_input,
                            self.ioContainerData.name_container_silver,
                            self.sep_processado)

                del(_df_data)
                logging.info(f"Fim da quebra do arquivo {self.path_file} do lote {count}")
                count = count + 1



    def __backup(self):
    
        file_name = Util.get_name_file(self.path_file)
        path_backup = Util.get_path_file_bronze(self.path_file, self.ioContainerData.dir_backup)
        backup = os.path.join(path_backup, file_name)

        self.ioContainerData.cp_file( self.path_file, 
                                      backup, 
                                      self.ioContainerData.name_container_bronze
                                    )
        logging.info(f'Arquivo salvo em backup {self.ioContainerData.name_container_bronze}/{backup}')

    #def __copy_input_enrichment(self):
    
    #    file_name = __get_name_file(is_hora=False)
    #    path_input_enrichment_input =  __get_path_file(self.ioContainerData.dir_input_enrichment_input,is_date=False)
    #    file_input_enrichment_input = os.path.join(path_input_enrichment_input, file_name)

    #    self.ioContainerData.cp_file( 
    #        self.path_file, 
    #        file_input_enrichment_input, 
    #        self.ioContainerData.name_container_bronze,
    #        self.ioContainerData.name_container_silver )
  
    #    logging.info(f'Arquivo movido para {file_input_enrichment_input}')

    #    return file_input_enrichment_input



""" Classe do silver"""
class Silver():

    def __init__(self, path_file, sep=';',  header=0, dtype=None) :

        self.ioContainerData = IOContainerData()
        self.conexaoBanco = ConexaoBanco()
        self.path_file = path_file
        self.sep = sep
        self.header = header
        self.dtype = dtype

    def run(self, dictParametros ):

        logging.info(f"Iniciando o processa de tratamento do arquivo")

        logging.info(f"Separador {self.sep}")
        logging.info(f"Posição do cabeçalho {self.header}")
        logging.info(f"Tipo de dado {self.dtype}")

        df_datas = self.ioContainerData.load(
            self.path_file, 
            self.ioContainerData.name_container_silver, 
            sep=self.sep, 
            header=self.header,  
            dtype=self.dtype,
            chunksize= Util.get_chunksize()
        )

        _is_first_file = self.__is_first_file()
        count = 1
        for df_data in df_datas:
            try:
            
                logging.info(f"Iniciando o processo de enrichment {count}")
                if isinstance(df_data, pd.DataFrame):
                     self.dados_original = df_data
                else:
                    self.dados_original = next(df_data)

                self.__processamento(dictParametros, _is_first_file and (count == 1) )

                count = count + 1 
                del(self.dados_original)
                logging.info(f"Fim do processo de enrichment {count}")
                
            except Exception as error:
                raise Exception(f"{error}")


    def __is_first_file(self):
        return self.path_file.endswith("_1.csv")


    def __processamento(self, dictParametros, is_first_processing):

        try:
            for key in dictParametros:

                parametro = dictParametros[key]

                if parametro.type_insert_table == 'append':
                    is_first_processing = False
                

                self.dados = self.__get_field(parametro.list_columns_to_use)

                self.__rename_field(parametro.list_columns_rename)
               
                self.__enrichment_sql(parametro.list_parametros_enrichment_sql)
               
                self.__delete_columns(parametro.list_columns_delete)
              
                self.__delete_lines(parametro.list_lines_delete)
               
                self.__drop_lines_duplicates(parametro.list_lines_duplicates, key, is_first_processing)

                self.__format_date(parametro.list_columns_format_date)

                self.__create_columns_analytics_apply(parametro.list_analytics)

                self.__reorganize_field(parametro.list_field_reorganize)

                self.__save_enrichment()
       
                self.__insert_data_base(key, parametro.type_insert_table , is_first_processing)

                self.__removido_input_enrichment()

                del(self.dados)

        except Exception as error:
            raise Exception(f"{error}")

   
    def __removido_input_enrichment(self):
        self.ioContainerData.delete()

        logging.info(f'Arquivo removido')

    def fail(self):
   
        file_name = Util.get_name_file(self.path_file)
        path_failed = Util.get_path_file_bronze(self.path_file, self.ioContainerData.dir_failed)
        failed = os.path.join(path_failed, file_name)

        self.ioContainerData.mv_file( self.path_file, 
                                      failed, 
                                      self.ioContainerData.name_container_silver, 
                                      self.ioContainerData.name_container_bronze 
                                    )

        logging.info(f'Arquivo salvo em falha {self.ioContainerData.name_container_bronze}/{failed}')


    def __delete_lines(self, list_lines_delete):

        try:
            if(list_lines_delete != None):
                logging.info(f"Iniciando o processo de deleção das linhas")

                for lines_delete in list_lines_delete:

                    if(lines_delete[1] == '=='):
                        self.dados = self.dados[ self.dados[ lines_delete[0] ] != lines_delete[2] ] 
                    elif(lines_delete[1] == '!='):
                        self.dados = self.dados[ self.dados[ lines_delete[0] ] == lines_delete[2] ]
                    elif(lines_delete[1] == '>'):
                        self.dados = self.dados[ self.dados[ lines_delete[0] ] > lines_delete[2] ] 
                    elif(lines_delete[1] == '>='):
                        self.dados = self.dados[ self.dados[ lines_delete[0] ] >= lines_delete[2] ] 
                    elif(lines_delete[1] == '<'):
                        self.dados = self.dados[ self.dados[ lines_delete[0] ] < lines_delete[2] ] 
                    elif(lines_delete[1] == '<='):
                        self.dados = self.dados[ self.dados[ lines_delete[0] ] <= lines_delete[2] ] 
                    elif(lines_delete[1] == 'nan'):
                        self.dados=self.dados.dropna(subset=lines_delete[0])
                    elif(lines_delete[1] == 'isnumeric'):
                        self.dados = self.dados[ self.dados[ lines_delete[0] ].str.isnumeric() ]


        except Exception as error:
            raise Exception(f"Erro ao deletar linha {error}")


    def __drop_lines_duplicates(self, list_lines_duplicates, name_table, is_first_processing):
        
        try:
            if(list_lines_duplicates != None):
                logging.info(f"Iniciando o processo de drop em linhas duplicadas")
                self.dados.drop_duplicates(list_lines_duplicates, inplace=True) 
                if(is_first_processing == False):

                    colunas = []
                    for coluna in list_lines_duplicates:
                        colunas.append(coluna )

                    query = "SELECT distinct " + ",".join(colunas) + " FROM " + name_table
                    _pd = self.conexaoBanco.select(query)

                    filtros = []
                    for lines_duplicates in list_lines_duplicates:
                        #df[df['column'].str.lower().isin([x.lower() for x in mylist])]
                        filtros.append( ~self.dados[lines_duplicates].isin( _pd[lines_duplicates] ) )

                        #filtros.append( ~self.dados[lines_duplicates].str.lower().isin(_pd[lines_duplicates].str.upper() ) )

                    tamanho = len(filtros)

                    if tamanho > 7:
                        raise Exception(f"Erro, não foi implementado para mais de 7 colunas")

                    if tamanho == 1:
                        self.dados = self.dados[ filtros[0] ]
                    elif tamanho == 2:
                        self.dados = self.dados[ filtros[0] & filtros[1] ]
                    elif tamanho == 3:
                        self.dados = self.dados[ filtros[0] & filtros[1] & filtros[2] ]
                    elif tamanho == 4:
                        self.dados = self.dados[ filtros[0] & filtros[1] & filtros[2] & filtros[3] ]
                    elif tamanho == 5:
                        self.dados = self.dados[ filtros[0] & filtros[1] & filtros[2] & filtros[3] & filtros[4]]
                    elif tamanho == 6:
                        self.dados = self.dados[ filtros[0] & filtros[1] & filtros[2] & filtros[3] & filtros[4] &  filtros[5] ]
                    elif tamanho == 7:
                        self.dados = self.dados[ filtros[0] & filtros[1] & filtros[2] & filtros[3] & filtros[4] & filtros[5] & filtros[6] ] 
           

        except Exception as error:
            raise Exception(f"Erro ao deletar campos duplicados {error}")


    def __delete_columns(self, list_columns_delete):
    
        try:
            if(list_columns_delete != None):
                logging.info(f"Iniciando o processo de deleção das colunas")
                self.dados.drop(columns=list_columns_delete, inplace=True, axis=1)
                #for column in list_columns_delete:
                #    if column in list(self.dados.columns):
                #        print(f"Coluna a ser deletada {column}")
                #        self.dados.drop(column, inplace=True, axis=1)
                #        print(f"Coluna {column} deletada")

        except Exception as error:
            raise Exception(f"Erro ao deletar coluna {error}")


    def __reorganize_field(self,list_field_reorganize):

        try:
            if( list_field_reorganize != None ):
                logging.info(f"Iniciando processo de reorganização de colunas")
                self.dados = self.dados[list_field_reorganize]
                logging.info(f"Colunas reorganizadas para {list_field_reorganize}")

        except Exception as error:
            raise Exception(f"Erro ao reorganizar campos {error}")


    #list_column_formt_date = ('Data de Criação Op','%d/%m/%Y')
    def __format_date(self,list_column_formt_date):

        try:
            if( list_column_formt_date != None):
                logging.info(f"Iniciando o processo de formatação das datas")
                for column_formt_date in list_column_formt_date:
                    logging.info(f"Coluna da data {column_formt_date[1]}")
                    try:
                        self.dados[ column_formt_date[0] ] = self.dados[ column_formt_date[1] ]\
                            .astype('datetime64[ns]').dt.strftime(column_formt_date[2])
                    except Exception as e:
                        logging.info(f"Erro no processo de conversão de data {e}")
                        self.dados[ column_formt_date[0] ] = np.NaN
        except Exception as error:
            raise Exception(f"Erro ao formatar data {error}")



    #list_analytics = [('teste','"joao" if( x["TIPO"].upper() == "MATRIZ" ) else None')]
    def __create_columns_analytics_apply(self,list_analytics):
        
        try:
            if(list_analytics != None and len(self.dados) > 0):
                logging.info(f"Iniciando o processo de aplicação de analise na coluna")
                for analytic in list_analytics:
                    logging.info(f"Coluna a ser analisada {analytic[0]}")
                    self.dados[analytic[0]] =  self.dados.apply(
                        lambda x: eval(compile(analytic[1], '<string>', 'eval')) ,axis=1)
        except Exception as error:
            raise Exception(f"Erro ao criar coluna analitica {error}")



    def __save_enrichment(self):
 
        try:
            file_name = Util.get_name_file(self.path_file)
            path_enrichment = Util.get_path_file_silver(self.path_file, 'enrichment', is_date=False)

            path_out_file_enrichment = os.path.join(path_enrichment, file_name)

            self.ioContainerData.upload_frame_to_blob( 
                self.ioContainerData.name_container_silver, 
                path_out_file_enrichment, 
                self.dados)

            logging.info(f'Arquivo enriquecido salvo em {path_out_file_enrichment}')
            
        except Exception as error:
            raise Exception(f"Erro ao salvar dados enriquecido {error}")


    def __insert_data_base(self, name_table, if_exists, is_first_processing):
        
        if(is_first_processing == False):
            if_exists = 'append'

        try:
            self.conexaoBanco.insert(self.dados, name_table, if_exists,chunksize=1000)
        except Exception as error:
            raise Exception(f"Erro ao salvar no banco de dados {name_table} erro {error}")


    def __close_base(self):

        try:
             self.conexaoBanco.close_connection()
        except Exception as error:
            logging.error(f"Erro ao fechar conexão com o banco {error}")

    def __get_field(self,  field_columns) -> pd.DataFrame:
       
        try:
            if(field_columns == None or len(field_columns) >= len(self.dados_original.columns)):
                return self.dados_original
            else:
                if type(field_columns) is list :
                    logging.info(f"Iniciando o processo de recuperação das colunas")
                    return self.dados_original.loc[:,field_columns]
                else:
                    raise Exception(f"Erro atributo fileds deve ser um list")
        except Exception as error2:
            raise Exception(f"Erro ao recuperar os campos {error2}")



    def __enrichment_sql(self,  list_parametros_enrichment_sql):

        try:
            if(list_parametros_enrichment_sql != None and len(list_parametros_enrichment_sql) > 0):
                logging.info(f"Iniciando de enriquecimento por sql")
                for parametros in list_parametros_enrichment_sql:

                    if(parametros.left_query != None):

                        _pd = self.conexaoBanco.select(parametros.left_query)

                        self.dados = pd.merge(_pd, 
                                        self.dados,
                                        how=parametros.how,
                                                 left_on=parametros.left_on,
                                        right_on=parametros.right_on
                                    )
                        
                    elif(parametros.right_query != None):
                
                        _pd = self.conexaoBanco.select(parametros.right_query)

                        self.dados = pd.merge( self.dados,
                                        _pd,
                                        how=parametros.how,
                                        left_on=parametros.left_on,
                                        right_on=parametros.right_on
                                    )
        
        except Exception as error:
            raise Exception(f"Erro no enriquecimento por sql{error}")


    def __rename_field(self, list_columns_rename):

        try:
            if(list_columns_rename != None):
                logging.info(f"Iniciando processo de renomeação de colunas")
                self.dados.rename(columns=list_columns_rename, inplace=True)
        except Exception as error:
            raise Exception(f"Erro ao renomear os campos {error}")



            
    def start(self, myDict)->str:

        msg = ""
        sucesso = True
        
        try:
            self.run(myDict)
            logging.info(f"Processamento finalizado com sucesso arquivo {self.path_file}")
            msg = msg + f"\nProcessamento finalizado com sucesso arquivo {self.path_file}. "
            sucesso = True
        except Exception as e:
            logging.error(f"Falha no processo {e}")
            msg = msg +  f"\nFalha no processo {e}. "
            sucesso = False
            self.fail()
        finally:
            self.__close_base()
            logging.info("Fim do processo")
            msg = msg + "\nFim do processo. "

        return sucesso, msg


    