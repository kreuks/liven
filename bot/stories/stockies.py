import random, urllib2, json
import logging

from bot.stories.base import Story
from bot.constants import Context, Intent, RESPONSES, OOT
from bot.util import get_result_story

logging.basicConfig(level=logging.INFO)

class StockPrice(Story):
    def __init__(self):
        self.prefix = 'http://finance.google.com/finance/info?client=ig&q='

    def compliance(self, context):
        logging.info(
            'compliance Stock price method'
        )
        return (
            Intent.STOCK_FIND in context.values()
        )

    def find_stock_price(self,context):
        stock_name = context[Context.STOCK_NAME]
        url = self.prefix + '%s:%s'%(stock_name[0:4], 'IDX')
        logging.info(
            'link : \n{}'.format(url)
        )
        try:
            content = urllib2.urlopen(url).read()
        except IOError:
            logging.info(
                'Error Open Page : Google Finance'
            )
            return {}
        obj = json.loads(content[3:])
        logging.info(
            'stock_code : {} \nstock_pricing : {} \ndifference : {} \ntime : {}'.format(obj[0]['t'], obj[0]['l_fix'], obj[0]['cp'], obj[0]['lt'])
        )
        return {
            'stock_code' : obj[0]['t'],         #0
            'stock_pricing' : obj[0]['l_fix'],  #1
            'difference' : obj[0]['cp'],        #2
            'time' : obj[0]['lt']                 #3
        }

    def run(self, context):
        logging.info(
            'method Run Stock Price'
        )
        result = get_result_story()
        stock_data = self.find_stock_price(context)
        response = RESPONSES[Context.STOCK_NAME]
        response = response[random.randint(0, len(response)-1)]
        if len(stock_data) > 0:
            result['context'] = context
            result['response'] = response.format(
                stock_data['stock_code'], stock_data['stock_pricing'], stock_data['difference'], stock_data['time']
            )
        else:
            result['context'] = context
            result['response'] = 'Sorry, gw pusing ga nemu nyarinya'
        return result
