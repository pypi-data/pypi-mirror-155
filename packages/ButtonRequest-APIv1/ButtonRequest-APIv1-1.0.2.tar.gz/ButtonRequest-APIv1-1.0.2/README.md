
# Button API V1 Library for Python
This Python library enables you to use the API effectively.

## Installation
To install use this library, you may install it with PyPi.

Open the Terminal and navigate to the folder you desire. Then type,
```bash
pip install ButtonRequest-APIv1
```

## How to use?


To use that, you must first declare the following,
```python
from ButtonRequest.APIv1 import apiClient
client = apiClient("{API Token}")
```

### Message
#### Fetch

```python
response = client.message.fetch()
```
You may also add filter conditions,
```python
response = client.message.fetch(filterDict={
    "msg_id":"{Msg ID}",
    "device_id":"{Device ID}",
    "pin":"{Pin Status}",
    "shared_to_me":"{Shared To Me}"
})

```
Eligible Filter Parameters: msg_id, device_id, pin, shared_to_me

#### Pin Status

```python
response = client.message.pinStatus("{Message ID}", "{Pin or Unpin}")
```

#### Delete
```python
response = client.message.delete("{Message ID}")
```

### DeviceList

#### Fetch
```python
response = client.deviceList.fetch()
```
You may also add filter,
```python
response = client.deviceList.fetch("{Device ID}",
    {
        "status":"{Status}",
        "repeated_message":"{Repeated Message}",
    }
);
```
Eligible Filter Parameters: status, repeated_message


#### Repeated Message
```python
response = client.deviceList.repeatedMessage("{Device Id}", "{Action}")
```

#### Button Message Update
```python

response = client.deviceList.buttonMessageUpdate("{Device Id}", 
    [
        {
            "buttonNo": "1", "message": "This is First Button"
        },
        {
            "buttonNo": "2", "message": "This is Second Button"
        }
    ]
)

```

#### Button Message Delete
```python

response = client.deviceList.buttonMessageDelete("{Device Id}", 
    [
        "{Button No 1}", "{Button No 2}"
    ]
)
```

#### New Device
```python
response = client.deviceList.newDevice("{Nickname}")
```

### Device Share
#### Fetch Shared To Me
```python
response = client.deviceShare.toMeFetch()
```
You may also pass filter array,
```python

response = client.deviceShare.toMeFetch({
    "case_id":"{Case ID}",
    "device_id":"{Device ID}",
    "owner_email":"{Email}",
    "right":"{Right}" 
})
```
Eligible Parameter: case_id, device_id, owner_email, right

#### Give Up Sharee Right
```python
response = client.deviceShare.giveUpShareeRight("{Case ID}")
```

#### Share To
```python
response = client.deviceShare.shareTo("{Device ID}", "{Email}")
```


#### Change Sharee Right
```python
response = client.deviceShare.changeShareeRight("{Case ID}", "{Right}")
```

### Mobile Access

#### Fetch
```python
response = client.mobileAccess.fetch()
```
You may also pass filter array.

```python
response = client.mobileAccess.fetch(
    {
        "case_id":"{Case ID}",
        "deleted_from_phone":"{Deleted or Not}"
    }
)
```
Eligible Parameter: case_id, deleted_from_phone

#### New
```python
response = client.mobileAccess.new("{Nickname}")
```

#### Amend Nickname


```python
response = client.mobileAccess.amendNickname("{Case ID}", "{New Nickname}")
```
#### Revoke

```python
response = client.mobileAccess.revoke("{CASE ID}")
```


## Response

Please refer to the API documentation
