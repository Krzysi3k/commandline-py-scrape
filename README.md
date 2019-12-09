# commandline-py-scrape

webscrape justjoin.it from commandline like a pro
following packages needs to be installed in order to webscrape and render javascript pages:

* beautifulsoup4: 4.7.1 or newer
* requests-html: 0.10.0 or newer

comandline parameters:
```--skill``` technologia np: Java, Devops, Python, etc...

```--min``` minimalna stawka wynagrodzenia [0 - 99999]

```--max``` maksymalna stawka wynagrodzenia [0 - 99999]

```--filtered``` tylko filtrowane oferty od: --min do: --max

```PS D:\>python cmd-scrape.py --skill java --min 6000 --max 12000```

