import os
import shutil
import mimetypes
import logging
import urllib.parse
import hashlib
import argparse
from itertools import islice

import imghdr
try:
    import magic
    has_magic_lib = True
except ImportError as e:
    has_magic_lib = False

from PIL import Image
import requests
from requests import ConnectionError
from requests import TooManyRedirects
from requests import Timeout
from requests import HTTPError
from requests import RequestException

import concurrent.futures

MY_USER_AGENT_STRING="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/47.0.2526.106 Chrome/47.0.2526.106 Safari/537.36"

session = None

def setup_session(max_retries=1):
    global session
    session = requests.Session()

    session.mount("http://", requests.adapters.HTTPAdapter(max_retries=max_retries))
    session.mount("https://", requests.adapters.HTTPAdapter(max_retries=max_retries))


def create_logger(logfilename):
    logger = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(logfilename)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s\n%(message)s", "%Y-%m-%d %H:%M:%S")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(console)


def hashfile(afile, hasher=None, blocksize=65536):

    if not hasher:
        hasher = hashlib.sha256()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.hexdigest()


def hashbinary(raw_bytes, hasher=None):

    if not hasher:
        hasher = hashlib.sha256()
    hasher.update(raw_bytes)
    return hasher.hexdigest()


def get_referer(url):
    parsed_uri = urllib.parse.urlparse(url)
    netloc = parsed_uri.netloc
    scheme = parsed_uri.scheme
    if netloc.startswith("fansshare"): 
        netloc = "www." + netloc

    domain = '{}://{}'.format(scheme, netloc)
    return domain


def generate_headers(url):
    user_agent = MY_USER_AGENT_STRING
    referer = get_referer(url)
    headers = {"Referer":referer, "User-agent":user_agent}
    return headers


def download_image(counter, url, sha256, timeout):

    logger = logging.getLogger("logger")
    try:
        headers = generate_headers(url)
        response = session.get(url, headers=headers, timeout=timeout)
        if response.status_code != requests.codes.OK:  
            response.raise_for_status()
        if has_magic_lib:
            content_type = magic.from_buffer(response.content, mime=True)
        else:
            content_type = response.headers["content-type"] 

        if (content_type is None) or not content_type.startswith("image"):
            logger.error("Line {number}: Invalid content-type {content_type}: {url}".format(number=counter,
                                                                                            content_type=content_type,
                                                                                            url=url))
            return None

        if hashbinary(response.content) != sha256:
            logger.error("Line {number}: SHA 256 hash different: {url}".format(number=counter, url=url))
            return None

        return response

    except KeyError as e:
        logger.error("Line {number}: {error}: {url}".format(number=counter, error=e, url=url))
        return None
    except ConnectionError as e:
        logger.error("Line {number}: {error}: {url}".format(number=counter, error=e, url=url))
        return None
    except HTTPError as e:
        logger.error("Line {number}: {error}: {url}".format(number=counter, error=e, url=url))
        return None
    except Timeout as e:
        logger.error("Line {number}: {error}: {url}".format(number=counter, error=e, url=url))
        return None
    except TooManyRedirects as e:
        logger.error("Line {number}: {error}: {url}".format(number=counter, error=e, url=url))
        return None
    except RequestException as e:
        logger.error("Line {number}: {error}: {url}".format(number=counter, error=e, url=url))
        return None
    except Exception as e:
        logger.error("Line {number}: {error}: {url}".format(number=counter, error=e, url=url))
        return None


def parse_line(line):
    parts = line.rstrip().split('\t') 

    name = parts[0]
    image_id = int(parts[1])
    face_id = int(parts[2])
    url = parts[3]
    bbox = list(map(int, parts[4].split(',')))
    sha256 = parts[5]

    return name, image_id, face_id, url, bbox, sha256


def ensure_dir_exists(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)


def save_image(counter, url, response, datasetpath, name, image_id, face_id, bbox, save_face=False):
    logger = logging.getLogger("logger")

    output_dir = os.path.join(datasetpath, "images", name)
    ensure_dir_exists(output_dir)

    filename = "{name}_{image_id}".format(name=name,
                                          image_id=image_id)
    outpath = os.path.join(output_dir, filename)

    with open(outpath, 'wb') as outfile:
        outfile.write(response.content)
    
    filetype = imghdr.what(outpath)

    if filetype is None and not has_magic_lib:
        os.remove(outpath)
        logger.error("Line {number}: Cannot determine file type: {url}".format(number=counter, url=url))
        return False

    elif filetype is None and has_magic_lib:
        mimetype = magic.from_buffer(response.content, mime=True)
        if mimetype is None:
            logger.error("Line {number}: Cannot determine file type: {url}".format(number=counter, url=url))
            return False

        ext = mimetypes.guess_extension(mimetype).lstrip('.')
        if ext is None:
            logger.error("Line {number}: Cannot determine file type: {url}".format(number=counter, url=url))
            return False
        elif ext == "jpe":
            filetype = "jpeg"

    newpath = "{}.{}".format(outpath, filetype)
    shutil.move(outpath, newpath)

    if save_face:
        try:
            I = Image.open(newpath)
            output_dir = os.path.join(datasetpath, "faces", name)
            ensure_dir_exists(output_dir)
            filename = "{name}_{image_id}_{face_id}.{ext}".format(name=name,
                                                                  image_id=image_id,
                                                                  face_id=face_id,
                                                                  ext=filetype)
            I.crop(bbox).save(os.path.join(output_dir, filename))
        except IOError as e:
            logger.error("Line {number}: {error}: {url}".format(number=counter, error=e, url=url))
            return False

    return True


def main():
    parser = argparse.ArgumentParser(description="Script to download FaceScrub dataset")
    parser.add_argument("inputfile", help="FaceScrub data file. E.g., actors_users_normal_bbox.txt", type=str)
    parser.add_argument("datasetpath", help="Directory to save images", type=str)
    parser.add_argument("--crop_face", help="Whether to crop and save face images", dest="crop_face", action="store_true", default=False)
    parser.add_argument('-t', '--timeout', type=float, help="Number of seconds (float) to wait before requests timeout", action="store", required=False, dest="timeout", default=10)
    parser.add_argument('-r', '--max_retries', type=int, help="Maximum number of retries before giving up", action="store", required=False, dest="max_retries", default=1)
    parser.add_argument('-l', '--logfile', type=str, help="File to log operations", action="store", required=False, dest="logfile", default="download.log")
    parser.add_argument('-s', '--start_at_line', type=int, help="Line number in FaceScrub data file to start download. Note: Header counts as 1 line",
                        action="store", required=False, dest="start_at_line", default=2)
    parser.add_argument('-e', '--end_at_line', type=int, help="Last line number in FaceScrub data file to download. Note: Header counts as 1 line",
                        action="store", required=False, dest="end_at_line", default=0)
    parser.add_argument('-n', '--number_of_thread', type=int, help="Number of threads run in thread poll when fetching data",
                        action="store", required=False, dest="number_of_thread", default=10)
    args = parser.parse_args()

    assert args.timeout > 0, "timeout must be > 0"
    assert args.max_retries >= 1, "max_retries must be >= 1"
    assert args.start_at_line >= 1, "start_at_line must be >= 1"
    assert args.end_at_line >= 0, "end_at_line must be >= 0"
    assert args.number_of_thread >= 1, "number_of_thread must be >= 1"

    end_at_line = None                 
    if args.end_at_line > 0:
        end_at_line = args.end_at_line + 1

    start_at_line = args.start_at_line - 1 

    create_logger(args.logfile)
    logger = logging.getLogger("logger")
    setup_session(args.max_retries)

    print("")
    print('=' * 30)
    print("Start processing from line: {}".format(args.start_at_line))
    if end_at_line is None:
        print("Processing till end of file")
    else:
        print("End processing at line: {}".format(args.end_at_line))
    print('=' * 30)
    print("")

    infile = None
    try:
        infile = open(args.inputfile, encoding='utf-8')
    except Exception as e:
        logger.error("{}".format(e))
        return

    def _f(counter, line, args):
        name, image_id, face_id, url, bbox, sha256 = parse_line(line)
        logger.info("Processing line {}: {}".format(counter, url))
        response = download_image(counter, url, sha256, args.timeout)
        if response:
            save_image(counter, url, response, args.datasetpath, name.replace(' ', '_'), image_id, face_id, bbox, save_face=args.crop_face)

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.number_of_thread) as executor:
        futures = []
        for counter, line in enumerate(islice(infile,start_at_line,end_at_line), start_at_line+1):
            future = executor.submit(_f, counter, line, args)
            futures.append(future)

if __name__ == "__main__":
    main()
