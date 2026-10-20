import json, urllib.request, datetime, time, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
HEAD={'User-Agent':'MemeHunterAI/2.0 (personal scanner)','Accept':'application/json'}
def get(url):
    req=urllib.request.Request(url,headers=HEAD)
    with urllib.request.urlopen(req,timeout=22) as res:return json.load(res)
def num(v):
    try:return float(v or 0)
    except (ValueError,TypeError):return 0.
def main():
    addresses=[]; errors=[]
    for path in ('token-profiles/latest/v1','token-boosts/latest/v1','token-boosts/top/v1'):
        try:
            result=get('https://api.dexscreener.com/'+path)
            for item in result if isinstance(result,list) else []:
                if item.get('chainId')=='solana' and item.get('tokenAddress') and item['tokenAddress'] not in addresses:addresses.append(item['tokenAddress'])
        except Exception as ex:errors.append(path+': '+str(ex))
    coins={}
    for offset in range(0,min(len(addresses),240),30):
        chunk=addresses[offset:offset+30]
        try:
            result=get('https://api.dexscreener.com/tokens/v1/solana/'+','.join(chunk))
            for p in result if isinstance(result,list) else []:
                if p.get('chainId')!='solana':continue
                base=p.get('baseToken') or {}; addr=base.get('address')
                if not addr or addr not in addresses:continue
                created=p.get('pairCreatedAt'); age=(time.time()*1000-num(created))/3600000 if created else None
                if age is None or age<0 or age>24:continue
                liq=num((p.get('liquidity') or {}).get('usd')); vol=num((p.get('volume') or {}).get('h1')); tx=p.get('txns') or {}; h1=tx.get('h1') or {}; buys=num(h1.get('buys')); sells=num(h1.get('sells')); cap=num(p.get('marketCap') or p.get('fdv'))
                if liq<1000:continue
                score=round(min(liq/30000,1)*25+min(vol/50000,1)*25+min((buys+sells)/200,1)*20+min(buys/max(sells,1),2)/2*15+min(liq/max(cap,1)*10,1)*15)
                warnings=[]
                if liq<10000:warnings.append('Niedrige Liquidität')
                if cap and liq/cap<.03:warnings.append('Geringe Liquidität relativ zur Bewertung')
                if sells and buys/sells<.7:warnings.append('Mehr Verkäufe als Käufe')
                if not sells and buys:warnings.append('Keine Verkäufe im 1h-Fenster – prüfen')
                row={'address':addr,'name':base.get('name','Unbekannt'),'symbol':base.get('symbol','?'),'pairAddress':p.get('pairAddress',''),'dex':p.get('dexId',''),'ageHours':round(age,2),'liquidityUsd':round(liq),'volume1hUsd':round(vol),'marketCapUsd':round(cap),'buys1h':int(buys),'sells1h':int(sells),'change1h':num((p.get('priceChange') or {}).get('h1')),'score':score,'warnings':warnings,'url':p.get('url','')}
                if addr not in coins or liq>coins[addr]['liquidityUsd']:coins[addr]=row
        except Exception as ex:errors.append('pair batch: '+str(ex))
        time.sleep(.3)
    data={'updatedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':'DEX Screener public API; candidate discovery from recent profiles and boosts, not all new launches','coins':sorted(coins.values(),key=lambda c:c['score'],reverse=True)[:150],'errors':errors}
    if errors and not coins:raise RuntimeError('No usable data: '+'; '.join(errors))
    (ROOT/'data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Saved',len(data['coins']),'coins; warnings:',errors)
if __name__=='__main__':main()
