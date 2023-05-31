# LeitorPDFLAN
A python script to automate the reading of a directory with pdfs of LAN cable tests, avoiding CTRL-C+CTRL-V. It can easily be changed to work on other files.

## Installing the Libraries

```
pip install requirements.txt
```

## Running the script

```
python LeitorLAN
```

## Adjusting for your application

One can easily apply this code by changing functions.py
You basically have to change the CONTENT_KEYS, TITLES, INDEX variables, that depend upon your pdf file.
Also, it is important to change the regex variable pattern, to lookup your content through the pages.
saveLANParam() and readsPdfsFolder() were thought for this use case and have to be changed as well.

### Next steps
- [ ] Generalize the code to other applications

