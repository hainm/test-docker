import requests


def download():
    url = 'https://github.com/hainm/ambertools-dev-binary/blob/master/{chunk}?raw=true'

    prefix = 'tmp_osx_ATa'
    with open('AT.tar', 'wb') as fh:
        for ext in 'abc':
            final_url = url.format(chunk=prefix + ext)
            print("Processing %s " % final_url)
            x = requests.get(final_url)
            fh.write(x.content)


def main():
    download()


if __name__ == '__main__':
    main()
