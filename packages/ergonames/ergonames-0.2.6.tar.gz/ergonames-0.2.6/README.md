# Ergo Names Python SDK

### Documentation

A full list of available functions can be found [here](https://zack-balbin.gitbook.io/ergonames/sdks/sdk-functions).

Example: Resolving an ErgoName Owner Address

```python
name = "~balb"
address = resolve_ergoname(name)
```
The result (owner address) will be:

```
3WwKzFjZGrtKAV7qSCoJsZK9iJhLLrUa3uwd4yw52bVtDVv6j5TL
```

Example: Getting registration date for an ErgoName

```python
name = "~balb"
date = get_date_registered(name)
```

The result (date registered YYYY-MM-DD HH:MM:SS) will be:

```
2022-04-17 12:15:39.771000
```

### Contribute

If you wish to contribute, make a pull request!