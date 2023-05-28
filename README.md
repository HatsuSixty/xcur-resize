# xcur-resize

Resize a cursor theme.

## Usage

By default, the script will resize the cursors to 75% of its original size. In order to run the script, you will need to have `xcur2png`, `xcursorgen` and `mogrify` available in your `$PATH`.

```console
$ ./xcur-resize.py <path-to-folder-containing-cursors>
```

If you want to change the geometry of the cursors, you can provide it in the ImageMagick geometry format (NNNNxNNNN or NN%) as an extra argument.
