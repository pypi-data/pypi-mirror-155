# Colorido

Colors for Terminal without weird code.


## Description

Colorido is a small Python 3.x lib to speed up the text coloring throughout
your Python projects. You ever can make your logs prettier. ;)

You don't need to install any dependency to use colorido. In a nutshell, just
import the `color` module from the `colorido` package and call the functions
in a print context to start coloring your strings.


## Installation

Install it with pip by running:

``` Shell
pip install colorido
```


## Usage

To use the colorido abilities, import the `color` module in your code and just
call the function with the color you want to print. See how in the example
below:

``` Python
from colorido import color

print('This is the color ' + color.red('red') + '.')
```


### Coloring

You can choose the color you want among the eight available color options. The
supported options are:

| Text color   | Function       |
| ------------ | -------------- |
| Black        | `black(str)`   |
| Blue         | `blue(str)`    |
| Cyan         | `cyan(str)`    |
| Green        | `green(str)`   |
| Magenta      | `magenta(str)` |
| Red          | `red(str)`     |
| White        | `white(str)`   |
| Yellow       | `yellow(str)`  |

> ℹ️ **Note:** the visual colors may vary according with the configuration of
your Terminal or system.


#### Basic examples

Below we have some examples of colorido's general usage.

Example 1:

``` Python
from colorido import color

text = color.green('BR') + color.yellow('AZ') + color.blue('IL')
print('Come to visit %s.' % text)
```

Example 2:

``` Python
from colorido import color

print(f'sudo {color.red("rm -rf /")}')
```

Example 3:
``` Python
from colorido import color

print(
    'Is zebra {black} with {white} stripes or {white} with {black} stripes?'.format(
        black=color.black('BLACK'),
        white=color.white('WHITE'),
    )
)
```


### Styling

Colorido also support text styling. The styles modify the heavy of the text.
The supported styles are:

- Dim text
- Normal text
- Bold text

You can style your text by passing an extra optional `style` parameter to the
color functions. For example, to get a bold red text, you can do:

Example 4:

``` Python
from colorido import color

print(color.red('STOP', style='bold'), 'deploys at friday!')
```

You can also omit the `style` keyword and pass the style parameter just like a
positional parameter.

Example 5:

``` Python
from colorido import color

print(color.magenta('Dimmed', 'dim'), 'texts are calm.')
```

Colorido supports three types of text styling.

| Text style | Parameter                     |
| ---------- | ----------------------------- |
| Dim        | `'d'` or `'dim'`              |
| Normal     | `'n'` or `'normal'` (default) |
| Bold       | `'b'` or `'bold'`             |

If you don't want to color your text, you can use the `font()` function to skip
the text coloring. For this, provide the desired style parameter just like you
do in the coloring functions. See how:

Example 6:

``` Python
from colorido import color

print(
    '{I} {love} {linux}.'.format(
        I=color.font('I', 'bold'),
        love=color.red('<3', 'bold'),
        linux=color.font('Linux', 'dim'),
    )
)
```

### Background color

> New in version 1.0.0!

You can also color the background of your logs! Just provide a `bg` parameter
to any color function with the name of the color you want.

Example 7:

``` Python
from colorido import color

print(
    'The sun rules the {day} and the moon rules the {night}.'.format(
        day=color.yellow('day', bg='white'),
        night=color.blue('night', bg='black'),
    )
)
```

The available background colors are the same eight available in the foreground
text colors. Below you have a list with the color options:

| Background color | Parameter   |
| ---------------- | ----------- |
| Black            | `'black'`   |
| Blue             | `'blue'`    |
| Cyan             | `'cyan'`    |
| Green            | `'green'`   |
| Magenta          | `'magenta'` |
| Red              | `'red'`     |
| White            | `'white'`   |
| Yellow           | `'yellow'`  |


If you want to use just the background color, with no foreground text color,
you can call again the `font()` function, providing the `bg` parameter. For
example:

Example 8:

``` Python
from colorido import color

print(
    'If your {code} have many {bugs}, you propably need more {coffee}.'.format(
        code=color.font('code', bg='blue'),
        bugs=color.font('bugs', bg='red'),
        coffee=color.font('coffee', bg='black'),
    )
)
```

You can also style your text while you choose your background color, just like we
have done in [styling section](#styling). See an example:

Example 9:

``` Python
from colorido import color

print(
    'The {white} {light} can split in a beautiful {ra}{i}{n}{b}{o}{w}.'.format(
        # We can style and also background our text with font() function
        white=color.font('white', 'bold', bg='white'),
        light=color.font('light', 'bold', bg='black'),
        ra=color.red('ra'),
        i=color.yellow('i'),
        n=color.green('n'),
        b=color.cyan('b'),
        o=color.blue('o'),
        w=color.magenta('w'),
    )
)
```

That's all folks! Bugs, questions or coffees, feel free to reach me in my [e-mail](mailto:italo.ramon.campos@gmail.com).


## Who is this lib for?

Colorido is addressed to anyone who wants a simple lib to print colored
texts in the screen without a hundred of things to learn. You just need to
import the module and call the functions you want to.

Colorido doesn't match programmers that want a full-featured lib. It just
returns colored texts to be printed in the screen. No things more. If this is not
your vibe, consider search for other python libraries (like colorama, colored or
PyColor).


## License

This lib is a free software and is distributed under the [MIT License](https://opensource.org/licenses/MIT).
