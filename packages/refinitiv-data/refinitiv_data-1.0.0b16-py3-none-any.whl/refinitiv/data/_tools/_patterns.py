"""ADC patterns for fincoder layer and fundamental and reference content object."""

import re

# re for ADC fields like started with "TR." case is ignored
ADC_TR_PATTERN = re.compile(r"^tr\..+", re.I)

# re for ADC date fields ended witH ".date" case is ignored
ADC_DATE_PATTERN = re.compile(r"^.+\.date$", re.I)

# re for finding expressions inside ADC fields like
# "TR.F.TotRevPerShr(SDate=0,EDate=-2,Period=FY0,Frq=FY).date"
ADC_PARAM_IN_FIELDS = re.compile(r".*\(.+\).*")

# re for ADC functions in fields like AVAIL(, AVG(
# AVAIL(TR.GrossProfit(Period=LTM,Methodology=InterimSum))
ADC_FUNC_PATTERN_IN_FIELDS = re.compile(r"^[A-Z]+\(")


# re for finding column name include sub-string
# ..._DATE...int
# ...DATE...int
# ..._DT...int
# ...DT...int
# ...DAT...int
PRICING_DATETIME_PATTERN = re.compile(".*(DATE|DT|DAT)\d*$")
