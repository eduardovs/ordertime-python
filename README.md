# Python OrderTime API

A basic python api helper to get data from the app [OrderTime](https://www.ordertime.com/) by [NumberCruncher](https://www.numbercruncher.com/)

## Getting Started

- [Get an API key](https://help.ordertime.com/help/getting-the-api-key) from OrderTime
- Store it, as well as your user name and password in a .env file, preferrably. In my case I've used a .ini for storing this data.
- Install the `requests` library.
```
pip install requests
```

## Sample Scripts

This folder contains a few examples of how I have used the OrderTime api to retrieve product and pricing data.

The relevant examples are:
- `volumepricelevels.py`
- `pricelevels.py`
- `iteminfo.py`

`monitor_base_pricing.py` and `filecomparerdaff.py` are just examples of how I've used the outputs from OrderTime to compare with my local excel data sources, in order to find discrepancies in both data, especially when it relates to pricing. At my company, we use Excel extensively to determine cost and sale prices and this script, and others I didn't share hear, audits and monitors changes and such discrepancies.

## Contributing

Feel free to fork this project and modify it to your liking, as its license gives you permission to do so. 

Because my company no longer uses OrderTime, I stopped developing this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.






