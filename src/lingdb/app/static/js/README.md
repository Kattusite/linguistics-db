Some properties I would like to rewrite front.js to have:

The key/value pairs needed for a div to send a query are all listed as attributes of that query div. This makes them easier to find.

The queries are checked for validity (by reading an isValid attr) before sending to server

The js for the 3-4 different handler types is modularized and dramaticalyl condensed

The js for equality checking (<= >= < > != ==) is scrapped and all made into python
