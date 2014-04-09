# last.fm faves dumper

A python script to dump your last.fm faves list into simplified JSON:

``` json
[
    {
        "date": "2012/05/20", 
        "name": "Halcyon + On + On", 
        "artist": "Orbital"
    }, 
    {
        "date": "2012/05/20", 
        "name": "Iron Man", 
        "artist": "Black Sabbath"
    }, 
    {
        "date": "2012/05/20", 
        "name": "Summer of '69", 
        "artist": "Bryan Adams"
    }
]
```

Or YAML:

``` yaml
- artist: The Killers
  date: 2014/04/08
  name: I Can't Stay
- artist: Michael Penn
  date: 2014/04/03
  name: Walter Reed
- artist: The Handsome Family
  date: 2014/04/02
  name: Far From Any Road
```

Installation:

```
pip install -e git+https://github.com/dreikanter/favesdump.git#egg=favesdump
```

Here are some usage examples. This command will dump faces for `username` using default file name and format settings:

```
favesdump username
```

This one will dump faves for `username` to `username.yml` file:

```
favesdump --path username.yml --format yaml username
```

It is possible to use some autoreplacemnts to define your own output file format, which could be helpful for automation:

```
favesdump --path {timestamp}-{user}.{format} --format yaml username
```

Use `favesdump --help` for command line usage.
