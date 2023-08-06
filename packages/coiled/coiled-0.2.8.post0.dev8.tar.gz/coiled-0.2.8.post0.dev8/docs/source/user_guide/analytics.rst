=========
Analytics
=========

*Measurement is the foundation of performance.*

Coiled Analytics lets you track Dask usage wherever Dask is run.

.. toctree::
   :maxdepth: 1
   :hidden:

   analytics-install
   analytics-privacy
   analytics-api

Motivation
----------

When running computations we often ask ourselves questions like the following:

-   Did my computation finish?
-   Did any exceptions occur?
-   How much did that cost me?
-   What is taking most of the time?
-   Why is that cluster still running?

Experienced users know that Dask presents answers to these questions visually
through the Dask dashboard.  However, the Dask dashboard only tracks the
real-time performance of a single Dask cluster.  Coiled extends Dask by
tracking many Dask clusters across many users and storing those results over
time for later analysis.  Coiled analytics provides a team-wide view of all
clusters over time.

Getting Started
---------------

Coiled Infrastructure
^^^^^^^^^^^^^^^^^^^^^

If you are launching clusters though Coiled then this is already set up for
you.

Your own infrastructure
^^^^^^^^^^^^^^^^^^^^^^^

You can use Coiled analytics on clusters that you manage yourself outside of
the Coiled platform.  See :doc:`analytics-install`

What information does Coiled Track?
-----------------------------------

Coiled tracks aggregate information about cluster activity including the
following:

-   Basic level statistics

    -   Number of active workers and worker threads
    -   Amount of used and total memory
    -   Software versions of common libraries

-   Performance statistics

    -   Task information, including names, numbers, and compute and transfer durations
    -   Profiling, including which functions and lines of code take the most time
    -   Code snippets surrounding the Dask calls
    -   How long has it been since any work was completed

-   Error tracking

    -   Every user-level exception
    -   Every dask-level exception

-   User-level tracking

    -   Which user within an account created the cluster
    -   Costs (estimated when run on non-Coiled architecture)
    -   Idleness

This is described in more detail at :doc:`analytics-privacy`

User Access
-----------

Everyone within the same account can view all analytics for this account.
This is especially valuable in two situations:

-   Team leaders and managers can have a single view over all Dask work within
    the organization

-   Coiled support staff can be added to an account to give them greater
    visibility to help in resolving problems.

Accessing Data
--------------

Data can be accessed in two locations:

-   Visually on the web at ``https://cloud.coiled.io/<your-account-name>/analytics``

    See also the `Analytics` item in your sidebar

-   Programmatically with the ``coiled.analytics`` Python API
    (see :doc:`analytics-api`)


Idle Clusters
-------------

Coiled can politely ask your Dask Scheduler to shut down after a suitable idle
timeout.  This can sometimes help to avoid high costs due to lingering
resources.

Idle timeouts are configurable with the following configuration (off by default):

.. code-block:: yaml

   coiled:
     analytics:
       idle:
         timeout: 20 minutes

Note that when running on your own hardware (not managed by Coiled) Coiled can
only make a best effort here through Dask.  We can not guarantee that things
will shut down cleanly (although they usually do) nor do we have any access
over instances or network resources beyond the Dask processes.
