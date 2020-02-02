# Pinger
Pinger is a tool to ping the ip addresses in files such as excel or csv to show if the hosts are turned on.

### How to Run
```
python3 pinger.py -f [file_name] 
```
or
```
./pinger.py -f [file_name]
```
![output](pictures/output.png)

### Parameters
| Short        | Long           | Description  | Default Value |
|:-----|:-----|:-----|:-----|
| -h | --help | Show this help message and exit |
| -f FILENAME | --filename FILENAME |   Name of file |
| -s SHEET | --sheet SHEET |  Sheet index | [default = 0] | 
| -c COLUMN | --column COLUMN | Column of ip address | [default = 0] |
| -pc PINGCOUNT | --pingcount PINGCOUNT | How many times sending ping request | [default = 3] |

![output](pictures/help.png)