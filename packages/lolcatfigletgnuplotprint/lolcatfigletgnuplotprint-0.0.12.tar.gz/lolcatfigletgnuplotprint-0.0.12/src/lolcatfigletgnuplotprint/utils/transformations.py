from typing import List


def chunk_list(list: List, chunk_size: int) -> List:
    """
    Chunks list into groups of chunk size
    """
    chunked_list = []
    for i in range(0, len(list), chunk_size):
        chunked_list.append(list[i : i + chunk_size])
    return chunked_list
