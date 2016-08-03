# Simple mail send

Simple smtp sending tool (smtp_send) with file and directory sending.

## Installing

Execute:

```sh
cd /tmp
git clone https://github.com/0dayexploit/smtp_send
```

You can use virtualenv and install project into python virtual environment:

```sh
virtualenv --system-site-packages --python=python3 venv
source venv/bin/activate
```

For installing execute:

```sh
python setup.py install
```

## Usage

smtp_send use smtp.mail.ru default server and port = 587

```sh
smtp_send login@mail.ru password
```

If you want to attach file or directory (without subdirectories)
set -a parameter:

```sh
smtp_send login@mail.ru password -a directory
```

To change server/port use -s/-p parameters:

```sh
smtp_send login@gmail.com password -s smtp.gmail.com
```

If you want to set Subject and Message fields use -S and -M parameters:

```sh
smtp_send login@mail.ru password -S Test -M \"Hello world\"
```
