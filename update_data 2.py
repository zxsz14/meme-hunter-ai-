import json, datetime, urllib.request, urllib.parse, time
BASE='https://api.dexscreener.com'
def get(path):
    req=urllib.request.Request(BASE+path,headers={'User-Agent':'MemeHunterResearch/1.0','Accept':'application/json'})
    with urllib.request.urlopen(req,timeout=25) as r:return json.load(r)
def main():
    profiles=get('/token-profiles/latest/v1')
    addresses=list(dict.fromkeys(x['tokenAddress'] for x in profiles if x.get('chainId')=='solana' and x.get('tokenAddress')))[:30]
    pairs=[]
    if addresses:
        pairs=get('/tokens/v1/solana/'+','.join(urllib.parse.quote(a,safe='') for a in addresses))
    unique={p['pairAddress']:p for p in pairs if p.get('chainId')=='solana' and p.get('pairAddress')}
    result={'updatedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pairs':list(unique.values())[:200]}
    with open('data.json','w') as f:json.dump(result,f,ensure_ascii=False,separators=(',',':'))
    print('Updated',len(result['pairs']),'pairs')
if __name__=='__main__':main()
