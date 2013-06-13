## Usage


### For importing the module

```python
from gp import Search
```

### Initialize Search object

Type the term you would like to search. This only searches apps!

```python
search = Search('twitter')
```
### Getting results

Get just the first result

```python
app = search.get_first()
```

Get entire first page

```python
page = i.get_all()
```

### More

If you would like to see all the apps with there permissions(24apps/page)


```python
for s in range(0,24):
    print p[s].get_name(), p[s].get_premis()
```