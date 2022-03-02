import json
import os.path
import sys

import responder

import search

def main(config):
    api=responder.API(secret_key=config['secret_key'], templates_dir=config['templates'], static_dir=config['static'])
    retriever=search.Search(data_path=config['data'], config_path=config['threshold'], sentences_path=config['sentences'])

    @api.route('/')
    def top(request, response):
        response.html=api.template('index.html')

    @api.route('/s')
    async def retrieval(request, response):
        data=await request.media()
        q=data['q']
        discipline=data['discipline']
        if discipline in config['discipline']:
            results=retriever.search(config['discipline'][discipline], q)[2]
        else:
            results=[]
        response.media={'results': results}
    return api

def get_config(config_file):
    with open(config_file) as f:
        config=json.load(f)
    return config

if __name__=='__main__':
    config=get_config(sys.argv[1])
    api=main(config)
    api.run(address=config['address'], port=config['port'])
else:
    config=get_config(os.environ['FECONFIG'])
    api=main(config)
