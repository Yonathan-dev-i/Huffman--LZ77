"""
Huffman Coding - Lossless Compression Algorithm
Implementation for academic demonstration
"""

import heapq
import json
import time
from collections import Counter
from dataclasses import dataclass, field
from typing import Optional, Dict, Tuple


@dataclass(order=True)
class HuffmanNode:
    freq: int
    char: Optional[str] = field(compare=False, default=None)
    left: Optional['HuffmanNode'] = field(compare=False, default=None)
    right: Optional['HuffmanNode'] = field(compare=False, default=None)


def build_frequency_table(text: str) -> Dict[str, int]:
    return dict(Counter(text))


def build_huffman_tree(freq_table: Dict[str, int]) -> HuffmanNode:
    heap = []
    for char, freq in freq_table.items():
        heapq.heappush(heap, HuffmanNode(freq=freq, char=char))

    if len(heap) == 1:
        node = heapq.heappop(heap)
        root = HuffmanNode(freq=node.freq, left=node, right=None)
        heapq.heappush(heap, root)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(
            freq=left.freq + right.freq,
            left=left,
            right=right
        )
        heapq.heappush(heap, merged)

    return heapq.heappop(heap)


def build_code_table(node: HuffmanNode, prefix: str = "", table: Dict = None) -> Dict[str, str]:
    if table is None:
        table = {}
    if node is None:
        return table
    if node.char is not None:
        table[node.char] = prefix if prefix else "0"
        return table
    build_code_table(node.left, prefix + "0", table)
    build_code_table(node.right, prefix + "1", table)
    return table


def encode_text(text: str, code_table: Dict[str, str]) -> str:
    return "".join(code_table[char] for char in text)


def bits_to_bytes(bit_string: str) -> bytes:
    padding = (8 - len(bit_string) % 8) % 8
    bit_string += "0" * padding
    result = bytearray()
    for i in range(0, len(bit_string), 8):
        result.append(int(bit_string[i:i+8], 2))
    return bytes([padding]) + bytes(result)


def bytes_to_bits(data: bytes) -> str:
    padding = data[0]
    bit_string = ""
    for byte in data[1:]:
        bit_string += format(byte, '08b')
    if padding:
        bit_string = bit_string[:-padding]
    return bit_string


def decode_text(bit_string: str, root: HuffmanNode) -> str:
    result = []
    node = root
    for bit in bit_string:
        if bit == "0":
            node = node.left
        else:
            node = node.right
        if node is None:
            break
        if node.char is not None:
            result.append(node.char)
            node = root
    return "".join(result)


def serialize_tree(node: HuffmanNode) -> dict:
    if node is None:
        return None
    return {
        "freq": node.freq,
        "char": node.char,
        "left": serialize_tree(node.left),
        "right": serialize_tree(node.right)
    }


def deserialize_tree(data: dict) -> Optional[HuffmanNode]:
    if data is None:
        return None
    node = HuffmanNode(
        freq=data["freq"],
        char=data["char"],
        left=deserialize_tree(data["left"]),
        right=deserialize_tree(data["right"])
    )
    return node


def compress(text: str) -> Tuple[bytes, dict]:
    start = time.time()

    freq_table = build_frequency_table(text)
    tree = build_huffman_tree(freq_table)
    code_table = build_code_table(tree)
    bit_string = encode_text(text, code_table)
    compressed_bytes = bits_to_bytes(bit_string)

    tree_data = serialize_tree(tree)
    metadata = {
        "tree": tree_data,
        "original_length": len(text),
        "freq_table": freq_table,
        "code_table": code_table
    }

    elapsed = time.time() - start

    original_size = len(text.encode('utf-8'))
    compressed_size = len(compressed_bytes) + len(json.dumps(metadata).encode('utf-8'))

    stats = {
        "original_size": original_size,
        "compressed_size": compressed_size,
        "compression_ratio": original_size / compressed_size if compressed_size > 0 else 0,
        "space_saving": (1 - compressed_size / original_size) * 100 if original_size > 0 else 0,
        "time_elapsed": elapsed,
        "freq_table": freq_table,
        "code_table": code_table,
        "bit_length": len(bit_string),
        "unique_chars": len(freq_table)
    }

    return compressed_bytes, metadata, stats


def decompress(compressed_bytes: bytes, metadata: dict) -> Tuple[str, dict]:
    start = time.time()

    tree = deserialize_tree(metadata["tree"])
    bit_string = bytes_to_bits(compressed_bytes)
    text = decode_text(bit_string, tree)

    elapsed = time.time() - start

    stats = {
        "time_elapsed": elapsed,
        "recovered_length": len(text),
        "original_length": metadata["original_length"]
    }

    return text, stats
