AWS Quickstart
~~~~~~~~~~~~~~

It's quick and easy to get started using Coiled in your own AWS account.
This guide will cover the steps for getting started with Coiled
using the command-line interface, all from your terminal.

#. Install the Coiled Python library with::

    pip install coiled

   **or**::

    conda install -c conda-forge coiled

#. Log in to your Coiled account::

    coiled login

#. Set up IAM::

    coiled setup aws

   With your permission, this command will create the IAM policies and infrastructure Coiled needs so you can create clusters in your AWS account. You will be prompted with an explanation at each step, so you can choose to say "yes" (or "no") at any point (see :doc:`aws_configure` for more details). 

   .. note::
      If you don't have an AWS account, you can sign up for `AWS Free Tier <https://aws.amazon.com/free>`_.

#. Start your Dask cluster in the cloud (see :ref:`Running your computation <first-computation>`)::

    ipython
    > import coiled
    > cluster = coiled.Cluster(n_workers=10)

Will this cost money?
---------------------

Yes, but you can try Coiled without seeing a huge bill from Amazon, or any bill from Coiled!

Setting up Coiled to use your AWS account is free of charge. There are no charges from Coiled or Amazon until you start spinning up clusters. Once you start spinning up clusters, you will pay Amazon for the EC2 instances, data transfer, and storing logs in CloudWatch.

You can try Coiled with a relatively small bill from Amazon. Running a cluster with 100 t3.medium instances for an hour, for example, will cost about $5 for the EC2 instances in any of the commonly used US regions (us-east-1, us-east-2, us-west-1, us-west-2). Data transfer is pennies per GB (see the `AWS EC2 pricing documentation <https://aws.amazon.com/ec2/pricing/on-demand/>`_).

Is Coiled secure?
-----------------

Our approach is to make your cluster secure, by default. Coiled has achieved SOC 2 compliance and prioritizes secure network communication and data privacy for our users.

Coiled was designed with secure network communication and data security in mind based on many years of experience of working with Dask users in enterprise environments. Communication between between client and the cluster is encrypted and authenticated (using mTLS). For more details see :ref:`Network security and architecture <network-architecture>`.

Additionally, all compute resources, access to sensitive data, storage of software environment images, and system logs will happen entirely within your AWS account. Coiled just has access to metadata about your cluster, but your data stays in your own account (see :doc:`analytics-privacy` for more details).






