===============
Getting Started
===============
This page assumes you have already `created your Coiled account <https://cloud.coiled.io/login>`_
and followed the step-by-step guide to configure your :doc:`AWS <aws_configure>` or
:doc:`GCP <gcp_configure>` account to run Coiled clusters.

In this guide you will:

#. Install Coiled
#. Setup your Coiled account
#. Run your first computation

1. Install
----------

.. raw:: html

    <script src="https://fast.wistia.com/embed/medias/6tv2je5v29.jsonp" async></script><script src="https://fast.wistia.com/assets/external/E-v1.js" async></script><div class="wistia_responsive_padding" style="padding:56.25% 0 0 0;position:relative;"><div class="wistia_responsive_wrapper" style="height:100%;left:0;position:absolute;top:0;width:100%;"><div class="wistia_embed wistia_async_6tv2je5v29 videoFoam=true" style="height:100%;position:relative;width:100%"><div class="wistia_swatch" style="height:100%;left:0;opacity:0;overflow:hidden;position:absolute;top:0;transition:opacity 200ms;width:100%;"><img src="https://fast.wistia.com/embed/medias/6tv2je5v29/swatch" style="filter:blur(5px);height:100%;object-fit:contain;width:100%;" alt="" aria-hidden="true" onload="this.parentNode.style.opacity=1;" /></div></div></div></div>

|

Coiled can be installed from PyPI using ``pip`` or from the conda-forge channel
using ``conda``:

.. panels::
    :body: text-center
    :header: text-center h5 bg-white

    Install with pip
    ^^^^^^^^^^^^^^^^

    .. code-block:: bash

        pip install coiled

    ---

    Install with conda
    ^^^^^^^^^^^^^^^^^^

    .. code-block:: bash

        conda install -c conda-forge coiled
        
.. _coiled-setup:

2. Setup
--------

.. raw:: html

    <script src="https://fast.wistia.com/embed/medias/04blcgav4s.jsonp" async></script><script src="https://fast.wistia.com/assets/external/E-v1.js" async></script><div class="wistia_responsive_padding" style="padding:56.25% 0 0 0;position:relative;"><div class="wistia_responsive_wrapper" style="height:100%;left:0;position:absolute;top:0;width:100%;"><div class="wistia_embed wistia_async_04blcgav4s videoFoam=true" style="height:100%;position:relative;width:100%"><div class="wistia_swatch" style="height:100%;left:0;opacity:0;overflow:hidden;position:absolute;top:0;transition:opacity 200ms;width:100%;"><img src="https://fast.wistia.com/embed/medias/04blcgav4s/swatch" style="filter:blur(5px);height:100%;object-fit:contain;width:100%;" alt="" aria-hidden="true" onload="this.parentNode.style.opacity=1;" /></div></div></div></div>

|

You can then configure your account credentials using the ``coiled login``
command line tool. From the command line enter:

.. code-block:: bash

    $ coiled login

You'll then be asked to login to the Coiled web interface, and navigate to 
https://cloud.coiled.io/profile where you can create and manage API tokens.

.. code-block:: bash

    Please login to https://cloud.coiled.io/profile to get your token
    Token:

Your token will be saved to :doc:`Coiled's local configuration file <configuration>`.

.. note:: **For Windows users**
    
    Unless you are using WSL, you will need to go to a command 
    prompt or PowerShell window within an environment
    that includes coiled (see the next step) to login via ``coiled login``.
    
    Additionally, users users should provide the token as an argument, i.e.
    ``coiled login --token <your-token>`` from the command line or
    ``!coiled login --token <your-token>`` from a Jupyter notebook, since
    the Windows clipboard will not be active at the "Token" prompt.

.. _first-computation:

3. Run your first computation
-----------------------------

.. raw:: html

    <script src="https://fast.wistia.com/embed/medias/qscpe0cicc.jsonp" async></script><script src="https://fast.wistia.com/assets/external/E-v1.js" async></script><div class="wistia_responsive_padding" style="padding:56.25% 0 0 0;position:relative;"><div class="wistia_responsive_wrapper" style="height:100%;left:0;position:absolute;top:0;width:100%;"><div class="wistia_embed wistia_async_qscpe0cicc videoFoam=true" style="height:100%;position:relative;width:100%"><div class="wistia_swatch" style="height:100%;left:0;opacity:0;overflow:hidden;position:absolute;top:0;transition:opacity 200ms;width:100%;"><img src="https://fast.wistia.com/embed/medias/qscpe0cicc/swatch" style="filter:blur(5px);height:100%;object-fit:contain;width:100%;" alt="" aria-hidden="true" onload="this.parentNode.style.opacity=1;" /></div></div></div></div>

|

When performing computations on remote Dask clusters, it's important to have the
same libraries installed both in your local Python environment (e.g. on your
laptop), as well as on the remote Dask workers in your cluster.

Coiled helps you seamlessly synchronize these software environments
(see :doc:`tutorials/matching_coiled_senvs`). For now, we'll do this
from the command line, relying on the :ref:`coiled-runtime metapackage <coiled-runtime>`.

The snippet below creates a local conda environment named
"coiled-default-py39", activates it, and launches an IPython session:

.. code-block:: bash

    $ conda create -n coiled-default-py39 python=3.9 coiled-runtime -c conda-forge
    $ conda activate coiled-default-py39
    $ ipython

Now that you have Coiled installed and setup, you can run a Dask computation.
Start by spinning up a remote Dask cluster by creating a :class:`coiled.Cluster` instance
and connecting this cluster to the Dask ``Client``:

.. code-block:: python

    from coiled import Cluster
    from dask.distributed import Client

    # create a remote Dask cluster with Coiled
    cluster = Cluster(software="coiled/default-py39")

    # interact with Coiled using the Dask distributed client
    client = Client(cluster)

    # link to Dask Dashboard
    print("Dask Dashboard:", client.dashboard_link)


.. note::
   If you're using a :doc:`Team account <teams>`, be sure to specify
   the ``account=`` option when creating a cluster:

   .. code-block:: python

      cluster = coiled.Cluster(account="<my-team-account-name>")

   Otherwise, the cluster will be created in your personal Coiled account.

You will then see a widget showing the cluster state overview and
progress bars as resources are provisioned (this may take a minute or two).
You can use the cluster details page (link at the top of the widget) for detailed information on cluster state and worker logs (see :doc:`logging`).

.. figure:: images/widget-gif.gif
   :alt: Terminal dashboard displaying the Coiled cluster status overview, configuration, and Dask worker states.

Once the cluster is ready, you can submit a Dask DataFrame computation for execution. Navigate to the `Dask dashboard <https://docs.dask.org/en/stable/dashboard.html>`_ (see ``Dashboard Address`` in the widget) for real-time diagnostics on your Dask computations.

.. code-block:: python

    import dask.dataframe as dd

    # read in parquet dataset
    df = dd.read_parquet(
        "s3://nyc-tlc/trip data/yellow_tripdata_2019-*.parquet",
        columns=["passenger_count", "tip_amount"],
        storage_options={"anon": True},
    ).persist()

    # perform a groupby with an aggregation
    df.groupby("passenger_count").tip_amount.mean().compute()

Lastly, you can stop the running cluster using the following commands.
By default, clusters will shutdown after 20 minutes of inactivity (see :doc:`cluster_management`).

.. code-block:: python

    # Close the cluster
    cluster.close()

    # Close the client
    client.close()


