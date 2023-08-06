.. _asyncio:

Asyncio (Why it is not supported)
=================================

From time-to-time a new GitHub issue will appear in which someone asks whether
Peewee supports (or will support) ``asyncio``. This document sets out to
explain my own reasoning about why Peewee does **not** suport asyncio.

Asyncio is Python's new standard mechanism for writing cooperatively-scheduled
asynchronous code. It works by leveraging Python generators to switch contexts
when an I/O operation would block. This is done explicitly in Python using the
``async/await`` syntax. This design requires that, at any place in the
application stack, the Python code yields when doing I/O. As a result, many
libraries must be written specifically with asyncio in mind. See this excellent
blog post for a description of some of the problems with this:
`What Color is your Function? <https://journal.stuffwithstuff.com/2015/02/01/what-color-is-your-function/>`_.

A better, more Pythonic, approach (in my opinion) is to use `gevent <https://www.gevent.org/>`_.
Gevent works by monkey-patching the blocking APIs at the source so that,
whenever an IO operation is performed, the green-thread yields control back to
the event loop automatically. The best part is that your application code,
libraries, etc., do not need to make **any** change to become async-friendly.
Furthermore, by avoiding the many layers of the asyncio abstractions, gevent is
likely to offer better performance. I have used gevent extensively for years
and have found it remarkably performant and stable.

Besides the difficulties with libraries and at the language-level, my opinion
is that database traffic is a bad fit for asyncio's primary use-case (large
numbers of slow connections). Mike Bayer, the author of SQLAlchemy, has written
an excellent blog post on asyncio and databases: `Asynchronous Python and Databases <https://techspot.zzzeek.org/2015/02/15/asynchronous-python-and-databases/>`_.
In the post, he
