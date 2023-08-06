# invesyservertools

A small set of useful tools an a server, especially for terminal scripts.

Why "invesy"? Invesy (from German **In**halts**ve**rwaltungs**sy**stem == content management system) is a closed source cms I created with Thomas Macher. It's only used in-house, that's why we didn't bother making it open source.


# What's in the box?
## interactive_tools
- **wait\_for\_key**: Wait for a pressed key to continue.

## print_tools
- **and_list**: human-readable list like `a, 1, 2 and something`
- **indent**: get an indentation string
- **print_**: Enhanced print function, specially enhanced for printing in the terminal and into log files.
- **format_filesize**: return a human-readable filesize, like `31.9 GiB`.

## system_tools
- **get_username**: get the username in the operating system
- **get\_home\_dir**
- **find\_file\_with\_path**: provide a filename and a start path to begin searching recursively, get the complete path including the filename