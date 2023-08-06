from multiprocessing import Pool
import itertools
import pandas as pd
import numpy as np
import networkx as nx
import datetime
import csv
import os


def clean_email_data(dir, files='all', include_subject=False, engine='c', encoding='latin', delete_old_file=False):
    """Cleans email data from Splunk to key fields only

    Parameters
    ----------
    dir: String ()
        Path to the root directory containing the data files to process

    file: List or 'all' (optional)
        List containing all files to be processed within the directory. If 'all'
        passed, then all CSV files in the directory will be processed

    include_subject: Boolean default = False
        Defines whether the Subject field should be included in the cleaned data

    engine: String default='c'
        The Pandas engine to read in the data, either 'c' or 'python'

    encoding: String default = 'latin'
        The file encoding of files to be read

    delete_old_file: Boolean default = False
        If set to True, the original Splunk data file will be delete_old_file

    Returns
    -------
    Nothing is returned by the function, but new files are written to 'dir' that
    have been cleaned
    """
    start = datetime.datetime.now()
    print(
        'Starting: ', str(start.hour).zfill(2) + ':'+ str(start.minute).zfill(2)
    )

    if files == 'all':
        files_to_process =  [f for f in os.listdir(dir) if f.endswith('.csv')]
    else:
        files_to_process = files

    num_files = len(files_to_process)
    print(f'{num_files} to process')

    cols_to_load = [
        'message_id',
        'SenderAddress',
        'RecipientAddress',
        'Received',
        'Size',
        'Status'
    ]

    if include_subject:
        cols_to_load.append('Subject')

    for idx, file in enumerate(files_to_process):
        path = dir + file

        df_emails = pd.read_csv(
            path,
            usecols=cols_to_load,
            engine=engine,
            encoding=encoding,
            error_bad_lines=False)

        output_fname = dir + file[:-4] + '_cleaned.csv'

        df_emails.to_csv(output_fname, index=False)

        if delete_old_file:
            os.unlink(path)

        finish = datetime.datetime.now()
        print(
            f'File {idx+1}/{num_files}: {file} finished at: '
            '{str(finish.hour).zfill(2)}:{str(finish.minute).zfill(2)}'
        )

    return None

def generate_node_edge_lists(email_data, demographic_data, demographic_key, output_dir, include_subject=False):
    """Generates Node and Edge lists from email data and saves them to csv

    Parameters
    ----------
    email_data: List of Strings
        List of paths to all files containing email data to be processed

    demographic_data: String
        Path to file containing all node demographic data to be added to Node
        list

    demographic_key: String
        Column in demographic_data that contains email address to act as join
        to email_data

    output_dir: String
        Path to directory to save Node and Edge lists into. Must include '/'
        at end.

    include_subject: Boolean default = False
        Defines whether the Subject field should be included in the email data

    Returns
    -------
    nodeList_fPath: String
        Path to the Node List generated

    edgeList_fPath: String
        Path to the Edge List generated
    """
    start = datetime.datetime.now()
    print('Starting: ', str(start.hour).zfill(2) + ':'+ str(start.minute).zfill(2))

    cols_to_load = [
        'SenderAddress',
        'RecipientAddress',
        'Received',
        'Size'
    ]

    if include_subject:
        cols_to_load.append('Subject')

    df_emails = pd.DataFrame(columns=cols_to_load)

    #Loading in email meta-data
    now = datetime.datetime.now()
    print(
        'Loading in email data: ',
        str(now.hour).zfill(2) + ':'+ str(now.minute).zfill(2)
    )

    for file in email_data:
        df_temp = pd.read_csv(file, usecols=cols_to_load)
        df_emails = df_emails.append(df_temp, sort=True)

    now = datetime.datetime.now()
    print('Email data loaded: ', str(now.hour).zfill(2) + ':'+ str(now.minute).zfill(2))

    #Loading in demographic data
    df_demographics = pd.read_csv(demographic_data, encoding='Latin')
    now = datetime.datetime.now()
    print('Demographic data loaded: ', str(now.hour).zfill(2) + ':'+ str(now.minute).zfill(2))

    #Cleaning up data-sets
    df_emails['RecipientAddress'] = df_emails['RecipientAddress'].str.lower()
    df_emails['SenderAddress'] = df_emails['SenderAddress'].str.lower()
    df_demographics[demographic_key] = df_demographics[demographic_key].str.lower()
    df_demographics = df_demographics.drop_duplicates(demographic_key).set_index(demographic_key)

    #Prepare Node List
    now = datetime.datetime.now()
    print('Node list preparation started: ', str(now.hour).zfill(2) + ':'+ str(now.minute).zfill(2))

    ## Generate list of unique emails
    unique_emails = list(df_emails['RecipientAddress'].unique())
    for idx, email in enumerate(df_emails['SenderAddress'].unique()):
        if email not in unique_emails:
            unique_emails.append(email)

    node_list = []
    for idx, email in enumerate(unique_emails):
        node = {
            'email': email
        }
        node_list.append(node)

    df_nodes = pd.DataFrame(node_list)

    for attr in list(df_demographics.columns):
        df_nodes[attr] = df_nodes['email'].map(df_demographics[attr])

    #Prepare Edge List
    now = datetime.datetime.now()
    print('Edge list preparation started: ', str(now.hour).zfill(2) + ':'+ str(now.minute).zfill(2))
    df_edges = pd.DataFrame({'weight': df_emails.groupby(['SenderAddress','RecipientAddress']).size()}).reset_index()

    #Save Lists to csv
    now = datetime.datetime.now()
    print('Saving Node and Edge lists: ', str(now.hour).zfill(2) + ':'+ str(now.minute).zfill(2))
    fName_date = str(now.year) + str(now.month).zfill(2) + str(now.day).zfill(2) + "_" + str(now.hour).zfill(2) + str(now.minute).zfill(2)

    nodeList_fName = 'nodeList_'+ fName_date + '.csv'
    nodeList_fPath = output_dir + nodeList_fName

    edgelist_fName = 'edgeList_'+ fName_date + '.csv'
    edgeList_fPath = output_dir + edgelist_fName

    df_nodes.to_csv(nodeList_fPath, index=False)
    df_edges.to_csv(edgeList_fPath, index=False)

    now = datetime.datetime.now()
    print('Node and Edge list preparation complete: ', str(now.hour).zfill(2) + ':'+ str(now.minute).zfill(2))
    print('Node List: ', nodeList_fName)
    print('Edge List: ', edgelist_fName)

    return nodeList_fPath, edgeList_fPath


def generate_nx_digraph(node_list, edge_list):
    """Generates NetworkX DiGraph object

    Parameters
    ----------
    node_list: String or Pandas Dataframe
        Path to file containing Node list, or Dataframe of Node List

    edge_list: String  or Pandas Dataframe
        Path to file containing Edge list

    Returns
    -------
    G: NetworkX DiGraph
        NetworkX DiGraph object
    """
    # Create our graph - directed = DiGraph
    G = nx.DiGraph()

    # Read in Node List
    print('Reading in Node list')
    with open(node_list, 'r') as nodecsv:
        nodereader = csv.reader(nodecsv)
        node_list = [n for n in nodereader]
        node_attrs = node_list[:1][0]
        nodes = node_list[1:]

    node_names = [n[0] for n in nodes]
    G.add_nodes_from(node_names)

    for idx, attr in enumerate(node_attrs[1:], 1):
        temp_dict = {}
        for node in nodes:
            temp_dict[node[0]] = node[idx]

        nx.set_node_attributes(G, temp_dict, attr)

    # Read in the edgelist file
    print('Node list loaded; Reading in Edge list')
    with open(edge_list, 'r') as edgecsv:
        edgereader = csv.reader(edgecsv)
        edges = [tuple(e[0:]) for e in edgereader][1:]

    G.add_weighted_edges_from(edges)

    print('NetworkX Graph generated')

    return G

def generate_nx_digraph_pandas(nodes_df, edges_df):
    node_file = './nodes_temp.csv'
    edge_file = './edge_temp.csv'

    nodes_df.to_csv(node_file, index=False)
    edges_df.to_csv(edge_file, index=False)

    G = generate_nx_digraph(node_file, edge_file)

    os.remove(node_file)
    os.remove(edge_file)

    return G


def _get_density(df_nodes, row, target_attribute):
    if row['sender_group'] == row['recipient_group']:
        node_count = df_nodes[df_nodes[target_attribute]==row['recipient_group']]['email'].count()
        density = row['num_edges']/(node_count * (node_count - 1))
        return density
    else:
        node_count_sender = df_nodes[df_nodes[target_attribute]==row['sender_group']]['email'].count()
        node_count_recipient = df_nodes[df_nodes[target_attribute]==row['recipient_group']]['email'].count()
        density = row['num_edges']/(node_count_sender * node_count_recipient)
        return density


def calc_density(df_nodes, df_edges, target_attribute):
    """Calculates the density of connections between the groups in a specific target target_attribute

    Parameters
    ----------
    df_nodes: Pandas DataFrame
        Dataframe containing the Node list

    df_edges: Pandas DataFrame
        DataFrame containing the edge list

    target_attribute: String
        Name of attribute in Node List that we want to calculate the densities between

    Returns
    ----------
    Pandas DataFrame containing the densities, grouped by the target_attribute values
    """

    df_edges = df_edges.copy()
    df_nodes = df_nodes.copy()

    df_edges['sender_group'] = df_edges['SenderAddress'].map(df_nodes.set_index('email')[target_attribute])
    df_edges['recipient_group'] = df_edges['RecipientAddress'].map(df_nodes.set_index('email')[target_attribute])

    df_densities = pd.DataFrame({'num_edges': df_edges.groupby(['sender_group','recipient_group'])['weight'].agg('count')}).reset_index()

    df_densities['density'] = df_densities.apply(lambda row: _get_density(df_nodes, row, target_attribute), axis=1)

    df_densities = df_densities[['sender_group','recipient_group','density']]
    df_densities['density'] = round(df_densities['density'],3)

    return df_densities


def _get_modularity(df_edges, row, target_attribute, weighted, source):
    if source == 'sender_group':
        source_group = 'sender_group'
        end_group = 'recipient_group'
    else:
        source_group = 'recipient_group'
        end_group = 'sender_group'

    if weighted:
        num_same_group = df_edges[(df_edges[source_group]==row[source_group]) & (df_edges[end_group]==row[source_group])]['weight'].count()
        num_diff_group = df_edges[(df_edges[source_group]==row[source_group]) & (df_edges[end_group]!=row[source_group])]['weight'].count()
    else:
        num_same_group = df_edges[(df_edges[source_group]==row[source_group]) & (df_edges[end_group]==row[source_group])]['weight'].sum()
        num_diff_group = df_edges[(df_edges[source_group]==row[source_group]) & (df_edges[end_group]!=row[source_group])]['weight'].sum()

    if num_same_group != 0:
        modularity = num_same_group/num_diff_group
        return modularity
    else:
        return np.nan


def calc_modularity(df_nodes, df_edges, target_attribute, weighted=False, direction='outbound'):
    """Calculates the Modularity of connections originating from groups in a specific target target_attribute

    Parameters
    ----------
    df_nodes: Pandas DataFrame
        Dataframe containing the Node list

    df_edges: Pandas DataFrame
        DataFrame containing the edge list

    target_attribute: String
        Name of attribute in Node List that we want to calculate the
        modularities between

    weighted: Boolean default False
        If set to True, the modularities will be weighted by the amount of
        email traffic.
        If False, will just calculate on basis on presence of a connection

    direction: String default = 'outbound'
        'outbound' or 'inbound' determines the direction of the email traffic
        to be considered

    Returns
    ----------
    Pandas DataFrame containing the modularities, grouped by the
    target_attribute values
    """
    if direction == 'outbound':
        source_group = 'sender_group'
        end_group = 'recipient_group'
    else:
        source_group = 'recipient_group'
        end_group = 'sender_group'

    df_edges = df_edges.copy()
    df_nodes = df_nodes.copy()

    df_edges['sender_group'] = df_edges['SenderAddress'].map(df_nodes.set_index('email')[target_attribute])
    df_edges['recipient_group'] = df_edges['RecipientAddress'].map(df_nodes.set_index('email')[target_attribute])

    if weighted:
        df_modularities = pd.DataFrame({'num_edges': df_edges.groupby([source_group])['weight'].agg('sum')}).reset_index()
    else:
        df_modularities = pd.DataFrame({'num_edges': df_edges.groupby([source_group])['weight'].agg('count')}).reset_index()

    df_modularities['modularity'] = df_modularities.apply(
        lambda row: _get_modularity(
            df_edges,
            row,
            target_attribute,
            weighted,
            source_group)
        , axis=1)

    df_modularities = df_modularities[[source_group,'modularity']]

    return df_modularities

def chunks(l, n):
    """Divide a list of nodes `l` in `n` chunks"""
    l_c = iter(l)
    while 1:
        x = tuple(itertools.islice(l_c, n))
        if not x:
            return
        yield x

def _betmap(G_normalized_weight_sources_tuple):
    """Pool for multiprocess only accepts functions with one argument.
    This function uses a tuple as its only argument. We use a named tuple for
    python 3 compatibility, and then unpack it when we send it to
    `betweenness_centrality_source`
    """
    return nx.betweenness_centrality_source(*G_normalized_weight_sources_tuple)

def betweenness_centrality_parallel(G, processes=None):
    """Parallel betweenness centrality function"""
    p = Pool(processes=processes)
    node_divisor = len(p._pool) * 4
    node_chunks = list(chunks(G.nodes(), int(G.order() / node_divisor)))
    num_chunks = len(node_chunks)
    bt_sc = p.map(_betmap,
                  zip([G] * num_chunks,
                      [True] * num_chunks,
                      [None] * num_chunks,
                      node_chunks))

    # Reduce the partial solutions
    bt_c = bt_sc[0]
    for bt in bt_sc[1:]:
        for n in bt:
            bt_c[n] += bt[n]
    return bt_c
