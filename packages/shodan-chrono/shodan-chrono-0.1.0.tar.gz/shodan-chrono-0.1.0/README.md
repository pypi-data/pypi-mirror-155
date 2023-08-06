# Shodan Chrono: Python

## Quickstart

Install the library using:

```shell
pip install shodan-chrono
```

And then use it in your code:

```python
import chrono

items = [i for i in range(100)]
with chrono.progress("My Script", len(items), api_key="YOUR SHODAN API KEY") as pb:
    for item in items:
        # Do something
        # Update the progress bar after we've processed the item
        pb.update()
```

You can also tell the progress bar to update by more than 1 tick:

```python
    pb.update(5)  # Tell Chrono that we've processed 5 items
```

## Configuring the API key

The Chrono API requires a [Shodan API key](https://account.shodan.io) and there are 3 possible ways you can provide that:

* Initialize the Shodan CLI on your local machine: ``shodan init YOUR_API_KEY``
* Set the ``SHODAN_API_KEY``  environment variable. For example: ``export SHODAN_API_KEY="YOUR KEY"``
* Use the ``api_key`` parameter on the ``chrono.progress()`` class

If you're already using the Shodan CLI for other things then you won't need to configure anything in order to use Chrono.

## Contributing

Checkout the repository and then use ``poetry`` to manage the dependencies, virtual environment and packaging. To get started, simply run the following command once you're in the ``python/`` subdirectory of this repository:

```shell
poetry install
```
