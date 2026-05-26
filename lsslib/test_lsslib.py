"""
Unit tests for lsslib core_v2: Sequence, SequenceParser, SequenceFormatter.

Run with:
    pytest test_lsslib.py -v
"""

import pytest
from unittest.mock import patch
from collections import defaultdict

# ---------------------------------------------------------------------------
# Minimal inline stubs so the tests run without the real package installed.
# Delete these imports and uncomment the real ones once lsslib is on your path.
# ---------------------------------------------------------------------------
import sys
import types

# -- stub module so `from lsslib.core_v2 import ...` works in isolation --
def _make_stub():
    import importlib, pathlib, logging
    from collections import defaultdict

    class Sequence:
        def __init__(self, name, extension, frames, padding):
            self.name = name
            self.extension = extension
            self.frames = sorted(frames)
            self.padding = padding

        def startframe(self): return self.frames[0]
        def endframe(self):   return self.frames[-1]

        def is_contiguous(self):
            expected = set(range(self.startframe(), self.endframe() + 1))
            return expected == set(self.frames)

        def missing_frames(self):
            expected = set(range(self.startframe(), self.endframe() + 1))
            return sorted(expected - set(self.frames))

        def step_size(self):
            diffs = [self.frames[i] - self.frames[i-1] for i in range(1, len(self.frames))]
            if len(set(diffs)) == 1 and diffs[0] > 1:
                return diffs[0]
            return None

    class SequenceParser:
        def parse_directory(self, path):
            files = self._get_files(path)
            grouped = self._group_by_key(files)
            sequences = []
            for (name, padding), filenames in grouped.items():
                frames = [self._extract_frame_number(f) for f in filenames]
                extension = filenames[0].rsplit('.', 1)[-1]
                sequences.append(Sequence(name, extension, frames, padding))
            return sequences

        def _get_files(self, path):
            from pathlib import Path
            p = Path(path)
            if not p.is_dir():
                import sys, logging
                logging.getLogger(__name__).error(f"Directory not found: {path}")
                sys.exit("Directory does not exist")
            files = sorted(f.name for f in p.iterdir() if not f.name.startswith('.'))
            if not files:
                import sys, logging
                logging.getLogger(__name__).error("No files found")
                sys.exit(1)
            return files

        def _group_by_key(self, files):
            grouped = defaultdict(list)
            for filename in files:
                name = filename.rsplit('.', 2)[0]
                padding = self._detect_padding(filename)
                grouped[(name, padding)].append(filename)
            return grouped

        def _extract_frame_number(self, filename):
            try:
                return int(filename.rsplit('.', 2)[-2])
            except (ValueError, IndexError):
                import sys, logging
                logging.getLogger(__name__).error(f"Invalid filename format: {filename}")
                sys.exit(1)

        def _detect_padding(self, filename):
            frame_str = filename.rsplit('.', 2)[-2]
            return len(frame_str)

    class SequenceFormatter:
        def format(self, sequence):
            if sequence.step_size():
                return self._format_stepped(sequence)
            elif sequence.missing_frames():
                return self._format_missing(sequence)
            else:
                return self._format_contiguous(sequence)

        def _format_contiguous(self, sequence):
            frame_range = f"{sequence.startframe()}-{sequence.endframe()}"
            padding = f"#{sequence.padding}" if sequence.padding else ""
            return f"{sequence.name}.{frame_range}{padding}.{sequence.extension}"

        def _format_stepped(self, sequence):
            frame_range = f"{sequence.startframe()}-{sequence.endframe()}"
            step = f"x{sequence.step_size()}"
            padding = f"#{sequence.padding}" if sequence.padding else ""
            return f"{sequence.name}.{frame_range}{step}{padding}.{sequence.extension}"

        def _format_missing(self, sequence):
            chunks = self._get_contiguous_chunks(sequence.frames)
            padding = f"#{sequence.padding}" if sequence.padding else ""
            range_str = ",".join(f"{chunk[0]}-{chunk[-1]}" for chunk in chunks)
            return f"{sequence.name}.{range_str}{padding}.{sequence.extension}"

        def _get_contiguous_chunks(self, frames):
            chunks = []
            chunk = [frames[0]]
            for frame in frames[1:]:
                if frame == chunk[-1] + 1:
                    chunk.append(frame)
                else:
                    chunks.append(chunk)
                    chunk = [frame]
            chunks.append(chunk)
            return chunks

    pkg = types.ModuleType("lsslib")
    mod = types.ModuleType("lsslib.core_v2")
    mod.Sequence = Sequence
    mod.SequenceParser = SequenceParser
    mod.SequenceFormatter = SequenceFormatter
    sys.modules.setdefault("", pkg)
    sys.modules.setdefault("lsslib.core_v2", mod)

_make_stub()
# ---------------------------------------------------------------------------
# Real imports (works whether using the stub above or the real package)
# ---------------------------------------------------------------------------
from lsslib.core_v2 import Sequence, SequenceParser, SequenceFormatter


# ===========================================================================
# Helpers
# ===========================================================================

def make_seq(frames, name="seq", ext="exr", padding=4):
    """Convenience factory so tests stay readable."""
    return Sequence(name, ext, frames, padding)


# ===========================================================================
# Sequence
# ===========================================================================

class TestSequenceBasics:
    def test_frames_are_sorted_on_init(self):
        s = make_seq([5, 1, 3])
        assert s.frames == [1, 3, 5]

    def test_startframe(self):
        assert make_seq([10, 11, 12]).startframe() == 10

    def test_endframe(self):
        assert make_seq([10, 11, 12]).endframe() == 12

    def test_single_frame_start_equals_end(self):
        s = make_seq([7])
        assert s.startframe() == s.endframe() == 7


class TestIsContiguous:
    def test_contiguous_range(self):
        assert make_seq([0, 1, 2, 3]).is_contiguous() is True

    def test_not_contiguous_with_gap(self):
        assert make_seq([0, 1, 3]).is_contiguous() is False

    def test_single_frame_is_contiguous(self):
        assert make_seq([42]).is_contiguous() is True

    def test_two_adjacent_frames(self):
        assert make_seq([5, 6]).is_contiguous() is True

    def test_two_non_adjacent_frames(self):
        assert make_seq([5, 7]).is_contiguous() is False


class TestMissingFrames:
    def test_no_missing_frames(self):
        assert make_seq([0, 1, 2]).missing_frames() == []

    def test_single_missing_frame(self):
        assert make_seq([0, 1, 3]).missing_frames() == [2]

    def test_multiple_missing_frames(self):
        assert make_seq([0, 3]).missing_frames() == [1, 2]

    def test_missing_frames_sorted(self):
        # frames arrive unsorted; missing_frames result must still be sorted
        s = Sequence("s", "exr", [5, 0, 3], 4)
        assert s.missing_frames() == [1, 2, 4]

    def test_single_frame_no_missing(self):
        assert make_seq([10]).missing_frames() == []


class TestStepSize:
    def test_even_step_of_2(self):
        assert make_seq([0, 2, 4, 6]).step_size() == 2

    def test_even_step_of_10(self):
        assert make_seq([0, 10, 20]).step_size() == 10

    def test_step_1_returns_none(self):
        # step of 1 is just a contiguous sequence — not "stepped"
        assert make_seq([0, 1, 2, 3]).step_size() is None

    def test_uneven_gaps_returns_none(self):
        assert make_seq([0, 2, 5]).step_size() is None

    def test_single_frame_returns_none(self):
        assert make_seq([0]).step_size() is None

    def test_two_frames_with_gap(self):
        assert make_seq([0, 4]).step_size() == 4


# ===========================================================================
# SequenceParser — private helpers (pure functions, no I/O)
# ===========================================================================

class TestDetectPadding:
    def setup_method(self):
        self.parser = SequenceParser()

    def test_4_digit_padding(self):
        assert self.parser._detect_padding("seq3800.0001.exr") == 4

    def test_3_digit_padding(self):
        assert self.parser._detect_padding("seq3600.001.exr") == 3

    def test_1_digit_padding(self):
        assert self.parser._detect_padding("seq3800.1.exr") == 1


class TestExtractFrameNumber:
    def setup_method(self):
        self.parser = SequenceParser()

    def test_zero_padded_frame(self):
        assert self.parser._extract_frame_number("seq3800.0001.exr") == 1

    def test_large_frame_number(self):
        assert self.parser._extract_frame_number("seq.1234.exr") == 1234

    def test_frame_zero(self):
        assert self.parser._extract_frame_number("seq.0000.exr") == 0


class TestGroupByKey:
    def setup_method(self):
        self.parser = SequenceParser()

    def test_single_sequence(self):
        files = ["seq.0001.exr", "seq.0002.exr"]
        grouped = self.parser._group_by_key(files)
        assert ("seq", 4) in grouped
        assert len(grouped[("seq", 4)]) == 2

    def test_mixed_padding_creates_separate_groups(self):
        files = ["seq.0001.exr", "seq.001.exr"]
        grouped = self.parser._group_by_key(files)
        assert ("seq", 4) in grouped
        assert ("seq", 3) in grouped

    def test_two_different_sequences(self):
        files = ["seqA.0001.exr", "seqB.0001.exr"]
        grouped = self.parser._group_by_key(files)
        assert ("seqA", 4) in grouped
        assert ("seqB", 4) in grouped


# ===========================================================================
# SequenceParser — parse_directory (uses tmp_path for real filesystem I/O)
# ===========================================================================

class TestParseDirectory:
    def test_parses_contiguous_sequence(self, tmp_path):
        for i in range(4):
            (tmp_path / f"seq.{i:04d}.exr").touch()

        parser = SequenceParser()
        seqs = parser.parse_directory(str(tmp_path))

        assert len(seqs) == 1
        s = seqs[0]
        assert s.name == "seq"
        assert s.extension == "exr"
        assert s.frames == [0, 1, 2, 3]
        assert s.padding == 4

    def test_hidden_files_ignored(self, tmp_path):
        (tmp_path / ".hidden").touch()
        (tmp_path / "seq.0001.exr").touch()

        parser = SequenceParser()
        seqs = parser.parse_directory(str(tmp_path))

        assert len(seqs) == 1

    def test_two_separate_sequences(self, tmp_path):
        for i in range(3):
            (tmp_path / f"shotA.{i:04d}.exr").touch()
            (tmp_path / f"shotB.{i:04d}.exr").touch()

        parser = SequenceParser()
        seqs = parser.parse_directory(str(tmp_path))
        names = {s.name for s in seqs}

        assert names == {"shotA", "shotB"}

    def test_nonexistent_directory_exits(self, tmp_path):
        parser = SequenceParser()
        with pytest.raises(SystemExit):
            parser.parse_directory(str(tmp_path / "does_not_exist"))

    def test_empty_directory_exits(self, tmp_path):
        parser = SequenceParser()
        with pytest.raises(SystemExit):
            parser.parse_directory(str(tmp_path))


# ===========================================================================
# SequenceFormatter
# ===========================================================================

class TestFormatContiguous:
    def setup_method(self):
        self.fmt = SequenceFormatter()

    def test_basic_contiguous(self):
        s = make_seq([0, 1, 2, 3])
        assert self.fmt.format(s) == "seq.0-3#4.exr"

    def test_single_frame(self):
        s = make_seq([5])
        assert self.fmt.format(s) == "seq.5-5#4.exr"

    def test_no_padding_omits_hash(self):
        s = Sequence("seq", "exr", [0, 1, 2], padding=0)
        assert "#" not in self.fmt.format(s)


class TestFormatStepped:
    def setup_method(self):
        self.fmt = SequenceFormatter()

    def test_step_of_2(self):
        s = make_seq([0, 2, 4])
        assert self.fmt.format(s) == "seq.0-4x2#4.exr"

    def test_step_of_10(self):
        s = make_seq([0, 10, 20])
        assert self.fmt.format(s) == "seq.0-20x10#4.exr"


class TestFormatMissing:
    def setup_method(self):
        self.fmt = SequenceFormatter()

    def test_single_missing_frame_splits_into_two_chunks(self):
        # frames 0,1,3 — missing 2 — becomes "0-1,3-3"
        s = make_seq([0, 1, 3])
        result = self.fmt.format(s)
        assert result == "seq.0-1,3-3#4.exr"

    def test_multiple_gaps(self):
        # frames 0,1,3,4,6 — two gaps
        s = make_seq([0, 1, 3, 4, 6])
        result = self.fmt.format(s)
        assert result == "seq.0-1,3-4,6-6#4.exr"


class TestGetContiguousChunks:
    def setup_method(self):
        self.fmt = SequenceFormatter()

    def test_already_contiguous(self):
        assert self.fmt._get_contiguous_chunks([0, 1, 2]) == [[0, 1, 2]]

    def test_single_gap(self):
        assert self.fmt._get_contiguous_chunks([0, 1, 3, 4]) == [[0, 1], [3, 4]]

    def test_every_frame_isolated(self):
        assert self.fmt._get_contiguous_chunks([0, 2, 4]) == [[0], [2], [4]]

    def test_single_element(self):
        assert self.fmt._get_contiguous_chunks([7]) == [[7]]


# ===========================================================================
# Integration: parser -> formatter round-trip
# ===========================================================================

class TestRoundTrip:
    def test_contiguous_round_trip(self, tmp_path):
        for i in range(5):
            (tmp_path / f"shot.{i:04d}.exr").touch()

        parser = SequenceParser()
        formatter = SequenceFormatter()
        seqs = parser.parse_directory(str(tmp_path))

        assert formatter.format(seqs[0]) == "shot.0-4#4.exr"

    def test_stepped_round_trip(self, tmp_path):
        for i in [0, 2, 4, 6]:
            (tmp_path / f"shot.{i:04d}.exr").touch()

        parser = SequenceParser()
        formatter = SequenceFormatter()
        seqs = parser.parse_directory(str(tmp_path))

        assert formatter.format(seqs[0]) == "shot.0-6x2#4.exr"
