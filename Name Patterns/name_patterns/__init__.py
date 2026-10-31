"""Suche nach regelmaessigen Namensmustern in Herrscherlisten.

Alle vier Stufen sind umgesetzt:

1. Kern -- Bloecke sammeln und zu Ketten verbinden (:mod:`.index`, :mod:`.search`)
2. Toleranz -- Budget fuer geringfuegige Abweichungen (:mod:`.search`)
3. Discovery -- Anchor und Echo automatisch finden (:mod:`.discovery`)
4. Signifikanz -- Seltenheit in Bit und Monte-Carlo-p-Wert (:mod:`.scoring`)
"""

from __future__ import annotations

from .data import load_name_metadata, load_names, name_file_sha256, normalize, strip_ordinal
from .discovery import Motif, candidate_motifs, discover
from .index import build_occurrences, find_blocks, find_bookend_blocks
from .model import (
    Block,
    Chain,
    Deviation,
    DeviationKind,
    PatternKind,
    Placement,
    SearchConfig,
)
from .scoring import (
    NullModel,
    ScoredChain,
    assess,
    bookend_bits,
    build_null_model,
    chain_bits,
    score_chains,
    simpson_index,
)
from .search import build_chains, find_bookend_chains, find_chains, find_chains_for_blocks

__all__ = [
    "Block",
    "Chain",
    "Deviation",
    "DeviationKind",
    "Motif",
    "NullModel",
    "PatternKind",
    "Placement",
    "ScoredChain",
    "SearchConfig",
    "assess",
    "bookend_bits",
    "build_chains",
    "build_null_model",
    "build_occurrences",
    "candidate_motifs",
    "chain_bits",
    "discover",
    "find_blocks",
    "find_bookend_blocks",
    "find_bookend_chains",
    "find_chains",
    "find_chains_for_blocks",
    "load_names",
    "load_name_metadata",
    "name_file_sha256",
    "normalize",
    "score_chains",
    "simpson_index",
    "strip_ordinal",
]
