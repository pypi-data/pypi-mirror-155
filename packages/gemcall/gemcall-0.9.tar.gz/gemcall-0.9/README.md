# gemcall

Python module/CLI program for making network requests with the gemini protocol.

## Command line usage

```
usage: gemcall [-h] [-c CLIENTCERT] [-k CLIENTKEY] [-u URL] [-o OUTPUTFILE]
               [-t TIMEOUT] [-q] [-n] [-s]

Python module/CLI program for making network requests with the gemini
protocol.

optional arguments:
  -h, --help            show this help message and exit
  -c CLIENTCERT, --clientcert CLIENTCERT
                        Path to client certificate. This is optional, but must
                        be used when -k/--clientkey is used.
  -k CLIENTKEY, --clientkey CLIENTKEY
                        Path to the private key file for a client certificate.
                        This is optional, but must be used when
                        -c/--clientcert is used.
  -u URL, --url URL     Fully qualified URL to fetch.
  -o OUTPUTFILE, --outputfile OUTPUTFILE
                        File to output response body to.
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout of connection attempt, in seconds. Default is
                        3.
  -q, --quiet           Don't print response header.
  -n, --nobody          Only print response header.
  -s, --stdoutonly      Print everything to stdout
```

## Installation

[![Packaging status](https://repology.org/badge/vertical-allrepos/python:gemcall.svg)](https://repology.org/project/python:gemcall/versions)

```
pip install git+https://notabug.org/tinyrabbit/gemcall.git#egg=gemcall
# unofficial package is uploaded on PyPI for convenience
pip install gemcall
```

## Library Usage

```
import gemcall

response = gemcall.request(url)

# OR

response = gemcall.request(url, clientcert, clientkey)

while True:
    buf = response.read()
    if len(buf) > 0:
        sys.stdout.buffer.write(buf)
    else:
        break

response.discard()
```

The gemcall.Response object has the following values:
* serverpubkey: the public key part of the server certificate (the ONLY relevant part in TOFU certificate validation).
* responsecode: the response code from the server.
* meta: the rest of the header.

The method read() should be used to get content from the response object. It takes an argument 'bufsize', which is how many bytes it will read at most. This defaults to 4096.

When you are done reading the response you should use the discard() method to close all file handles and sockets the Response object is handling.

## CLI Usage

```
gemcall [OPTIONS]
```

## Features
* Supports client certificates.
* Supports streaming.

## Todo
* Error checking >.<
* Validation of response code and meta.

