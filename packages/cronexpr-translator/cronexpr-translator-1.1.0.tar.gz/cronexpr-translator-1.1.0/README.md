cronexpr-translator
-
The python translator for cron expressions

---

`cronexpr-translator` gets a cron expression in a string format and returns a string in the following format with the
description of every field in the given cron expression.

** The translator leverages `cronexpr-validator` to validate the given cron expressions.
1. If an invalid cron expression is provided, the translator will return `CRON EXPRESSION IS NOT VALID` message,
but will not raise an error.
2. If one of the subexpressions is not translated by any reason, the translator will return 
`COULD NOT TRANSLATE SUBEXPRESSION` in the subexpression description, and will not raise an error.
3. In summary, any raised errors by the application are not expected, and must be reported as a bug.

`second -> seconds description` \
`minute -> minutes description` \
`hour -> hours description` \
`day of month -> days of month description` \
`month -> month description` \
`day of week -> days of week description` \
`year -> years description`
- Usage example

```python
from cronexpr-translator.translator import Translator

cron_expression_sample = "* * * * * *"
translated_cron_expression = Translator.translate_expression(cron_expression_sample)    
```
The output of the code snippet showed above, will be something like:

```
second -> seconds description
minute -> minutes description
hour -> hours description
day of month -> days of month description
month -> month description
day of week -> days of week description
year -> years description
```

Below you can find the description rules for every field of the cron expression.

** The connectors from the list expression types are for range values within the list. List values are separated by a comma.

**SECONDS**

|**Expression Type** |**Prefix**|**Suffix**             |**Connector**|**Iterator prefix**|**Iterator suffix**|**Start value prefix**|**Start value suffix**|
|--------------------|----------|-----------------------|-------------|-------------------|-------------------|----------------------|----------------------|
|STAR [ \* ]         |every     |second                 |None         |None               |None               |None                  |None                  |
|VALUE [ACTUAL VALUE]|at second |None                   |None         |None               |None               |None                  |None                  |
|SLASH [ \/ ]        |None      |None                   |None         |every              |seconds            |starting at second    |past the minute       |
|RANGE [ \- ]        |seconds   |past the minute        |through      |None               |None               |None                  |None                  |
|LIST [ \, ]         |at        |seconds past the minute|through      |None               |None               |None                  |None                  |

**MINUTES**

|**Expression Type** |**Prefix**|**Suffix**           |**Connector**|**Iterator prefix**|**Iterator suffix**|**Start value prefix**|**Start value suffix**|
|--------------------|----------|---------------------|-------------|-------------------|-------------------|----------------------|----------------------|
|STAR [ \* ]         |every     |minute               |None         |None               |None               |None                  |None                  |
|VALUE [ACTUAL VALUE]|at minute |None                 |None         |None               |None               |None                  |None                  |
|SLASH [ \/ ]        |None      |None                 |None         |every              |minutes            |starting at minute    |past the hour         |
|RANGE [ \- ]        |minutes   |past the hour        |through      |None               |None               |None                  |None                  |
|LIST [ \, ]         |at        |minutes past the hour|through      |None               |None               |None                  |None                  |

**HOURS**

|**Expression Type** |**Prefix**|**Suffix**|**Connector**|**Iterator prefix**|**Iterator suffix**|**Start value prefix**|**Start value suffix**|
|--------------------|----------|----------|-------------|-------------------|-------------------|----------------------|----------------------|
|STAR [ \* ]         |every     |hour      |None         |None               |None               |None                  |None                  |
|VALUE [ACTUAL VALUE]|at        |None      |None         |None               |None               |None                  |None                  |
|SLASH [ \/ ]        |None      |None      |None         |every              |hours              |starting at           |None                  |
|RANGE [ \- ]        |between   |None      |and          |None               |None               |None                  |None                  |
|LIST [ \, ]         |at        |None      |and          |None               |None               |None                  |None                  |

**DAY OF MONTH**

|**Expression Type** |**Prefix** |**Suffix**  |**Connector**|**Iterator prefix**|**Iterator suffix**|**Start value prefix**|**Start value suffix**|
|--------------------|-----------|------------|-------------|-------------------|-------------------|----------------------|----------------------|
|STAR [ \* ]         |every      |day         |None         |None               |None               |None                  |None                  |
|VALUE [ACTUAL VALUE]|on day     |of the month|None         |None               |None               |None                  |None                  |
|SLASH [ \/ ]        |None       |None        |None         |every              |days               |starting on day       |of the month          |
|RANGE [ \- ]        |between day|of the month|and          |None               |None               |None                  |None                  |
|LIST [ \, ]         |on day     |of the month|through      |None               |None               |None                  |None                  |

- Day of month also allows L and W characters, with special rules:

`last day expression[L]` -> on the last day of the month \
`first week day expression[1W]` -> first week day of the month \
`week day expression[_DIGIT_W or W_DIGIT_]` -> on the week day nearest day _DIGIT_ of the month \
`last week day expression[LW or WL]` -> on the last week day of the month

**MONTH**

|**Expression Type** |**Prefix** |**Suffix**  |**Connector**|**Iterator prefix**|**Iterator suffix**|**Start value prefix**|**Start value suffix**|
|--------------------|-----------|------------|-------------|-------------------|-------------------|----------------------|----------------------|
|STAR [ \* ]         |every      |month       |None         |None               |None               |None                  |None                  |
|VALUE [ACTUAL VALUE]|only in    |None        |None         |None               |None               |None                  |None                  |
|SLASH [ \/ ]        |None       |None        |None         |every              |months             |None                  |through december      |
|RANGE [ \- ]        |None       |None        |through      |None               |None               |None                  |None                  |
|LIST [ \, ]         |only in    |None        |through      |None               |None               |None                  |None                  |

**DAY OF WEEK**

|**Expression Type** |**Prefix** |**Suffix**     |**Connector**|**Iterator prefix**|**Iterator suffix**|**Start value prefix**|**Start value suffix**|
|--------------------|-----------|---------------|-------------|-------------------|-------------------|----------------------|----------------------|
|STAR [ \* ]         |every      |day of the week|None         |None               |None               |None                  |None                  |
|VALUE [ACTUAL VALUE]|only on    |None           |None         |None               |None               |None                  |None                  |
|SLASH [ \/ ]        |None       |None           |None         |every              |days of the week   |None                  |through saturday      |
|RANGE [ \- ]        |None       |None           |through      |None               |None               |None                  |None                  |
|LIST [ \, ]         |only on    |None           |through      |None               |None               |None                  |None                  |

- Day of week also allows the L character, with special rules:

`last day expression[_DIGIT_L or L_DIGIT_]` -> on the last _DIGIT_ of the month \
`last day expression[L]` -> only in saturday

**YEAR**

|**Expression Type** |**Prefix** |**Suffix**  |**Connector**|**Iterator prefix**|**Iterator suffix**|**Start value prefix**|**Start value suffix**|
|--------------------|-----------|------------|-------------|-------------------|-------------------|----------------------|----------------------|
|STAR [ \* ]         |every      |year        |None         |None               |None               |None                  |None                  |
|VALUE [ACTUAL VALUE]|only in    |None        |None         |None               |None               |None                  |None                  |
|SLASH [ \/ ]        |None       |None        |None         |every              |years              |None                  |through 2099          |
|RANGE [ \- ]        |None       |None        |through      |None               |None               |None                  |None                  |
|LIST [ \, ]         |only in    |None        |through      |None               |None               |None                  |None                  |
