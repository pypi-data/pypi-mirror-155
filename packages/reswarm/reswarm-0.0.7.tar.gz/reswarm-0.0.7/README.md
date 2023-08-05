# reswarm-py

## About

Makes publishing data to a Record Evolution Datapod incredibly easy!

## Usage

```
from asyncio.events import get_event_loop
from reswarm import Reswarm

async def main():
    rw = Reswarm(serial_number="7652ee0b-c2cb-466a-b8ee-fec4167bf7ce")
    result = await rw.publish('re.meetup.data', {"temperature": 20})
    print(result)

if __name__ == "__main__":
    get_event_loop().run_until_complete(main())
```

## Options

The `Reswarm` `__init__` function can be configured with the following options:

```
{
    serial_number: string;
}
```

**serial_number**: Used to set the serial_number of the device if the `DEVICE_SERIAL_NUMBER` environment variable does not exist. It can also be used if the user wishes to authenticate as another device.
