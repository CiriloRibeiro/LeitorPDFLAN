# LeitorPDFLAN
A Python script is provided below to automate the process of reading a directory containing PDFs of LAN cable tests, eliminating the need for manual copy-pasting (CTRL-C+CTRL-V). The script can be easily modified to work with other types of files.

## Installing the Libraries

```
pip install requirements.txt
```

## Running the script

```
python LeitorLAN
```

## To adapt the code for your specific application, follow these steps:

Open the file functions.py and make the necessary changes.
Update the values of the following variables: CONTENT_KEYS, TITLES, and INDEX. These variables depend on the structure and content of your PDF file.
Modify the regex variable pattern to match the specific pattern you need for extracting content from the pages.
If required, make appropriate changes to the functions saveLANParam() and readsPdfsFolder() to suit your use case.
By following these steps, you can customize the script to meet your specific requirements and efficiently automate the reading process for your desired files.

### Next steps
- [ ] Generalize the code to other applications

