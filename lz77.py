"""
LZ77 - Lossless Compression Algorithm
Implementation for academic demonstration
"""

import time
import json
from typing import List, Tuple


def find_longest_match(window: str, lookahead: str, max_offset: int, max_length: int) -> Tuple[int, int, str]:
    best_offset = 0
    best_length = 0
    best_char = lookahead[0] if lookahead else ''

    window_len = len(window)
    lookahead_len = len(lookahead)

    for offset in range(1, min(window_len, max_offset) + 1):
        start = window_len - offset
        length = 0
        while length < min(lookahead_len - 1, max_length) and \
              window[(start + length) % window_len] == lookahead[length] if offset <= window_len else \
              window[start + length % offset] == lookahead[length]:
            length += 1

        # Simpler and more reliable match finding
        match_len = 0
        pos = window_len - offset
        while match_len < lookahead_len - 1 and match_len < max_length:
            window_pos = pos + match_len
            if window_pos >= window_len:
                break
            if window[window_pos] == lookahead[match_len]:
                match_len += 1
            else:
                break

        if match_len > best_length:
            best_length = match_len
            best_offset = offset
            if best_length < lookahead_len:
                best_char = lookahead[best_length]

    return best_offset, best_length, best_char


def compress(text: str, window_size: int = 255, lookahead_size: int = 15) -> Tuple[List[Tuple], dict]:
    start_time = time.time()

    if not text:
        return [], {}

    tokens = []
    pos = 0
    n = len(text)

    while pos < n:
        window_start = max(0, pos - window_size)
        window = text[window_start:pos]
        lookahead = text[pos:pos + lookahead_size]

        if not lookahead:
            break

        offset, length, next_char = 0, 0, lookahead[0]

        for off in range(1, len(window) + 1):
            match_len = 0
            win_pos = len(window) - off
            while (match_len < len(lookahead) - 1 and
                   match_len < lookahead_size - 1 and
                   win_pos + match_len < len(window) and
                   window[win_pos + match_len] == lookahead[match_len]):
                match_len += 1

            if match_len > length:
                length = match_len
                offset = off
                if pos + length < n:
                    next_char = text[pos + length]
                else:
                    next_char = ''

        tokens.append((offset, length, next_char))

        if length > 0 and next_char:
            pos += length + 1
        elif length > 0 and not next_char:
            pos += length
        else:
            pos += 1

    elapsed = time.time() - start_time

    # Serialize tokens to bytes (simple encoding)
    serialized = json.dumps(tokens).encode('utf-8')

    original_size = len(text.encode('utf-8'))
    compressed_size = len(serialized)

    stats = {
        "original_size": original_size,
        "compressed_size": compressed_size,
        "compression_ratio": original_size / compressed_size if compressed_size > 0 else 0,
        "space_saving": (1 - compressed_size / original_size) * 100 if original_size > 0 else 0,
        "time_elapsed": elapsed,
        "token_count": len(tokens),
        "window_size": window_size,
        "lookahead_size": lookahead_size,
        "literal_tokens": sum(1 for t in tokens if t[1] == 0),
        "reference_tokens": sum(1 for t in tokens if t[1] > 0)
    }

    return tokens, serialized, stats


def decompress(tokens: List[Tuple], original_length: int = None) -> Tuple[str, dict]:
    start_time = time.time()

    result = []

    for offset, length, next_char in tokens:
        if length > 0 and offset > 0:
            start = len(result) - offset
            for i in range(length):
                if start + i < len(result):
                    result.append(result[start + i])
        if next_char:
            result.append(next_char)

    text = ''.join(result)

    elapsed = time.time() - start_time

    stats = {
        "time_elapsed": elapsed,
        "recovered_length": len(text),
        "tokens_processed": len(tokens)
    }

    return text, stats


def decompress_from_bytes(serialized: bytes, original_length: int = None) -> Tuple[str, dict]:
    tokens = json.loads(serialized.decode('utf-8'))
    # Convert lists back to tuples
    tokens = [(t[0], t[1], t[2]) for t in tokens]
    return decompress(tokens, original_length)
