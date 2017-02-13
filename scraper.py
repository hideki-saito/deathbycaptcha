# -*- coding: utf-8 -*-

import os

# import xlsxwriter
from bs4 import BeautifulSoup
import requests
import deathbycaptcha

dbc_id = "igormsg"
dbc_pd = "avemaria123"

#url = "http://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjreva_solicitacao2.asp"
url = "http://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjreva_solicitacao2.asp"
#inputFile_path = raw_input("Input the file path that contatin ids: ")
inputFile_path = "id.txt"
# captcha_file_name = "captcha.png"
captcha_file_name = "Captcha-6.gif"
s = requests.session()
r = requests.Response

def getId():
    id_list = [line.rstrip('\n') for line in open(inputFile_path)]
    return id_list

def file_download(url):
    with open(captcha_file_name, 'wb') as handle:
        response = s.get(url)
        if not response.ok:
            print "error"

        for block in response.iter_content(1024):
            handle.write(block)
        handle.close()

def get_char_from_captcha():
    # r = s.get(url)
    # soup = BeautifulSoup(r.content, 'html.parser')
    # captcha_url = "http://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva" + soup.find(name='img', attrs={'id':'imgCaptcha'}).get('src')[1:]
    # print captcha_url
    #
    # file_download(captcha_url)

    client = deathbycaptcha.SocketClient(dbc_id, dbc_pd)
    captcha = client.decode(captcha_file_name, 60)

    #os.remove(captcha_file_name)
    return captcha["text"]

def output():

    pass


def main():
    workbook = xlsxwriter.Workbook("report.xls")
    worksheet = workbook.add_worksheet()
    field = [u"Id number", u"NÚMERO DE INSCRIÇÃO", u"DATA DE ABERTURA", u"NOME EMPRESARIAL", u"TÍTULO DO ESTABELECIMENTO (NOME DE FANTASIA)", u"CÓDIGO E DESCRIÇÃO DA ATIVIDADE ECONÔMICA PRINCIPAL", u"CÓDIGO E DESCRIÇÃO DAS ATIVIDADES ECONÔMICAS SECUNDÁRIAS", u"CÓDIGO E DESCRIÇÃO DA NATUREZA JURÍDICA", u"LOGRADOURO", u"NÚMERO", u"COMPLEMENTO", u"CEP ", u"BAIRRO/DISTRITO", u"MUNICÍPIO", u"UF", u"ENDEREÇO ELETRÔNICO", u"TELEFONE",u"ENTE FEDERATIVO RESPONSÁVEL (EFR)", u"SITUAÇÃO CADASTRAL", u"DATA DA SITUAÇÃO CADASTRAL", u"MOTIVO DE SITUAÇÃO CADASTRAL", u"SITUAÇÃO ESPECIAL", u"DATA DA SITUAÇÃO ESPECIAL"]
    for i in range(0, len(field)):
            worksheet.write(0, i, field[i])

    row = 1

    id_list = getId()
    print id_list

    for id in id_list:
        while 1:
            try:
                char = get_char_from_captcha()
                print char

                payload = {"txtTexto_captcha_serpro_gov_br":char,
                        "submit1":"Consultar",
                        "search_type":"cnpj",
                        "origem":"comprovante",
                        "cnpj":id
                }
                r = s.get("http://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/valida.asp", data=payload)
                if r.url == "http://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/Cnpjreva_Comprovante.asp":
                    break

            except Exception:
                pass

        print r.content

        soup = BeautifulSoup(r.content, 'html.parser')


        values = [id]
        column2 = soup.find('font', text="NÚMERO DE INSCRIÇÃO")

        for i in range(0, len(values)):
            worksheet.write(row, i, values[i])

        row = row + 1
    workbook.close()

        # s.get("http://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/Cnpjreva_Vstatus.asp?origem=comprovante&cnpj=" + id)
        #r = s.get("http://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/Cnpjreva_Comprovante.asp")



if __name__ == "__main__":
    # main()
    text = get_char_from_captcha()
    print text