# Introduction

Get your China A-share financial risk metrics **alpha, beta** out of box.

## Installation
```
pip install finstats
```

# Usage

## flags:

- -s:  specify the stock code
- -b:  specify the benchmark code, usually sh000001, sh000300
- -r:  risk free return. default 0
- -p:  period. periodicity of the 'returns' data:: y/q/m/w/d, default is d
- -l:  number of records to fetch, default is 1023.
  


use **finstats --help** to see more details
## example:

```bash
finstats -s sh600519 -b sh000001 -l 500
```

# Data Source

finstats uses Sina HTTP API as its data source