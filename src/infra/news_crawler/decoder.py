# Based on https://github.com/adbar/trafilatura/blob/master/trafilatura/utils.py
import logging

import chardet

logger = logging.getLogger(__name__)


def _isutf8(data):
    """Simple heuristic to determine if a bytestring uses standard unicode encoding"""
    try:
        data.decode('UTF-8')
    except UnicodeDecodeError:
        return False
    else:
        return True


def _detect_encoding(bytesobject):
    """Read the first chunk of input and return its encoding"""
    # unicode-test
    if _isutf8(bytesobject):
        return 'UTF-8'
    else:
        guess = chardet.detect(bytesobject)
        logger.debug('guessed encoding: %s', guess['encoding'])
        return guess['encoding']
    # fallback on full response
    # if guess is None or guess['encoding'] is None: # or guess['confidence'] < 0.99:
    #    guessed_encoding = chardet.detect(bytesobject)['encoding']
    # return
    return None


def decode_response(response):
    """Read the first chunk of server response and decode it"""
    guessed_encoding = _detect_encoding(response.content)
    logger.debug('response/guessed encoding: %s / %s', response.encoding, guessed_encoding)
    # process
    if guessed_encoding is not None:
        try:
            htmltext = response.content.decode(guessed_encoding)
        except UnicodeDecodeError:
            logger.warning('encoding error: %s / %s', response.encoding, guessed_encoding)
            htmltext = response.text
    else:
        htmltext = response.text
    return htmltext