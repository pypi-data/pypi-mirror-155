PET dataset reader
##################

Benchmarking procedure to test approaches on the `PET-dataset`_ (hosted on huggingface_).

.. _PET-dataset: https://pdi.fbk.eu/pet-dataset/
.. _huggingface: https://huggingface.co/datasets/patriziobellan/PET

This is an alpha version. Do not use it in production since names and functions may change.

Documentation will come soon.

Example of ''how to benchmark an approach''
*******************************************


.. code-block:: python

    from petbenchmarks.benchmarks import BenchmarkApproach

    BenchmarkApproach(tested_approach_name='Approach-name',
                      predictions_file_or_folder='path-to-prediction-file.json')


The ``BenchmarkApproach`` object does all the job.
It reads the file, computes score and generates a reports in the same
directory of the ``path-to-prediction-file.json``.


Created by `Patrizio Bellan`_.

.. _Patrizio Bellan: https://pdi.fbk.eu/bellan/

