# Lolcatfigletgnuplotprint

A simple commandline output utility package for printing simple messages and linear xy-plot data with colours and style

## Requirements

Relies on [lolcat](https://github.com/tehmaze/lolcat), [figlet](http://www.figlet.org/) and [gnuplot](http://www.gnuplot.info/).

## Install

```
python -m pip install lolcatfigletgnuplotprint
```

## Usage

As a library function:

```
from lolcatfigletgnuplotprint import print_example
print_example()
```

```
from lolcatfigletgnuplotprint import lolcat_figlet_print

lolcat_figlet_print(
    message="Content",
    heading_text="Example heading",
    description_text="A description",
)
```

```
from lolcatfigletgnuplotprint import plot_print

plot_print(
    value_groups=[
        {
            "title": "Data 1",
            "values": [
                {"value": 1, "timestamp": 1655305933},
                {"value": 5, "timestamp": 1655305938},
                {"value": 2, "timestamp": 1655305943},
            ],
        },
        {
            "title": "Data 2",
            "values": [
                {"value": 7, "timestamp": 1655305933},
                {"value": 3, "timestamp": 1655305938},
                {"value": 5, "timestamp": 1655305943},
            ],
        },
    ],
)
```

As commandline util:

```
python -m lolcatfigletgnuplotprint --help
```

As ran with pre-built docker image:

```
docker run -it --rm lsipii/lolcatfigletgnuplotprint --help
```

## Example output

![Example output](./resourses/example-cli-output.png)
