# hu_porthu

EPG source: port.hu

## Usage

### First run

At the first run, it must be run with the `--configure` parameter.
By default, the configuration file saved in the `.xmltv` folder of the home directory. This can be changed with the `--config-file` parameter.

```
tv_grab_pyepg_hu_porthu --configure
```

A fresh channel list is downloaded each configuration run, if a configuration file already contains a channel selection, this selection will be used by default.

After the configuring is done the grabber can be run with the [standard XMLTV parameters](../../../README.md#standard_xmltv_parameters) to download the EPG. To see the progress add the `--verbose` parameter to the command.

Example to download the EPG for tomorrow, show the progress and save the EPG in the current directory:

```
tv_grab_pyepg_hu_porthu --days 1 --offset 1 --verbose --output tomorrow_epg.xml
```

Additional parameters are documented in the `--help` of the grabber and some of them below.

### Extra functionality

To download a more detailed EPG (descriptions, actors, etc...) the `--slow` parameter can be used. This significantly slows down the downloading progress, because these details must be downloaded for each program separately.

To tune the performance, the `--jobs`, `--ratelimit` and `--interval` parameters are available. The default is 1 job, and 1 request per second. The formula to calculate the target requests per seconds value is below.

```
req/sec = jobs * ( ratelimit / interval )
```

Be thoughtful while changing these parameters, setting a too high limit may cause to be banned from the site.