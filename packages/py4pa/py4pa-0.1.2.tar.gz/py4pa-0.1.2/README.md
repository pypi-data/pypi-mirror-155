# Python for People Analytics

## Installation

Download and install the package on your machine:
```
pip install py4pa
```

If you need to bypass SSL verification on your machine (if you are behind a proxy for example), you can use the following install command:
```
pip install py4pa --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

Import the package into your Python script:
```
import py4pa
# or
from py4pa import [arm]
```

## Usage

### `py4pa.ona`

- `py4pa.ona.clean_email_data(dir, files='all', include_subject=False, engine='c', encoding='latin', delete_old_file=False)`
- `py4pa.ona.generate_node_edge_lists(email_data, demographic_data, demographic_key, output_dir, include_subject=False)`
- `py4pa.ona.generate_nx_digraph(node_list, edge_list)`
- `py4pa.ona.calc_density(df_nodes, df_edges, target_attribute)`
- `py4pa.ona.calc_modularity(df_nodes, df_edges, target_attribute, weighted=False, direction='outbound')`

### `py4pa.arm`

- `py4pa.arm.concat_fields(df, fields)`

### `py4pa.vis`

- `py4pa.vis.gen_expn_colors()`
- `py4pa.vis.gen_gradient_cmap(start, end, steps=50)`

### `py4pa.nlp`

### `py4pa.email_helper`

- `py4pa.email_helper.send_plain_text_email(server, sender, recip, subject, body)`

### `py4pa.http`

- `py4pa.http.get_random_useragent(browser=None):`
- `py4pa.http.Visier`

### `py4pa.misc`

- `py4pa.misc.csv_to_utf8(file)`
- `py4pa.misc.upgradeAllPackages()`
- `py4pa.misc.installPackage(package)`
- `py4pa.misc.getDateTimeStamp(time=True)`
- `py4pa.misc.continuous_logging(msg)`
