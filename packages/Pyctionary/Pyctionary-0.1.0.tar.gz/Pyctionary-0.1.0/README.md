## Pyctionary!

*   **Project description**

`Pyctionary` is a dictionary that provides a free API to find word meanings, synonyms, and detect word language. (More is coming :) )

_This Module uses BS4 and requests as dependencies_

*   **Installation**

```plaintext
 pip install Pyctionary
```

*   **Usage**

```plaintext
 from pyctionary import Pictionary
 Pyctio=Pictionary()
```

*   **Synonyms :**

This method is used to get synonyms of a list of words and it returns a python dictionary of words and their synonyms.

```plaintext
Pyctio.synoyms(["help"],max_synonyms=5)
```

*   **Definition:**

You can get the definition of English words with:

```plaintext
Pyctio.define("laughter")
```

*   **Language:**

Return a python dictionary, country language and language code (eg. EN-GB)

```plaintext
Pyctio.language("Hola")
```

_About:_

Made by M'GHARI Tariq 2022.