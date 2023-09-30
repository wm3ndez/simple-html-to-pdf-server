Simple HTML to PDF server
=========================

How to use
----------

Build and run the docker image
```bash
$ docker build -t html_to_pdf_server .
$ docker run -p 5000:5000 html_to_pdf_server
```

Send the HTML as text:

```bash
$ curl -o mypdf.pdf -X POST -d "<h1>Hello</h1>" http://localhost:5000/pdf
```