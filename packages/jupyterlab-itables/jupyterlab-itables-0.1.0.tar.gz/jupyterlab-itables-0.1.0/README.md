# A Jupyter Lab extension for itables

This extension exposes the [jquery](https://jquery.com/) and [datatables.net](https://datatables.net/) libraries and css as static files in Jupyter Lab.

The purpose of doing this is to allow the [itables](https://mwouts.github.io/itables) package to have an [offline mode](https://github.com/mwouts/itables/issues/70) in Jupyter Lab.

Install it in the Python environment you use to launch Jupyter Lab with:
```shell
pip install jupyterlab-itables
```

Then relaunch Jupyter Lab with
```shell
jupyter lab
```

Assuming that Jupyter Lab is running on port 8888, you will be able to access the static files at e.g.
- http://localhost:8888/static/itables/jquery/dist/jquery.min.js
- http://localhost:8888/static/itables/datatables.net-dt/css/jquery.dataTables.min.css
- http://localhost:8888/static/itables/datatables.net/js/jquery.dataTables.mjs

# How to develop this extension

Assuming that you have conda and mamba, 
you can create a minimal Jupyter Lab environment with
```shell
mamba env create --file environment.yml
```
or update it with
```shell
mamba env update --file environment.yml
```

Activate that environment with
```shell
conda activate jupyterlab-itables-dev
```

Then build the extension in development mode with
```shell
pip install -ve .
```

In development mode the extension needs to be enabled manually with:
```shell
jupyter server extension enable --py jupyterlab_itables
```

# How to release a new version manually

Clean the project files with
```shell
rm -rf node_modules jupyterlab_itables/static dist build package-lock.json
```

Upgrade the version number in `setup.py`, then:
```shell
python setup.py sdist bdist_wheel
```

Check the size and the contents of the `.tar.gz` file in the `dist` folder, 
and then upload it to [pypi](https://pypi.org/) with

```shell
twine upload dist/jupyterlab-itables-xxx.tar.gz 
```