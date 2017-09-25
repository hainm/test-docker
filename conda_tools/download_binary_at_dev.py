import requests


def download(fn):
    url = 'https://github.com/hainm/ambertools-dev-binary/blob/master/{chunk}?raw=true'

    prefix = 'tmp_osx-64_ATa'
    with open(fn, 'wb') as fh:
        for ext in 'abc':
            final_url = url.format(chunk=prefix + ext)
            print("Processing %s " % final_url)
            x = requests.get(final_url)
            if x.ok:
                fh.write(x.content)
            else:
                print("Can not download %s" % final_url)
                return
    print("Done. Please check %s" % fn)


def main():
    release_name = 'osx-64.ambertools-18.dev.py27.tar'
    download(release_name)


if __name__ == '__main__':
    main()
