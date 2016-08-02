# Simple mail send

Simple smtp sending tool (smtp_send) with file and directory sending.

## Installing

Execute:

```cd /tmp
git clone https://github.com/0dayexploit/smtp_send
```
You can use virtualenv and install project into python virtual environment:

```virtualenv --system-site-packages --python=python3 venv
source venv/bin/activate
```
For installing execute:

```python setup.py install
```

## Usage

smtp_send use smtp.mail.ru default server and port = 587

```smtp_send login@mail.ru password
```

If you want to attach file or directory (without subdirectories)
set -a parameter:

```smtp_send login@mail.ru password -a directory
```

To change server/port use -s/-p parameters:

```smtp_send login@gmail.com password -s smtp.gmail.com
```
