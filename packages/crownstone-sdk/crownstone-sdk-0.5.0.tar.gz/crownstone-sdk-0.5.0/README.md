# Python SDK

The Python SDK bundles a couple of tools based on the Python libs:

* https://github.com/crownstone/crownstone-lib-python-ble
* https://github.com/crownstone/crownstone-lib-python-core
* https://github.com/crownstone/crownstone-lib-python-uart

If you are interested instead of creating your own tools using the above libraries, you are kindly referred to those
repositories themselves.

## Installation from PyPi

You can install these tools through pip:

```
pip install crownstone-sdk
```

## Installation from source

You can install these tools through pip also locally by:

```
git clone https://github.com/crownstone/crownstone-python-sdk
cd crownstone-python-sdk
pip install .
```

## Tool arguments

These tools are meant to be used as quick-access to common functionality. They are standalone binaries that work as is.
Again, for examples on how to use the libraries, go to the above repositories.

The tool configuration can be done through files in this repository and name them exactly like this:
- `tool_config.json`
    - You can find a template of this in the `tools/config` folder. Fill it with your settings in order for all tools to work.
- `key_file.json`
    - You can choose to use a `key_file.json` in a different location on your computer if you don't want to put keys in a repository (even though `tool_config.json` is in .gitignore). You can configure your `tool_config` to do this.

It is also possible to use command line arguments which will override the values in any file:

```
  --help                   show this help message and exit
  --bleAdapterAddress [I]  bleAdapterAddress of the BLE chip you want to use (linux only). This is usually a mac address.
  --keyFile KEYFILE        the json file with key information
  --configFile CONFIGFILE  the json file with config information
```

## Tool config

This is the tool config format. It is shown in `config/tool_config.template.json`.

#### Obtaining keys

Go to [my.crownstone](my.crownstone.rocks) and copy the access token to your clipboard.
Click of the [Crownstone REST API explorer](https://my.crownstone.rocks/explorer/), and set your access tokes.
Now you are able to make calls to the API.

To get your sphere keys go to the *users/me* tab, click the *try it out* button, and copy your ID from the response body.
With this ID you can access your keys on the */users/{id}/keysV2* tab. Fill your ID into the form and the response body should display the keys and key types. These have to be formatted like shown bellow.
```
{
  "absolutePathToKeyFile": null,
  "keys": {
    "admin":              "adminKeyForCrown",
    "member":             "memberKeyForHome",
    "basic":              "basicKeyForOther",
    "serviceDataKey":     "MyServiceDataKey",
    "localizationKey":    "aLocalizationKey",
    "meshApplicationKey": "MyGoodMeshAppKey",
    "meshNetworkKey":     "MyGoodMeshNetKey"
  },
  "bleAdapterAddress": null
}
```

#### absolutePathToKeyFile
If this is defined, the keys are ignored. The tool will look for a key_file at that path instead.

#### keys
These are the keys that belong to your sphere. They are used to decrypt the advertisements and to encrypt the communication during connections.

#### bleAdapterAddress
The bleAdapterAddress of the BLE chip you want the library to use.


## Key file
This is the format of the `key_file.json`. You can use it via the absolutePathToKeyFile config or via the keyFile command line argument.

```
{
  "admin":              "adminKeyForCrown",
  "member":             "memberKeyForHome",
  "basic":              "basicKeyForOther",
  "serviceDataKey":     "MyServiceDataKey",
  "localizationKey":    "aLocalizationKey",
  "meshApplicationKey": "MyGoodMeshAppKey",
  "meshNetworkKey":     "MyGoodMeshNetKey"
}
```

## commandLine arguments
These arguments are available for all tools. A tool may have different arguments as well, those are listed as additional parameters below the tool.

| command&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | explanation |
|--------- | --- |
| --bleAdapterAddress    | bleAdapterAddress of the BLE chip you want to use (linux only). This is usually a mac address. |
| --keyFile     | The json file with key information, expected values: admin, member, guest, basic, serviceDataKey, localizationKey, meshApplicationKey, and meshNetworkKey |
| --configFile  | The json all data required to configure the tools. See the template file or the definition above for more information. |

## Available tools

Currently, available tools are:

<details>
<summary> cs_scan_any_crownstone --verbose [--macFilter filter]</summary>

> This will scan for any available BLE (Bluetooth Low Energy) device.
> 
> - Parameters
>   - **verbose**: Optionally show full advertisement, not just a single line summary.
>   - **macFilter**(string): Optionally only filter for specific MAC address (e.g. `AA:BB:CC:DD:EE:FF`).
>
</details>

<details>
<summary> cs_scan_known_crownstone --verbose [--macFilter filter]</summary>

> This will scan for any Crownstone in your sphere. This requires the keys you set to match those on the Crownstones.
> 
> - Parameters
>   - **verbose**: Optionally show full advertisement, not just a single line summary.
>   - **macFilter**(string): Optionally only filter for specific MAC address (e.g. `AA:BB:CC:DD:EE:FF`).
>
</details>

<details>
<summary> cs_switch_crownstone [--bleAddress address] --switchTo state</summary>

> This will switch a Crownstone in your sphere. This requires the keys you set to match those on the Crownstones.
> 
> - Parameters
>   - **bleAddress**(string): Optionally. The MAC address of the Crownstone that you want to switch (e.g. `AA:BB:CC:DD:EE:FF`). Required if you do not switch via broadcast.
>   - **switchTo**(integer): Set the switch state. Between 0 and 100 is dimming (0 is off, 100 is fully on). Set to 255 to switch to what the "behaviour rules" on the Crownstones want it to be.
>
</details>

<details>
<summary> cs_upload_microapp --bleAddress address --file binaryFile</summary>

> This will upload a microapp.
> 
> - Parameters
>   - **bleAddress**(string): Required MAC address of the Crownstone that you want to upload microapp to (e.g. `AA:BB:CC:DD:EE:FF`).
>   - **file**(string): Required binary file (`.bin`) of the microapp to be uploaded.
>
</details>

<details>
<summary> cs_enable_microapp --bleAddress address</summary>

> This will enable a microapp. Required if a microapp is not yet been enabled or has been disabled.
> 
> - Parameters
>   - **bleAddress**(string): Required MAC address of the Crownstone that you want to upload microapp to (e.g. `AA:BB:CC:DD:EE:FF`).
>
</details>
