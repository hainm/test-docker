import requests


def download(fn):
    url = 'https://github.com/hainm/ambertools-dev-binary/blob/master/{chunk}?raw=true'

    prefix = 'tmp_osx_ATa'
    with open(fn, 'wb') as fh:
        for ext in 'abc':
            final_url = url.format(chunk=prefix + ext)
            print("Processing %s " % final_url)
            x = requests.get(final_url)
            fh.write(x.content)
    print("Done. Please check %s" % fn)


def main():
    release_name = 'osx-64.ambertools-18.dev.py27.tar'
    download(release_name)


if __name__ == '__main__':
    main()
