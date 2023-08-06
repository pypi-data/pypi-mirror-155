Arthur SDK Python API Reference
===============================

This page contains the complete Python API reference for Arthur's SDK. For guides and concepts, see
`our main docs <https://docs.arthur.ai>`_.


Essentials
~~~~~~~~~~
There are a few touch points that are most commonly needed in the SDK. These are:

- The :class:`ArthurAI <arthurai.client.client.ArthurAI>` client to create a connection to Arthur
    - Its :meth:`ArthurAI.model() <arthurai.client.client.ArthurAI.model>` method to create a new (empty) model
    - Its :meth:`ArthurAI.get_model() <arthurai.client.client.ArthurAI.get_model>` to fetch an existing model already registered with Arthur
- The :class:`ArthurModel <arthurai.core.models.ArthurModel>` class (returned by both of the above methods) to interact with a particular model
    - Its :meth:`ArthurModel.build() <arthurai.core.models.ArthurModel.build>` method to construct a new model from a DataFrame
    - Its :meth:`ArthurModel.save() <arthurai.core.models.ArthurModel.save>` method to register a model with the Arthur platform


Contents
~~~~~~~~

.. toctree::
   :maxdepth: 2

   Arthur Docs <https://docs.arthur.ai>
   SDK Home <self>
   Permissions by Function <permissions>
   apiref/arthurai

Indices
~~~~~~~

* :ref:`genindex`
* :ref:`modindex`
