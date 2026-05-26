import logging
import sys
from collections import defaultdict
from pathlib import Path

logger = logging.getLogger(__name__)


class Sequence:
    """
    Holds parsed sequence data.
    """

    def __init__(self, name: str, extension: str, frames: list[int], padding: int):
        self.name = name            # "seq3800"
        self.extension = extension  # "exr"
        self.frames = sorted(frames)
        self.padding = padding

    def startframe(self) -> int:
        return self.frames[0]

    def endframe(self) -> int:
        return self.frames[-1]

    def is_contiguous(self) -> bool:
        expected = set(range(self.startframe(), self.endframe() + 1))
        return expected == set(self.frames)

    def missing_frames(self) -> list[int]:
        expected = set(range(self.startframe(), self.endframe() + 1))
        return sorted(expected - set(self.frames))

    def step_size(self) -> int | None:
        """
        Returns the step size if the sequence is evenly stepped, otherwise None.
        e.g. [0, 2, 4, 6] -> 2,  [0, 1, 3] -> None
        """
        differences = [self.frames[i] - self.frames[i - 1] for i in range(1, len(self.frames))]
        if len(set(differences)) == 1 and differences[0] > 1:
            return differences[0]
        return None


class SequenceParser:
    """
    Turns a directory of filenames into a list of Sequence objects.
    Reads and parses files.
    """

    def parse_directory(self, path: str) -> list[Sequence]:
        """
        Reads a directory and returns a list of Sequence objects.
        """
        files = self._get_files(path)
        grouped = self._group_by_key(files)

        sequences = []
        for (name, padding), filenames in grouped.items():
            frames = [self._extract_frame_number(f) for f in filenames]
            extension = filenames[0].rsplit('.', 1)[-1]
            sequences.append(Sequence(name, extension, frames, padding))

        return sequences

    def _get_files(self, path: str) -> list[str]:
        """
        Reads filenames from a directory, ignoring hidden files.
        """
        p = Path(path)
        if not p.is_dir():
            logger.error(f"Directory not found: {path}")
            sys.exit("Directory does not exist")

        files = sorted(f.name for f in p.iterdir() if not f.name.startswith('.'))

        if not files:
            logger.error("No files found")
            sys.exit(1)

        return files

    def _group_by_key(self, files: list[str]) -> dict[tuple, list[str]]:
        """
        Groups filenames by (sequence name, padding length).
        Keeping padding in the key means mixed-padding sequences become separate groups.

        e.g. seq3600.0001.exr -> ("seq3600", 4)
             seq3600.001.exr  -> ("seq3600", 3)
        """
        grouped = defaultdict(list)
        for filename in files:
            name = filename.rsplit('.', 2)[0]
            padding = self._detect_padding(filename)
            grouped[(name, padding)].append(filename)
        return grouped

    def _extract_frame_number(self, filename: str) -> int:
        """
        Extracts the integer frame number from a filename.
        e.g. "seq3800.0001.exr" -> 1
        """
        try:
            return int(filename.rsplit('.', 2)[-2])
        except (ValueError, IndexError):
            logger.error(f"Invalid filename format: {filename}. Expected name.framenumber.extension")
            sys.exit(1)

    def _detect_padding(self, filename: str) -> int:
        """
        Detects the padding width from a single filename.
        e.g. "seq3800.0001.exr" -> 4,  "seq3800.1.exr" -> 1
        """
        frame_str = filename.rsplit('.', 2)[-2]
        return len(frame_str)


class SequenceFormatter:
    """
    Renders a Sequence to a compact string.
    """

    def format(self, sequence: Sequence) -> str:
        """
        Dispatches to the appropriate formatting method based on sequence type.
        """
        if sequence.step_size():
            return self._format_stepped(sequence)
        elif sequence.missing_frames():
            return self._format_missing(sequence)
        else:
            return self._format_contiguous(sequence)

    def _format_contiguous(self, sequence: Sequence) -> str:
        """
        seq3800.0000.exr - seq3800.0003.exr  ->  seq3800.0-3#4.exr
        """
        frame_range = f"{sequence.startframe()}-{sequence.endframe()}"
        padding = f"#{sequence.padding}" if sequence.padding else ""
        return f"{sequence.name}.{frame_range}{padding}.{sequence.extension}"

    def _format_stepped(self, sequence: Sequence) -> str:
        """
        seq3800.0000.exr, seq3800.0002.exr, seq3800.0004.exr  ->  seq3800.0-4x2#4.exr
        """
        frame_range = f"{sequence.startframe()}-{sequence.endframe()}"
        step = f"x{sequence.step_size()}"
        padding = f"#{sequence.padding}" if sequence.padding else ""
        return f"{sequence.name}.{frame_range}{step}{padding}.{sequence.extension}"

    def _format_missing(self, sequence: Sequence) -> str:
        """
        seq3800.0000.exr, seq3800.0002.exr, seq3800.0003.exr  ->  seq3800.0-1,2-3#4.exr

        Handles multiple missing frames by splitting into contiguous chunks.
        """
        chunks = self._get_contiguous_chunks(sequence.frames)
        padding = f"#{sequence.padding}" if sequence.padding else ""
        range_str = ",".join(f"{chunk[0]}-{chunk[-1]}" for chunk in chunks)
        return f"{sequence.name}.{range_str}{padding}.{sequence.extension}"

    def _get_contiguous_chunks(self, frames: list[int]) -> list[list[int]]:
        """
        Splits a frame list into contiguous runs.
        e.g. [0, 1, 3, 4, 5] -> [[0, 1], [3, 4, 5]]
        """
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
