import requests
import argparse


def download(fn, platform):
    url = 'https://github.com/hainm/ambertools-dev-binary/blob/master/{chunk}?raw=true'

    exts = 'abc' if platform == 'osx' else 'abcd'
    prefix = 'tmp_{}-64_ATa'.format(platform)
    with open(fn, 'wb') as fh:
        for ext in exts:
            final_url = url.format(chunk=prefix + ext)
            print("Processing %s " % final_url)
            x = requests.get(final_url)
            if x.ok:
                fh.write(x.content)
            else:
                print("Can not download %s" % final_url)
                return
    print("Done. Please check %s" % fn)


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--linux", action="store_true")
    parser.add_argument("--osx", action="store_true")
    opt = parser.parse_args(args)
    template = '{}-64.ambertools-18.dev.py27.tar'
    dev_dict = {'osx': template.format('osx'),
                'linux': template.format('linux')}
    if opt.linux:
        download(dev_dict['linux'], 'linux')
    if opt.osx:
        download(dev_dict['osx'], 'osx')


if __name__ == '__main__':
    main()
