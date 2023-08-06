from dataclasses import dataclass
import re


@dataclass
class ContentRange:
    first: int
    last: int
    count: int
    unit: str

    _pattern = re.compile(r'^(\w+) (\d+)-(\d+)\/(\d+)$')

    @classmethod
    def parse(cls, header: str) -> 'ContentRange':
        result = cls._pattern.search(header)

        if result:
            unit, first, last, count = result.groups()

            return ContentRange(
                first=int(first),
                last=int(last),
                count=int(count),
                unit=unit,
            )

        raise ValueError('Could not parse content range')
