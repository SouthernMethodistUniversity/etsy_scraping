from playwright.sync_api import sync_playwright
import sys, os, re, threading,tempfile,tarfile,hashlib,subprocess
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import concurrent.futures
from datetime import date

class Tls(threading.local):
    def __init__(self) -> None:
        self.playwright=sync_playwright().start()

class Worker:
    tls=Tls()

    def getItemContent(self,site):
        browser=self.tls.playwright.firefox.launch()
        page=browser.new_page()
        page.goto(site)
        title=str(page.title())
        content=page.content()
        page.close()
        browser.close()
        return content


if __name__ == "__main__":
    urlList=[]
    with open('/scratch/group/kbnk_group/projects/etsy_scraping/runs/lists/list{}.txt'.format(sys.argv[1]),'r') as textList:
        contents=textList.readlines()
        for line in contents:
            currentPlace=line[:-1]
            urlList.append(currentPlace)
    #urlList=urlList[0:50]

    today=date.today().strftime('%Y-%m-%d')

    bashCommand='mkdir /scratch/group/kbnk_group/projects/etsy_scraping/runs/{0}/'.format(today)
    if os.path.exists('/scratch/group/kbnk_group/projects/etsy_scraping/runs/{0}/'.format(today))==False:
        subprocess.run(bashCommand,shell=True)

    i=0
    # Etsy can handle 25 workers
    with ThreadPoolExecutor(max_workers=25) as executor:
        worker=Worker()
        future_to_url = {executor.submit(worker.getItemContent, site): site for site in urlList}
        for future in concurrent.futures.as_completed(future_to_url):
            site = future_to_url[future]
            hashed_site = hashlib.sha256(site.encode()).hexdigest()
            try:
                data = future.result()
                #print(site)
                with open("/scratch/group/kbnk_group/projects/etsy_scraping/runs/{0}/{1}.html".format(today,hashed_site),'w') as outFile:
                    outFile.write(data)
                with tarfile.open("/scratch/group/kbnk_group/projects/etsy_scraping/runs/{0}/{1}.txz".format(today,hashed_site),'w:xz') as tarFile:
                    tarFile.add("/scratch/group/kbnk_group/projects/etsy_scraping/runs/{0}/{1}.html".format(today,hashed_site),arcname=str(hashed_site)+'.html')
                subprocess.run('rm /scratch/group/kbnk_group/projects/etsy_scraping/runs/{0}/{1}.html'.format(today,hashed_site),shell=True)
                i+=1
            except Exception as exc:
                print('%r generated an exception: %s' %(site,exc))
    print(i,"/",len(urlList))
