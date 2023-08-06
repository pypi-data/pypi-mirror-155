# ustick
Ustick is a cli tool to create, store, and formatted display your console stickers.
It stores stickers as data in ~/.notes file and show formatted data to you.
Stickers are limited in size, if you get over it - you'll know.

## Installation
Use pip to install the package:
```
pip install ustick
```
or clone the repository and run pip3:
```
git clone https://github.com/hexpizza/ustick.git
cd ustick
pip3 install ./
```

## Usage
To add sticker run:
```
ustick -a 'My first note to feed my cat at 09.00am'
```
To show stickers run 'ustick' or 'ustick -s':
```
ustick                                             
/=#3792================\
|My first note to feed |
|my cat at 09.00am     |
|                      |
|                      |
\======================/
```
There is a mechanism to find stickers with a keyword, which can be word, phrase or sticker ID. if it's in one of the stickers, the sticker will be shown to you with a coloured pard which you required:
```
ustick -f 'my cat'                                 
```

To remove all the stickers you can run and apply your choise:
```
ustick --remove-all
Are you sure to remove all notes? (yes/no): yes
```