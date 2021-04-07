# One-Handed Stenotype

A Plover plugin implementing a one-handed Stenotype layout.
Requires Plover v4.0.0.dev8 or later.

Credit goes to Soffit and Kaoffie on the
[Plover Discord](https://discord.me/plover) for coming up with the idea
and proposing possible implementations.

## Installation

1. Clone this repository:

    ```
    git clone https://github.com/jenchanws/plover-one-handed.git
    ```

2. Install it locally to Plover's environment:

    ```
    /path/to/Plover -s plover_plugins install -e plover-one-handed
    ```

3. Go to Configure &rarr; Plugins and enable the `one_handed` extension.

4. Go to Configure &rarr; System and switch to the `One-Handed Stenotype` system.

## Usage

By default, the following keys are used on the one-handed layout:

```
┌───┬───┬───┬───┬───┐
│ 1 │ 2 │ 3 │ 4 │ 5 │
└┬──┴┬──┴┬──┴┬──┴┬──┴┬───┐
 │ Q │ W │ E │ R │ T │ Y │
 └───┴───┴───┴┬──┴┬──┴┬──┴┐
              │ F │ G │ H │
              └───┴┬──┴┬──┴┬───┐
                   │ B │ N │ M │
                   └───┴───┴───┘
```

The keys are mapped to the two sides of the standard Stenotype layout as follows:

```
┌───┬───┬───┬───┬───┐
│ S │ T │ P │ H │ * │
└┬──┴┬──┴┬──┴┬──┴┬──┴┬───┐
 │ S │ K │ W │ R │ * │ A │
 └───┴───┴───┴┬──┴┬──┴┬──┴┐
              │ # │ U │ O │
              └───┴┬──┴┬──┴┬───┐
                   │ E │ l │ r │
                   └───┴───┴───┘
```

```
┌───┬───┬───┬───┬───┐
│ F │ P │ L │ T │ D │
└┬──┴┬──┴┬──┴┬──┴┬──┴┬───┐
 │ R │ B │ G │ S │ Z │ A │
 └───┴───┴───┴┬──┴┬──┴┬──┴┐
              │ # │ U │ O │
              └───┴┬──┴┬──┴┬───┐
                   │ E │ l │ r │
                   └───┴───┴───┘
```

* To stroke an outline on **only the left side** of the keyboard, stroke `l`
  and the remainder of the keys. For example, 'this' is stroked as `lTH-`, and
  'have' is `lSR-`.

* To stroke an outline on **only the right side** of the keyboard, stroke `r`
  and the remainder of the keys. For example, 'of the' is stroked as `r-FT`, and
  'being' is `r-BG`.

* To stroke an outline on **both sides** of the keyboard, stroke the left side
  first then the right side. For example, 'example' (`KP-L`) is stroked as
  `KP-/-L`. The plugin interprets the strokes as two halves of the same outline.

Vowels and the number key can be stroked on either side.
