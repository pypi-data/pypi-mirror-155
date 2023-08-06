# bigmcl
## Large scale Markov clustering (MCL) via subgraph extraction    

`bigmcl` will isolate disconnected subgraphs from a large graph file and execute
MCL on the subgraphs. bigmcl enables MCL on large, highly disconnected graphs, 
such as those used in orthogroup inference. Not recommended for graphs that are 
manageable with typical MCL.

Important to note that the inflation parameter is affected by this approach -
I have noted clusters are more granular if anything. In the future, I plan on
implementing a systematic approach option for identifying ideal inflations for
each subgraph.

Please cite this git repository and MCL when this software contributes to your analysis.


## DISCLAIMER
`bigmcl` is currently in a beta state, and while I appreciate bringing issues to
my attention, I am currently focused on getting things working well for my own
research, so I cannot guarantee timely issue resolution. My hope is `bigmcl` will
be in a longterm stable state by publication 2022.


<br />

## INSTALL

```
pip install bigmcl
```

Clone `mcl` [from here](https://github.com/micans/mcl), compile, and add to your path.

<br />

## USE

Input and go:
```
bigmcl -i <GRAPH.imx> -I 1.5
```

More elaborate options:
```
usage: bigmcl.py [-h] -i INPUT -I INFLATION [-s] [-r ROW_FILE] [-m] [-o OUTPUT] [-c CORES]
                 [-v]

Isolates disconnected graphs and runs MCL on the subgraphs. Input data must be numerical.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        MCL graph file in imx format
  -I INFLATION, --inflation INFLATION
  -s, --symmetric       Matrix is symmetric (throughput increase)
  -r ROW_FILE, --row_file ROW_FILE
                        Continue from finished row.txt
  -m, --mcl_format      Output clusters in MCL format
  -o OUTPUT, --output OUTPUT
                        Alternative output directory
  -c CORES, --cores CORES
  -v, --verbose
```

