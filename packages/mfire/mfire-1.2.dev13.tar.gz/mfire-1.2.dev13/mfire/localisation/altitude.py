"""Module for manipulating names of areas defined by their altitude.

It considers suchs areas as a given type of Intervals, and it is then possible
to combine them (union, intersection, difference) as you can expect from any interval.

There is also functions and methods to combine altitude-defined areas with other
areas.
"""

from __future__ import annotations
import re
from typing import Tuple, Optional

import interval as PyInterval

from mfire.settings import LANGUAGE, ALT_MIN, ALT_MAX

# defining useable class function outside the module
__all__ = ["AltitudeInterval", "rename_alt_min_max"]


# functions to export outside the module
def rename_alt_min_max(
    area_name: str, alt_min: Optional[int] = ALT_MIN, alt_max: Optional[int] = ALT_MAX,
) -> str:
    """Renames a given area_name according to the given alt_min and alt_max thresholds.

    >>> rename_alt_min_max("à Toulouse", 0, 1000)
    "à Toulouse"
    >>> rename_alt_min_max("entre 1000 m et 2000 m", alt_max=2000)
    "au-dessus de 1000 m"

    Args:
        area_name (str): Name to change if related to the alt_min and alt_max.
        alt_min (Optional[int], optional): Alt min threshold. Defaults to ALT_MIN.
        alt_max (Optional[int], optional): Alt max threshold. Defaults to ALT_MAX.

    Returns:
        str: New name
    """
    area_interval = AltitudeInterval.from_str(area_name)
    if bool(area_interval):
        return area_interval.name(alt_min=alt_min, alt_max=alt_max)
    return area_name


# extending 'interval' class
class AltitudeInterval(PyInterval.interval):
    """Class extending PyInterval 'interval' class in order to apply interval
    arithmetic to altitude's names fusion.
    We extend the class in order to bring some basic algebra of sets to intervals
    (because we, in our case, tend to consider intervals as sets).
    """

    units = "m"
    pattern = re.compile(
        fr"(?:{LANGUAGE.dessous} (\d+) m)"
        fr"|(?:{LANGUAGE.entre} (\d+) m {LANGUAGE.et} (\d+) m)"
        fr"|(?:{LANGUAGE.a_grave} (\d+) m)"
        fr"|(?:{LANGUAGE.dessus} (\d+) m)"
    )

    def __invert__(self) -> AltitudeInterval:
        """Implementation of the unary operator '~' used to invert an interval.
        We define the "inverse" of an interval I as:
        * I | ~I == [-inf, inf] (i.e. union(I, ~I) = everything)
        * I & ~I == singleton(min(I)), singleton(max(I))
            if min(I) != -inf and max(I) != inf

        For example:
        >>> ~AltitudeInterval([-inf, 0])
        AltitudeInterval([0, inf])
        >>> ~AltitudeInterval([0, 100])
        AltitudeInterval([-inf, 0], [100, inf])
        >>> ~AltitudeInterval([0])
        AltitudeInterval([-inf, inf])
        >>> ~AltitudeInterval([-inf, 0], [100, 200], [300], [400, inf])
        AltitudeInterval([0, 100], [200, 400])

        Returns:
            AltitudeInterval: Inverted (or complementary) of self
        """
        bounds = (
            [-PyInterval.inf]
            + list(b for comp in self for b in comp)
            + [PyInterval.inf]
        )
        return self.__class__(
            *(
                (bounds[i], bounds[i + 1])
                for i in range(0, len(bounds), 2)
                if bounds[i] != PyInterval.inf and bounds[i + 1] != -PyInterval.inf
            )
        )

    def difference(self, other: AltitudeInterval) -> AltitudeInterval:
        """Implementation of the "set's" corresponding difference.
        It returns a new AltitudeInterval with sections of self that are not in other.

        For instance:
        >>> AltitudeInterval([0, 1000]).difference([500, inf])
        AltitudeInterval([0, 500])

        !Warning: Do not use the operator '-' for this difference. Indeed, the
        __sub__ dunder method is already used for applying the arithmetic substraction.

        Args:
            other (AltitudeInterval): Other interval to apply difference to

        Returns:
            AltitudeInterval: New substracted AltitudeInterval
        """
        return self & (~self.__class__(other))

    def __xor__(self, other: AltitudeInterval) -> AltitudeInterval:
        """Implementation of the "set's" corresponding symmetric_difference.
        It returns a new AltitudeInterval with sections in either the self
        or other but not both.

        Args:
            other (AltitudeInterval): Other interval to apply the difference to.

        Returns:
            AltitudeInterval: New symmetrically substracted AltitudeInterval
        """
        return self.difference(other) | self.__class__(other).difference(self)

    def symmetric_difference(self, other: AltitudeInterval) -> AltitudeInterval:
        """Implementation of the "set's" corresponding symmetric_difference.
        It returns a new AltitudeInterval with sections in either the self
        or other but not both.

        Args:
            other (AltitudeInterval): Other interval to apply the difference to.

        Returns:
            AltitudeInterval: New symmetrically substracted AltitudeInterval
        """
        return self ^ other

    def issubinterval(self, other: AltitudeInterval) -> bool:
        """Test whether the self interval is a sub interval of the other interval,
        i.e. self is a subset of the other set.

        Args:
            other (AltitudeInterval): Other set to test the inclusion with.

        Returns:
            bool: True if self is a sub-interval of other, else False
        """
        return (self & self.__class__(other)) == self

    def issuperinterval(self, other: AltitudeInterval) -> bool:
        """Test whether the self interval is a super interval of the other interval,
        i.e. other is a subset of the self set.

        Args:
            other (AltitudeInterval): Other set to test the inclusion with.

        Returns:
            bool: True if self is a super-interval of other, else False
        """
        other_interval = self.__class__(other)
        return (self & other_interval) == other_interval

    @classmethod
    def name_section(
        cls,
        section: Tuple[Optional[int], Optional[int]],
        alt_min: Optional[int] = ALT_MIN,
        alt_max: Optional[int] = ALT_MAX,
    ) -> str:
        """Class method used for naming a single section (or self.Component)
        of an interval.

        Examples:
        >>> AltitudeInterval.name_section((-inf, 1000))
        "en dessous de 1000 m"
        >>> AltitudeInterval.name_section((1000, inf))
        "au-dessus de 1000 m"
        >>> AltitudeInterval.name_section((1000, 2000))
        "entre 1000 m et 2000 m"
        >>> AltitudeInterval.name_section((1000, 2000), alt_max=2000)
        "au-dessus de 1000 m"
        >>> AltitudeInterval.name_section((1000, 1000))
        "à 1000 m"

        Args:
            section (Tuple[int, int]): (low, high) altitude values to name.
            alt_min (Optional[int], optional): Alt min boundary. Defaults to ALT_MIN.
            alt_max (Optional[int], optional): Alt max boundary. Defaults to ALT_MAX.

        Returns:
            str: Name of the given section.
        """
        alt_min = int(alt_min) if alt_min is not None else ALT_MIN
        alt_max = int(alt_max) if alt_max is not None else ALT_MAX
        low, high = (int(v) if abs(v) != PyInterval.inf else v for v in section)
        if low <= alt_min and high >= alt_max:
            return ""
        if low == high:
            if low <= alt_min or high >= alt_max:
                return ""
            return f"{LANGUAGE.a_grave} {low} {cls.units}"
        if alt_min < low < alt_max <= high:
            return f"{LANGUAGE.dessus} {low} {cls.units}"
        if low <= alt_min < high < alt_max:
            return f"{LANGUAGE.dessous} {high} {cls.units}"
        if alt_min < low < high < alt_max:
            return (
                f"{LANGUAGE.entre} {low} {cls.units} {LANGUAGE.et} {high} {cls.units}"
            )
        return ""

    def name(
        self, alt_min: Optional[int] = ALT_MIN, alt_max: Optional[int] = ALT_MAX,
    ) -> str:
        """Method for naming self interval. It basically concatenates the names
        of each of its sections.

        Examples:
        >>> inter = AltitudeInterval((-inf, 100), (200, 300), (400), (500, 1000))
        >>> inter.name()
        "en dessous de 100 m, entre 200 m et 300 m, à 400 m et entre 500 m et 1000 m"
        >>> inter.name(alt_max=1000)
        "en dessous de 100 m, entre 200 m et 300 m, à 400 m et au-dessus de 500 m"
        >>> inter.name(alt_min=400, alt_max=800)
        "au-dessus de 500 m"

        Args:
            alt_min (Optional[int], optional): Alt min boundary. Defaults to ALT_MIN.
            alt_max (Optional[int], optional): Alt max boundary. Defaults to ALT_MAX.

        Returns:
            str: Name of the self interval.
        """
        new_self = self & self.__class__((alt_min, alt_max))
        sections = [
            self.name_section(section=(low, high), alt_min=alt_min, alt_max=alt_max)
            for low, high in new_self
            if not (low == high and (low <= alt_min or high >= alt_max))
        ]  # we exclude singletons that are equals to alt_min or alt_max
        if len(sections) == 0:
            return ""
        *first, last = sections
        result = ", ".join(first)
        if bool(result):
            result += f" {LANGUAGE.et} "
        return result + last

    @classmethod
    def from_str(cls, my_str: str) -> AltitudeInterval:
        """Class method that interpret a given 'my_str' into an AltitudeInterval.

        For instance,
        >>> AltitudeInterval.from_str("au-dessus de 800 m")
        AltitudeInterval([800.0, inf])
        >>> AltitudeInterval.from_str("entre 1000 m et 2000 m")
        AltitudeInterval([1000.0, 2000.0])
        >>> AltitudeInterval.from_str("à 200 m")
        AltitudeInterval([200.0, 200.0])
        >>> AltitudeInterval.from_str("en dessous de 450 m")
        AltitudeInterval([-inf, 450])
        >>> AltitudeInterval.from_str(
        ...     "en dessous de 100 m, entre 800 m et 900 m et au-dessus de 1000 m"
        ... )
        AltitudeInterval([-inf, 100], [800, 900], [1000, inf])
        >>>  AltitudeInterval.from_str("à Toulouse")
        AltitudeInterval()

        Args:
            my_str (str): String to convert as an AltitudeInterval

        Returns:
            AltitudeInterval: New AltitudeInterval
        """
        alt_inter = cls()
        for match in cls.pattern.finditer(str(my_str)):
            match_name = match.group(0)
            values = [int(v) for v in match.groups() if v is not None]
            if LANGUAGE.dessous in match_name:
                alt_inter |= cls([-PyInterval.inf, values[0]])
            elif LANGUAGE.entre in match_name:
                alt_inter |= cls(values)
            elif LANGUAGE.a_grave in match_name:
                alt_inter |= cls(values)
            elif LANGUAGE.dessus in match_name:
                alt_inter |= cls([values[0], PyInterval.inf])
        return alt_inter
