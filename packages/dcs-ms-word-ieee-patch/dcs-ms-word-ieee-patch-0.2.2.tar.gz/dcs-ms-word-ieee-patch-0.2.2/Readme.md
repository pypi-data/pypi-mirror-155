# Microsoft Word IEEE Citation Patcher

Post-processing script that patches IEEE citation format in [Microsoft Word][ms-word] documents in the [docx format][docx-format].

Word does only allow to list citations one by one and has no integrated logic to group or sort them.
Especially in scientific documents it is often the case that multiple citations are added to the same paragraphs and it is likely that they are not in order.
Sorting and grouping citation references is a tedious task, so this script is here to help.

An original text like this

> as shown by Brown [5], [4]; as mentioned earlier [9], [4], [5], [2], [7], [6]; Smith [4] and Brown and Jones [5]; Wood et al. [7]

is transformed to this

> as shown by Brown [4], [5]; as mentioned earlier [2], [4]-[7], [9]; Smith [4] and Brown and Jones [5]; Wood et al. [7]

or with an optional compression option to this

> as shown by Brown [4,5]; as mentioned earlier [2,4-7,9]; Smith [4] and Brown and Jones [5]; Wood et al. [7]


## Installation

Python >= 3.8 is required for this tool to work.
The package is hosted on [PyPI].

To install with pip, use the following command:

```console
$ pip install dcs-ms-word-ieee-patch
```

This installs two CLI scripts, `ieee-patch` and `xml-pretty-print`.

## Usage

Run the script with the path to the 

```console
$ ieee-patch /path/to/file.docx                 # on unix
$ ieee-patch C:\Users\foobar\Desktop\file.docx  # on windows
```

The script by default creates a file with the filename suffix `.patched` in the same folder as the original file and patches the content within this file which means the original file is left untouched.

In case the replacement should be done in-place, e.g., when space limitations apply, use the `--overwrite` CLI flag.
**Please use this flag only if really necessary, since the original content cannot be restored after is has been overwritten!**

# Legal notice

This project is not affiliated, associated, authorized, endorsed by, or in any way officially connected with the Microsoft Corporation, or any of its subsidiaries or its affiliates.


[ms-word]: https://products.office.com/en-us/word
[docx-format]: https://docs.microsoft.com/en-us/openspecs/office_standards/ms-docx/b839fe1f-e1ca-4fa6-8c26-5954d0abbccd
[PyPI]: https://pypi.org/project/dcs-ms-word-ieee-patch/