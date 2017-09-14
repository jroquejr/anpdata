# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from operator import itemgetter
import scrapy
from scrapy import FormRequest
import re
from collections import OrderedDict


class AnpSpider(scrapy.Spider):
    name = 'anp'
    allowed_domains = [u'anp.gov.br']
    start_urls = [u'http://www.anp.gov.br/preco/prc/Resumo_10_Ultimas_Coletas_Index.asp']
    ULTIMAS_COLETAS = u'http://www.anp.gov.br/preco/prc/Relatorio_Excel_Ultimas_Coletas_Posto.asp'

    def parse(self, response):

        regex = re.compile(r'(value\=\")(?P<valor>\d+)(\"\>)(?P<texto>.*)(\<\/option\>)')
        options = response.css('#frmEntregues0 select[name=selPeriodoSemana] option').extract()[-3:]

        for option in options:
            periodo = regex.search(option, re.IGNORECASE).groupdict()
            yield self.process_coletas(periodo.get('valor'), periodo.get("texto"))

    def process_coletas(self, periodo, periodo_texto):

        combustiveis = {
            487: "Gasolina",
            643: "Etanol",
            476: "GNV",
            532: "Diesel",
            462: "GPL"
        }

        for combustivel in combustiveis.keys():
            request = FormRequest(
                url=self.ULTIMAS_COLETAS,
                dont_filter=True,
                method="post",
                callback=self.parse_report,
                formdata={
                    'COD_SEMANA': "954",
                    'COD_COMBUSTIVEL': "487",
                    "COD_MUNICIPIO": "988",
                    "DESC_MUNICIPIO": "SALVADOR",
                    "BAIRRO": "0",
                    "btnSalvar": "exportar"
                }
            )

            request.meta.update({
                'cidade_id': 988,
                'cidade_cod': 'SALVADOR',
                'combustivel_cod': combustivel,
                'combustivel_nome': combustiveis.get(combustivel),
                'periodo_id': periodo,
                'periodo_texto': periodo_texto
            })

            return request

    def parse_report(self, response):

        step = 9
        headers = ('razao_social', 'endereco', 'bairro', 'bandeira', 'preco_venda', 'preco_compra', 'modalidade', 'fornecedor_branca', 'data')

        table = response.css('table.table_padrao')[0]
        table_columns = table.css('td')

        if not (len(table_columns) % step == 0):
            print('Mal formação da tabela: {}'.format(len(table_columns)))

        columns_dados = [ column.css('::text').extract_first().strip() for column in table_columns ]

        for x in range(0, len(columns_dados), step):
            item = dict(zip(headers, columns_dados[x:x+step]))
            item.update({
                'cidade_id': response.meta.get('cidade_id'),
                'cidade_cod': response.meta.get('cidade_cod'),
                "combustivel_cod": response.meta.get('combustivel_cod'),
                'combustivel_nome': response.meta.get('combustivel_nome'),
                'periodo_id': response.meta.get('periodo_id'),
                'periodo_texto': response.meta.get('periodo_texto')
            })

            yield item
