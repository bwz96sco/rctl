# PyYAML Documentation

PyYAML is a YAML parser and emitter for Python.

## Installation

Simple install:

```
pip install pyyaml
```

To install from source, download the source package *PyYAML-5.1.tar.gz* and unpack it. Go to the directory *PyYAML-5.1* and run:

```
$ python setup.py install
```

If you want to use LibYAML bindings, which are much faster than the pure Python version, you need to download and install [LibYAML](./LibYAML). Then you may build and install the bindings by executing

```
$ python setup.py --with-libyaml install
```

In order to use [LibYAML](./LibYAML) based parser and emitter, use the classes `CParser` and `CEmitter`. For instance,

```
from import try from import as as except ImportError from import# ... = =# ... = =
```

Note that there are some subtle (but not really significant) differences between pure Python and [LibYAML](./LibYAML) based parsers and emitters.

## Frequently Asked Questions

### Dictionaries without nested collections are not dumped correctly

*Why does*

```
import = """ a: 1 b: c: 3 d: 4 """ print
```

```
a: 1 b: {c: 3, d: 4}
```

*(see #18, #24)?*

It’s a correct output despite the fact that the style of the nested mapping is different.

By default, PyYAML chooses the style of a collection depending on whether it has nested collections. If a collection has nested collections, it will be assigned the block style. Otherwise it will have the flow style.

If you want collections to be always serialized in the block style, set the parameter `default_flow_style` of `dump()` to `False`. For instance,

```
>>> print = False 1 3 4
```

## Python 3 support

Starting from the *3.08* release, PyYAML and LibYAML bindings provide a complete support for Python 3. This is a short outline of differences in PyYAML API between Python 2 and Python 3 versions.

*In Python 2:*

* `str` objects are converted into `!!str`, `!!python/str` or `!binary` nodes depending on whether the object is an ASCII, UTF-8 or binary string.
* `unicode` objects are converted into `!!python/unicode` or `!!str` nodes depending on whether the object is an ASCII string or not.
* `yaml.dump(data)` produces the document as a UTF-8 encoded `str` object.
* `yaml.dump(data, encoding=('utf-8'|'utf-16-be'|'utf-16-le'))` produces a `str` object in the specified encoding.
* `yaml.dump(data, encoding=None)` produces a `unicode` object.

*In Python 3:*

* `str` objects are converted to `!!str` nodes.
* `bytes` objects are converted to `!!binary` nodes.
* For compatibility reasons, `!!python/str` and `!python/unicode` tags are still supported and the corresponding nodes are converted to `str` objects.
* `yaml.dump(data)` produces the document as a `str` object.
* `yaml.dump(data, encoding=('utf-8'|'utf-16-be'|'utf-16-le'))` produces a `bytes` object in the specified encoding.

## Tutorial

Start with importing the `yaml` package.

```
>>> import
```

### Loading YAML

**Warning: It is not safe to call `yaml.load` with any data received from an untrusted source! `yaml.load` is as powerful as `pickle.load` and so may call any Python function.** Check the `yaml.safe_load` function though.

The function `yaml.load` converts a YAML document to a Python object.

```
>>> """... - Hesperiidae... - Papilionidae... - Apatelodidae... - Epiplemidae... """ 'Hesperiidae' 'Papilionidae' 'Apatelodidae' 'Epiplemidae'
```

`yaml.load` accepts a byte string, a Unicode string, an open binary file object, or an open text file object. A byte string or a file must be encoded with *utf-8*, *utf-16-be* or *utf-16-le* encoding. `yaml.load` detects the encoding by checking the *BOM* (byte order mark) sequence at the beginning of the string/file. If no *BOM* is present, the *utf-8* encoding is assumed.

`yaml.load` returns a Python object.

```
>>> u"""... hello: Привет!... """# In Python 3, do not use the 'u' prefix 'hello' u' \u041f\u0440\u0438\u0432\u0435\u0442!'>>> = file'document.yaml' 'r'# 'document.yaml' contains a single YAML document.>>># A Python object corresponding to the document.
```

If a string or a file contains several documents, you may load them all with the `yaml.load_all` function.

```
>>> = """... ---... name: The Set of Gauntlets 'Pauraegen'... description: >... A set of handgear with sparks that crackle... across its knuckleguards.... ---... name: The Set of Gauntlets 'Paurnen'... description: >... A set of gauntlets that gives off a foul,... acrid odour yet remains untarnished.... ---... name: The Set of Gauntlets 'Paurnimmen'... description: >... A set of handgear, freezing with unnatural cold.... """>>> for in print 'description''A set of handgear with sparks that crackle across its knuckleguards. \n ' 'name' "The Set of Gauntlets 'Pauraegen'" 'description''A set of gauntlets that gives off a foul, acrid odour yet remains untarnished. \n ' 'name' "The Set of Gauntlets 'Paurnen'" 'description''A set of handgear, freezing with unnatural cold. \n ' 'name' "The Set of Gauntlets 'Paurnimmen'"
```

PyYAML allows you to construct a Python object of any type.

```
>>> """... none: [~, null]... bool: [true, false, on, off]... int: 42... float: 3.14159... list: [LITE, RES_ACID, SUS_DEXT]... dict: {hp: 13, sp: 5}... """ 'none' None None 'int' 42 'float'3.1415899999999999 'list' 'LITE' 'RES_ACID' 'SUS_DEXT' 'dict' 'hp' 13 'sp' 5 'bool' True False True False
```

Even instances of Python classes can be constructed using the `!!python/object` tag.

```
>>> class def __init__ self self = self = self = def __repr__ self return " %s(name= %r, hp= %r, sp= %r)" % self __name__ self self self>>> """... !!python/object:__main__.Hero... name: Welthyr Syxgon... hp: 1200... sp: 0... """ = 'Welthyr Syxgon' = 1200 = 0
```

Note that the ability to construct an arbitrary Python object may be dangerous if you receive a YAML document from an untrusted source such as the Internet. The function `yaml.safe_load` limits this ability to simple Python objects like integers or lists.

A python object can be marked as safe and thus be recognized by `yaml.safe_load`. To do this, derive it from `yaml.YAMLObject` (as explained in section *Constructors, representers, resolvers*) and explicitly set its class property `yaml_loader` to `yaml.SafeLoader`.

### Dumping YAML

The `yaml.dump` function accepts a Python object and produces a YAML document.

```
>>> print 'name' 'Silenthand Olleander' 'race' 'Human' 'traits' 'ONE_HAND' 'ONE_EYE'
```

`yaml.dump` accepts the second optional argument, which must be an open text or binary file. In this case, `yaml.dump` will write the produced YAML document into the file. Otherwise, `yaml.dump` returns the produced document.

```
>>> = file'document.yaml' 'w'>>># Write a YAML representation of data to 'document.yaml'.>>> print# Output the document to the screen.
```

If you need to dump several YAML documents to a single stream, use the function `yaml.dump_all`. `yaml.dump_all` accepts a list or a generator producing

Python objects to be serialized into a YAML document. The second optional argument is an open file.

```
>>> print 1 2 3 = True --- 1 2 3>>> print 1 2 3 = True --- 1 --- 2 --- 3
```

You may even dump instances of Python classes.

```
>>> class def __init__ self self = self = self = def __repr__ self return " %s(name= %r, hp= %r, sp= %r)" % self __name__ self self self>>> print "Galain Ysseleg" =- 3 = 2!!/ object -3 2
```

`yaml.dump` supports a number of keyword arguments that specify formatting details for the emitter. For instance, you may set the preferred intendation and width, use the canonical YAML format or force preferred style for scalars and collections.

```
>>> print range 50 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49>>> print range 50 = 50 = 4 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49>>> print range 5 = True ---!!!! int "0"!! int "1"!! int "2"!! int "3"!! int "4">>> print range 5 = False - 0 - 1 - 2 - 3 - 4>>> print range 5 = True = '"'!! int "0"!! int "1"!! int "2"!! int "3"!! int "4"
```

### Constructors, representers, resolvers

You may define your own application-specific tags. The easiest way to do it is to define a subclass of `yaml.YAMLObject`:

```
>>> class =u'!Monster' def __init__ self self = self = self = self = def __repr__ self return " %s(name= %r, hp= %r, ac= %r, attacks= %r)" % self __name__ self self self self
```

The above definition is enough to automatically load and dump `Monster` objects:

```
>>> """... --- !Monster... name: Cave spider... hp: [2,6] # 2d6... ac: 16... attacks: [BITE, HURT]... """ = 'Cave spider' = 2 6 = 16 = 'BITE' 'HURT'>>> print = 'Cave lizard' = 3 6 = 16 = 'BITE' 'HURT'! 16 3 6
```

`yaml.YAMLObject` uses metaclass magic to register a constructor, which transforms a YAML node to a class instance, and a representer, which serializes a class instance to a YAML node.

If you don’t want to use metaclasses, you may register your constructors and representers using the functions `yaml.add_constructor` and `yaml.add_representer`. For instance, you may want to add a constructor and a representer for the following `Dice` class:

```
>>> class tuple def __new__ return tuple __new__ def __repr__ self return"Dice(%s, %s)" % self>>> print 3 6 3 6
```

The default representation for `Dice` objects is not pretty:

```
>>> print 3 6!!/ object/ -!!/ tuple 3 6
```

Suppose you want a `Dice` object to represented as `AdB` in YAML:

```
>>> print 3 6
```

First we define a representer that converts a dice object to a scalar node with the tag `!dice`, then we register it.

```
>>> def returnu'!dice' u' %s d %s ' %>>>
```

Now you may dump an instance of the `Dice` object:

```
>>> print 'gold' 10 6! '10d6'
```

Let us add the code to construct a Dice object:

```
>>> def = = map int 'd' return>>>u'!dice'
```

Then you may load a `Dice` object as well:

```
>>> print """... initial hit points: !dice 8d4... """ 'initial hit points' 8 4
```

You might not want to specify the tag `!dice` everywhere. There is a way to teach PyYAML that any untagged plain scalar which looks like XdY has the implicit tag `!dice`. Use `add_implicit_resolver`:

```
>>> import>>> = compiler'^\d+d\d+$'>>>u'!dice'
```

Now you don’t have to specify the tag to define a `Dice` object:

```
>>> print 'treasure' 10 20>>> print """... damage: 5d10... """ 'damage' 5 10
```

## YAML syntax

A good introduction to the YAML syntax is [Chapter 2 of the YAML specification](http://yaml.org/spec/1.1/#id857168).

You may also check [the YAML cookbook](https://yaml.org/YAML_for_ruby.html). Note that it is focused on a Ruby implementation and uses the old YAML 1.0 syntax.

Here we present most common YAML constructs together with the corresponding Python objects.

### Documents

YAML stream is a collection of zero or more documents. An empty stream contains no documents. Documents are separated with `---`. Documents may optionally end with `...`. A single document may or may not be marked with `---`.

Example of an implicit document:

```
- - -
```

Example of an explicit document:

```
--- - - -...
```

Example of several documents in the same stream:

```
--- - - - - - --- - --- - -# # Note that comments are denoted with ' #' (space then #). - -
```

### Block sequences

In the block context, sequence entries are denoted by `-` (dash then space):

```
# YAML - 'Narthanc' - 'Nimthanc' - 'Dethanc'
```

```
# Python "The Dagger 'Narthanc'" "The Dagger 'Nimthanc'" "The Dagger 'Dethanc'"
```

Block sequences can be nested:

```
# YAML - - - - - - - - - - -
```

```
# Python 'HTML' 'LaTeX' 'SGML' 'VRML' 'XML' 'YAML' 'BSD' 'GNU Hurd' 'Linux'
```

It’s not necessary to start a nested sequence with a new line:

```
# YAML -1.1 - -2.1 -2.2 - - -3.1 -3.2 -3.3
```

```
# Python1.12.12.23.13.23.3
```

A block sequence may be nested to a block mapping. Note that in this case it is not necessary to indent the sequence.

```
# YAMLleft hand: - -right hand: - - -
```

```
# Python 'right hand' 'Ring of Resist Fire' 'Ring of Resist Cold' 'Ring of Resist Poison' 'left hand' 'Ring of Teleportation' 'Ring of Speed'
```

### Block mappings

In the block context, keys and values of mappings are separated by `:` (colon then space):

```
# YAMLbase armor class:  0base damage:  [4, 4]plus to-hit:  12plus to-dam:  16plus to-ac:  0
```

```
# Python'plus to-hit' 12 'base damage' 4 4 'base armor class' 0'plus to-ac' 0'plus to-dam' 16
```

Complex keys are denoted with `?` (question mark then space):

```
# YAML ?!!python/tuple[0, 0]:  The Hero ?!!python/tuple[0, 1]:  Treasure ?!!python/tuple[1, 0]:  Treasure ?!!python/tuple[1, 1]:  The Dragon
```

```
# Python 0 1 'Treasure' 1 0 'Treasure' 0 0 'The Hero' 1 1 'The Dragon'
```

Block mapping can be nested:

```
# YAMLhero:hp:  34sp:  8level:  4orc:hp:  12sp:  0level:  2
```

```
# Python 'hero' 'hp' 34 'sp' 8 'level' 4 'orc' 'hp' 12 'sp' 0 'level' 2
```

A block mapping may be nested in a block sequence:

```
# YAML -name:  PyYAMLstatus:  4license:  MITlanguage:  Python -name:  PySyckstatus:  5license:  BSDlanguage:  Python
```

```
# Python 'status' 4 'language' 'Python' 'name' 'PyYAML' 'license' 'MIT' 'status' 5 'license' 'BSD' 'name' 'PySyck' 'language' 'Python'
```

### Flow collections

The syntax of flow collections in YAML is very close to the syntax of list and dictionary constructors in Python:

```
# YAML{str:  [15, 17],con:  [16, 16],dex:  [17, 18],wis:  [16, 16],int:  [10, 13],chr:  [5, 8]  }
```

```
# Python 'dex' 17 18 'int' 10 13 'chr' 5 8 'wis' 16 16 'str' 15 17 'con' 16 16
```

### Scalars

There are 5 styles of scalars in YAML: plain, single-quoted, double-quoted, literal, and folded:

```
# YAMLplain:  Scroll of Remove Cursesingle-quoted:  'EASY_KNOW'double-quoted:  "?"literal: |# Borrowed from http://www.kersbergen.com/flump/religion.htmlfolded:>
```

```
# Python 'plain' 'Scroll of Remove Curse' 'literal' 'by hjw ___ \n '' __ /.-. \\\n '' / )_____________ \\\\  Y \n '' /_ /=== == === === = \\  _ \\ _ \n ''( /)=== == === === == Y \\\n '' `-------------------( o ) \n ' ' \\___/ \n ''single-quoted' 'EASY_KNOW''double-quoted' '?' 'folded''It removes all ordinary curses from all equipped items. Heavy or permanent curses are unaffected. \n '
```

Each style has its own quirks. A plain scalar does not use indicators to denote its start and end, therefore it’s the most restricted style. Its natural applications are names of attributes and parameters.

Using single-quoted scalars, you may express any value that does not contain special characters. No escaping occurs for single quoted scalars except that a pair of adjacent quotes `''` is replaced with a lone single quote `'`.

Double-quoted is the most powerful style and the only style that can express any scalar value. Double-quoted scalars allow *escaping*. Using escaping sequences `\x*` and `\u***`, you may express any ASCII or Unicode character.

There are two kind of block scalar styles: *literal* and *folded*. The literal style is the most suitable style for large block of text such as source code. The folded style is similar to the literal style, but two adjacent non-empty lines are joined to a single line separated by a space character.

### Aliases

~~*Note that PyYAML does not yet support recursive objects.*~~

Using YAML you may represent objects of arbitrary graph-like structures. If you want to refer to the same object from different parts of a document, you need to use anchors and aliases.

Anchors are denoted by the `&` indicator while aliases are denoted by ``. For instance, the document

```
left hand:  &Aname:  The Bastard Sword of Eowynweight:  30right hand:  *A
```

expresses the idea of a hero holding a heavy sword in both hands.

PyYAML now fully supports recursive objects. For instance, the document

```
&A[*A]
```

will produce a list object containing a reference to itself.

### Tags

Tags are used to denote the type of a YAML node. Standard YAML tags are defined at <http://yaml.org/type/index.html>.

Tags may be implicit:

```
boolean:  trueinteger:  3float:  3.14
```

```
'boolean' True 'integer' 3 'float'3.14
```

or explicit:

```
boolean:  !!bool  "true"integer:  !!int  "3"float:  !!float  "3.14"
```

```
'boolean' True 'integer' 3 'float'3.14
```

Plain scalars without explicitly defined tags are subject to implicit tag resolution. The scalar value is checked against a set of regular expressions and if one of them matches, the corresponding tag is assigned to the scalar. PyYAML allows an application to add custom implicit tag resolvers.

## YAML tags and Python types

The following table describes how nodes with different tags are converted to Python objects.

| *YAML tag* | *Python type* |
| --- | --- |
| *Standard YAML tags* |
| `!!null` | `None` |
| `!!bool` | `bool` |
| `!!int` | `int` or `long` (`int` in Python 3) |
| `!!float` | `float` |
| `!!binary` | `str` (`bytes` in Python 3) |
| `!!timestamp` | `datetime.datetime` |
| `!!omap`, `!!pairs` | `list` of pairs |
| `!!set` | `set` |
| `!!str` | `str` or `unicode` (`str` in Python 3) |
| `!!seq` | `list` |
| `!!map` | `dict` |
| *Python-specific tags* |
| `!!python/none` | `None` |
| `!!python/bool` | `bool` |
| `!!python/bytes` | (`bytes` in Python 3) |
| `!!python/str` | `str` (`str` in Python 3) |
| `!!python/unicode` | `unicode` (`str` in Python 3) |
| `!!python/int` | `int` |
| `!!python/long` | `long` (`int` in Python 3) |
| `!!python/float` | `float` |
| `!!python/complex` | `complex` |
| `!!python/list` | `list` |
| `!!python/tuple` | `tuple` |
| `!!python/dict` | `dict` |
| *Complex Python tags* |
| `!!python/name:module.name` | `module.name` |
| `!!python/module:package.module` | `package.module` |
| `!!python/object:module.cls` | `module.cls` instance |
| `!!python/object/new:module.cls` | `module.cls` instance |
| `!!python/object/apply:module.f` | value of `f(...)` |

### String conversion (Python 2 only)

There are four tags that are converted to `str` and `unicode` values: `!!str`, `!!binary`, `!!python/str`, and `!!python/unicode`.

`!!str`-tagged scalars are converted to `str` objects if its value is *ASCII*. Otherwise it is converted to `unicode`. `!!binary`-tagged scalars are converted to `str` objects with its value decoded using the *base64* encoding. `!!python/str` scalars are converted to `str` objects encoded with *utf-8* encoding. `!!python/unicode` scalars are converted to `unicode` objects.

Conversely, a `str` object is converted to 1. a `!!str` scalar if its value is *ASCII*. 2. a `!!python/str` scalar if its value is a correct *utf-8* sequence. 3. a `!!binary` scalar otherwise.

A `unicode` object is converted to 1. a `!!python/unicode` scalar if its value is *ASCII*. 2. a `!!str` scalar otherwise.

### String conversion (Python 3 only)

In Python 3, `str` objects are converted to `!!str` scalars and `bytes` objects to `!!binary` scalars. For compatibility reasons, tags `!!python/str` and `!!python/unicode` are still supported and converted to `str` objects.

### Names and modules

In order to represent static Python objects like functions or classes, you need to use a complex `!!python/name` tag. For instance, the function `yaml.dump` can be represented as

```
!!python/name:yaml.dump
```

Similarly, modules are represented using the tag `!python/module`:

```
!!python/module:yaml
```

### Objects

Any pickleable object can be serialized using the `!!python/object` tag:

```
!!python/object:module.Class{attribute:  value,}
```

In order to support the pickle protocol, two additional forms of the `!!python/object` tag are provided:

```
!!python/object/new:module.Classargs:  [,]kwds:  {key:  value,}state: ...listitems:  [,]dictitems:  [key:  value,]!!python/object/apply:module.functionargs:  [,]kwds:  {key:  value,}state: ...listitems:  [,]dictitems:  [key:  value,]
```

If only the `args` field is non-empty, the above records can be shortened:

```
!!python/object/new:module.Class[,]!!python/object/apply:module.function[,]
```

## Reference

*Warning: API stability is not guaranteed!*

### The yaml package

```
=
```

`scan(stream)` scans the given `stream` and produces a sequence of tokens.

```
= = None = = None = None = None = None = None
```

`parse(stream)` parses the given `stream` and produces a sequence of parsing events.

`emit(events, stream=None)` serializes the given sequence of parsing `events` and writes them to the `stream`. if `stream` is `None`, it returns the produced stream.

```
= = = None = ='utf-8'# encoding=None (Python 3) = None = None = None = None = None = None = None = None = None = None =
```

`compose(stream)` parses the given `stream` and returns the root of the representation graph for the first document in the stream. If there are no documents in the stream, it returns `None`.

`compose_all(stream)` parses the given `stream` and returns a sequence of representation graphs corresponding to the documents in the stream.

`serialize(node, stream=None)` serializes the given representation graph into the `stream`. If `stream` is `None`, it returns the produced stream.

`serialize_all(node, stream=None)` serializes the given sequence of representation graphs into the given `stream`. If `stream` is `None`, it returns the produced stream.

```
= = = None = = None = None ='utf-8'# encoding=None (Python 3) = None = None = None = None = None = None = None = None = None = None = = None = None
```

`load(stream)` parses the given `stream` and returns a Python object constructed from for the first document in the stream. If there are no documents in the stream, it returns `None`.

`load_all(stream)` parses the given `stream` and returns a sequence of Python objects corresponding to the documents in the stream.

`safe_load(stream)` parses the given `stream` and returns a Python object constructed from for the first document in the stream. If there are no documents in the stream, it returns `None`. `safe_load` recognizes only standard YAML tags and cannot construct an arbitrary Python object.

A python object can be marked as safe and thus be recognized by `yaml.safe_load`. To do this, derive it from `yaml.YAMLObject` (as explained in section *Constructors, representers, resolvers*) and explicitly set its class property `yaml_loader` to `yaml.SafeLoader`.

`safe_load_all(stream)` parses the given `stream` and returns a sequence of Python objects corresponding to the documents in the stream. `safe_load_all` recognizes only standard YAML tags and cannot construct an arbitrary Python object.

`dump(data, stream=None)` serializes the given Python object into the `stream`. If `stream` is `None`, it returns the produced stream.

`dump_all(data, stream=None)` serializes the given sequence of Python objects into the given `stream`. If `stream` is `None`, it returns the produced stream. Each object is represented as a YAML document.

`safe_dump(data, stream=None)` serializes the given Python object into the `stream`. If `stream` is `None`, it returns the produced stream. `safe_dump` produces only standard YAML tags and cannot represent an arbitrary Python object.

`safe_dump_all(data, stream=None)` serializes the given sequence of Python objects into the given `stream`. If `stream` is `None`, it returns the produced stream. Each object is represented as a YAML document. `safe_dump_all` produces only standard YAML tags and cannot represent an arbitrary Python object.

```
def# ... return def# ... return = =
```

`add_constructor(tag, constructor)` specifies a `constructor` for the given `tag`. A constructor is a function that converts a node of a YAML representation graph to a native Python object. A constructor accepts an instance of `Loader` and a node and returns a Python object.

`add_multi_constructor(tag_prefix, multi_constructor)` specifies a `multi_constructor` for the given `tag_prefix`. A multi-constructor is a function that converts a node of a YAML representation graph to a native Python object. A multi-constructor accepts an instance of `Loader`, the suffix of the node tag, and a node and returns a Python object.

```
def# ... return def# ... return = =
```

`add_representer(data_type, representer)` specifies a `representer` for Python objects of the given `data_type`. A representer is a function that converts a native Python object to a node of a YAML representation graph. A representer accepts an instance of `Dumper` and an object and returns a node.

`add_multi_representer(base_data_type, multi_representer)` specifies a `multi_representer` for Python objects of the given `base_data_type` or any of its subclasses. A multi-representer is a function that converts a native Python object to a node of a YAML representation graph. A multi-representer accepts an instance of `Dumper` and an object and returns a node.

```
= = = =
```

`add_implicit_resolver(tag, regexp, first)` adds an implicit tag resolver for plain scalars. If the scalar value is matched the given `regexp`, it is assigned the `tag`. `first` is a list of possible initial characters or `None`.

`add_path_resolver(tag, path, kind)` adds a path-based implicit tag resolver. A `path` is a list of keys that form a path to a node in the representation graph. Paths elements can be string values, integers, or `None`. The `kind` of a node can be `str`, `list`, `dict`, or `None`.

### Mark

```
buffer
```

An instance of `Mark` points to a certain position in the input stream. `name` is the name of the stream, for instance it may be the filename if the input stream is a file. `line` and `column` is the line and column of the position (starting from 0). `buffer`, when it is not `None`, is a part of the input stream that contain the position and `pointer` refers to the position in the `buffer`.

### YAMLError

```
YAMLError()
```

If the YAML parser encounters an error condition, it raises an exception which is an instance of `YAMLError` or of its subclass. An application may catch this exception and warn a user.

```
try = file'config.yaml' 'r' except print"Error in configuration file:"
```

An exception produced by the YAML processor may point to the problematic position.

```
>>> try"unbalanced blackets: ][" except if hasattr 'problem_mark' = print"Error position: (%s: %s)" % + 1 + 1 1 22
```

### Tokens

Tokens are produced by a YAML scanner. They are not really useful except for low-level YAML applications such as syntax highlighting.

The PyYAML scanner produces the following types of tokens:

```
# Start of the stream.# End of the stream.# YAML directive, either %YAML or %TAG.# '---'.# '...'.# Start of a new block sequence.# Start of a new block mapping.# End of a block collection.# '['.# '{'.# ']'.# '}'.# Either '?' or start of a simple key.# ':'.# '-'.# ','.# '*value'.# '&value'.# '!value'.# 'value'.
```

`start_mark` and `end_mark` denote the beginning and the end of a token.

Example:

```
>>> = """... ---... block sequence:... - BlockEntryToken... block mapping:... ? KeyToken... : ValueToken... flow sequence: [FlowEntryToken, FlowEntryToken]... flow mapping: {KeyToken: ValueToken}... anchors and tags:... - &A !!int '5'... - *A... ...... """>>> for in print ='utf-8' = True = None = u'block sequence' = True = None = u'BlockEntryToken' = True = None = u'block mapping' = True = None = u'KeyToken' = True = None = u'ValueToken' = True = None = u'flow sequence' = True = None = u'FlowEntryToken' = True = None = u'FlowEntryToken' = True = None = u'flow mapping' = True = None = u'KeyToken' = True = None = u'ValueToken' = True = None = u'anchors and tags' = u'A' =u'!!' u'int' = False = "'" = u'5' = u'A'
```

### Events

Events are used by the low-level Parser and Emitter interfaces, which are similar to the SAX API. While the Parser parses a YAML stream and produces a sequence of events, the Emitter accepts a sequence of events and emits a YAML stream.

The following events are defined:

```
StreamStartEvent(encoding, start_mark, end_mark) StreamEndEvent(start_mark, end_mark) DocumentStartEvent(explicit, version, tags, start_mark, end_mark) DocumentEndEvent(start_mark, end_mark) SequenceStartEvent(anchor, tag, implicit, flow_style, start_mark, end_mark) SequenceEndEvent(start_mark, end_mark) MappingStartEvent(anchor, tag, implicit, flow_style, start_mark, end_mark) MappingEndEvent(start_mark, end_mark) AliasEvent(anchor, start_mark, end_mark) ScalarEvent(anchor, tag, implicit, value, style, start_mark, end_mark)
```

The `flow_style` flag indicates if a collection is block or flow. The possible values are `None`, `True`, `False`. The `style` flag of a scalar event indicates the style of the scalar. Possible values are `None`, `_`, `'\_`, `'"'`, `'|'`, `'>'`. The `implicit` flag of a collection start event indicates if the tag may be omitted when the collection is emitted. The `implicit` flag of a scalar event is a pair of boolean values that indicate if the tag may be omitted when the scalar is emitted in a plain and non-plain style correspondingly.

Example:

```
>>> = """... scalar: &A !!int '5'... alias: *A... sequence: [1, 2, 3]... mapping: [1: one, 2: two, 3: three]... """>>> for in print = None = None = True = None = None = True False = u'scalar' = u'A' =u'tag:yaml.org,2002:int' = False False = u'5' = None = None = True False = u'alias' = u'A' = None = None = True False = u'sequence' = None = None = True = None = None = True False = u'1' = None = None = True False = u'2' = None = None = True False = u'3' = None = None = True False = u'mapping' = None = None = True = None = None = True False = u'1' = None = None = True False = u'one' = None = None = True False = u'2' = None = None = True False = u'two' = None = None = True False = u'3' = None = None = True False = u'three'>>> print ='utf-8' = True = None =u'tag:yaml.org,2002:map' = True = False = None =u'tag:yaml.org,2002:str' = True True = u'agile languages' = None =u'tag:yaml.org,2002:seq' = True = True = None =u'tag:yaml.org,2002:str' = True True = u'Python' = None =u'tag:yaml.org,2002:str' = True True = u'Perl' = None =u'tag:yaml.org,2002:str' = True True = u'Ruby' = True ---
```

### Nodes

Nodes are entities in the YAML informational model. There are three kinds of nodes: *scalar*, *sequence*, and *mapping*. In PyYAML, nodes are produced by Composer and can be serialized to a YAML stream by Serializer.

```
ScalarNode(tag, value, style, start_mark, end_mark) SequenceNode(tag, value, flow_style, start_mark, end_mark) MappingNode(tag, value, flow_style, start_mark, end_mark)
```

The `style` and `flow_style` flags have the same meaning as for events. The value of a scalar node must be a unicode string. The value of a sequence node is a list of nodes. The value of a mapping node is a list of pairs consisting of key and value nodes.

Example:

```
>>> print """... kinds:... - scalar... - sequence... - mapping... """ =u'tag:yaml.org,2002:map' = =u'tag:yaml.org,2002:str' = u'kinds' =u'tag:yaml.org,2002:seq' = =u'tag:yaml.org,2002:str' = u'scalar' =u'tag:yaml.org,2002:str' = u'sequence' =u'tag:yaml.org,2002:str' = u'mapping'>>> print =u'tag:yaml.org,2002:seq' = =u'tag:yaml.org,2002:str' = u'scalar' =u'tag:yaml.org,2002:str' = u'sequence' =u'tag:yaml.org,2002:str' = u'mapping' - - -
```

### Loader

```
# The following classes are available only if you build LibYAML bindings.
```

`Loader(stream)` is the most common of the above classes and should be used in most cases. `stream` is an input YAML stream. It can be a string, a Unicode string, an open file, an open Unicode file.

`Loader` supports all predefined tags and may construct an arbitrary Python object. Therefore it is not safe to use `Loader` to load a document received from an untrusted source. By default, the functions `scan`, `parse`, `compose`, `construct`, and others use `Loader`.

`SafeLoader(stream)` supports only standard YAML tags and thus it does not construct class instances and probably safe to use with documents received from an untrusted source. The functions `safe_load` and `safe_load_all` use `SafeLoader` to parse a stream.

`BaseLoader(stream)` does not resolve or support any tags and construct only basic Python objects: lists, dictionaries and Unicode strings.

`CLoader`, `CSafeLoader`, `CBaseLoader` are versions of the above classes written in C using the <LibYAML> library.

```
*
```

`Loader.check_token(*TokenClasses)` returns `True` if the next token in the stream is an instance of one of the given `TokenClasses`. Otherwise it returns `False`.

`Loader.peek_token()` returns the next token in the stream, but does not remove it from the internal token queue. The function returns `None` at the end of the stream.

`Loader.get_token()` returns the next token in the stream and removes it from the internal token queue. The function returns `None` at the end of the stream.

```
*
```

`Loader.check_event(*EventClasses)` returns `True` if the next event in the stream is an instance of one of the given `EventClasses`. Otherwise it returns `False`.

`Loader.peek_event()` returns the next event in the stream, but does not remove it from the internal event queue. The function returns `None` at the end of the stream.

`Loader.get_event()` returns the next event in the stream and removes it from the internal event queue. The function returns `None` at the end of the stream.

```
Loader.check_node() Loader.get_node()
```

`Loader.check_node()` returns `True` is there are more documents available in the stream. Otherwise it returns `False`.

`Loader.get_node()` construct the representation graph of the next document in the stream and returns its root node.

```
# Loader.add_constructor is a class method.# Loader.add_multi_constructor is a class method.
```

`Loader.check_data()` returns `True` is there are more documents available in the stream. Otherwise it returns `False`.

`Loader.get_data()` constructs and returns a Python object corresponding to the next document in the stream.

`Loader.add_constructor(tag, constructor)`: see `add_constructor`.

`Loader.add_multi_constructor(tag_prefix, multi_constructor)`: see `add_multi_constructor`.

`Loader.construct_scalar(node)` checks that the given `node` is a scalar and returns its value. This function is intended to be used in constructors.

`Loader.construct_sequence(node)` checks that the given `node` is a sequence and returns a list of Python objects corresponding to the node items. This function is intended to be used in constructors.

`Loader.construct_mapping(node)` checks that the given `node` is a mapping and returns a dictionary of Python objects corresponding to the node keys and values. This function is intended to be used in constructors.

```
# Loader.add_implicit_resolver is a class method.# Loader.add_path_resolver is a class method.
```

`Loader.add_implicit_resolver(tag, regexp, first)`: see `add_implicit_resolver`.

`Loader.add_path_resolver(tag, path, kind)`: see `add_path_resolver`.

### Dumper

```
= None = None = None = None = None = None = None = None = None = None = None = None# The following classes are available only if you build LibYAML bindings.
```

`Dumper(stream)` is the most common of the above classes and should be used in most cases. `stream` is an output YAML stream. It can be an open file or an open Unicode file.

`Dumper` supports all predefined tags and may represent an arbitrary Python object. Therefore it may produce a document that cannot be loaded by other YAML processors. By default, the functions `emit`, `serialize`, `dump`, and others use `Dumper`.

`SafeDumper(stream)` produces only standard YAML tags and thus cannot represent class instances and probably more compatible with other YAML processors. The functions `safe_dump` and `safe_dump_all` use `SafeDumper` to produce a YAML document.

`BaseDumper(stream)` does not support any tags and is useful only for subclassing.

`CDumper`, `CSafeDumper`, `CBaseDumper` are versions of the above classes written in C using the <LibYAML> library.

`Dumper.emit(event)` serializes the given `event` and writes it to the output stream.

`Dumper.open()` emits `StreamStartEvent`.

`Dumper.serialize(node)` serializes the given representation graph into the output stream.

`Dumper.close()` emits `StreamEndEvent`.

```
# Dumper.add_representer is a class method.# Dumper.add_multi_representer is a class method. = None = None = None
```

`Dumper.represent(data)` serializes the given Python object to the output YAML stream.

`Dumper.add_representer(data_type, representer)`: see `add_representer`.

`Dumper.add_multi_representer(base_data_type, multi_representer)`: see `add_multi_representer`.

`Dumper.represent_scalar(tag, value, style=None)` returns a scalar node with the given `tag`, `value`, and `style`. This function is intended to be used in representers.

`Dumper.represent_sequence(tag, sequence, flow_style=None)` return a sequence node with the given `tag` and subnodes generated from the items of the given `sequence`.

`Dumper.represent_mapping(tag, mapping, flow_style=None)` return a mapping node with the given `tag` and subnodes generated from the keys and values of the given `mapping`.

```
# Dumper.add_implicit_resolver is a class method.# Dumper.add_path_resolver is a class method.
```

`Dumper.add_implicit_resolver(tag, regexp, first)`: see `add_implicit_resolver`.

`Dumper.add_path_resolver(tag, path, kind)`: see `add_path_resolver`.

### YAMLObject

```
class = = =u'...' = @classmethod def# ... return @classmethod def# ... return
```

Subclassing `YAMLObject` is an easy way to define tags, constructors, and representers for your classes. You only need to override the `yaml_tag` attribute. If you want to define your custom constructor and representer, redefine the `from_yaml` and `to_yaml` method correspondingly.

## Deviations from the specification

*need to update this section*

* rules for tabs in YAML are confusing. We are close, but not there yet. Perhaps both the spec and the parser should be fixed. Anyway, the best rule for tabs in YAML is to not use them at all.
* Byte order mark. The initial BOM is stripped, but BOMs inside the stream are considered as parts of the content. It can be fixed, but it’s not really important now.
* ~~Empty plain scalars are not allowed if alias or tag is specified.~~ This is done to prevent anomalities like *[ !tag, value]*, which can be interpreted both as *[ ! value ]* and *[ ! "“,”value" ]*. The spec should be fixed.
* Indentation of flow collections. The spec requires them to be indented more than their block parent node. Unfortunately this rule renders many intuitively correct constructs invalid, for instance,

  ```
   block: { } # this is indentation violation according to the spec.
  ```
* ‘:’ is not allowed for plain scalars in the flow mode. ~~*{1:2}* is interpreted as *{ 1 : 2 }*.~~
 
