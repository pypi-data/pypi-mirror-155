import pandas as pd
import plotly.graph_objects as go
from taxontabletools.taxontable_manipulation import strip_metadata
from taxontabletools.taxontable_manipulation import collect_metadata
from taxontabletools.taxontable_manipulation import add_metadata
from taxontabletools.taxontable_manipulation import reduce_taxontable
import PySimpleGUI as sg
from pathlib import Path
from difflib import get_close_matches
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def add_traits_to_TTT(TaXon_table_xlsx, path_to_outdirs, source_file_xlsx):

    TaXon_table_xlsx = Path(TaXon_table_xlsx)
    TaXon_table_df = pd.read_excel(TaXon_table_xlsx).fillna('')
    source_file_xlsx = Path(source_file_xlsx)
    source_file_df = pd.read_excel(source_file_xlsx).fillna('')
    taxonomic_level = source_file_df.columns.tolist()[0]
    allowed_taxonomic_levels = ['Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']

    if taxonomic_level not in allowed_taxonomic_levels:
        warning_text = 'You entered \'{}\'.\nPlease use one of the following taxonomic levels:\n{}'.format(taxonomic_level, ', '.join(allowed_taxonomic_levels))
        sg.Popup(warning_text, title='Error')

    else:
        taxa_whitelist = source_file_df[taxonomic_level].values.tolist()
        trait_dict = {}
        trait_names = source_file_df.columns.tolist()[1::] + ['FLAG']
        n_traits = len(trait_names)

        ############################################################################
        ## create the progress bar window
        layout = [[sg.Text('Progress bar')],
                  [sg.ProgressBar(1000, orientation='h', size=(20, 20), key='progressbar')],
                  [sg.Cancel()]]
        window_progress_bar = sg.Window('Progress bar', layout, keep_on_top=True)
        progress_bar = window_progress_bar['progressbar']
        progress_update = 0
        progress_increase = 1000 / len(TaXon_table_df)
        ############################################################################

        for line in TaXon_table_df[['ID', taxonomic_level]].values.tolist():
            taxon_to_test = line[1]
            ID = line[0]

            ## case 1: taxon is in whitelist
            if taxon_to_test in taxa_whitelist and taxon_to_test != '':
                traits = source_file_df.loc[source_file_df[taxonomic_level] == taxon_to_test].values.tolist()[0][1::]
                trait_dict[ID] = [ID] + traits + ['']

            ## case 2: taxon is not in whitelist but is assigned to a species
            elif taxon_to_test != '':

                ## search closest match
                closest_match = get_close_matches(taxon_to_test, taxa_whitelist, n=1)

                ## if there is a close match add to list but mark it
                if closest_match != [] and similar(taxon_to_test, closest_match[0]) >= 0.9:
                    trait_dict[ID] = [ID] + traits + [closest_match[0]]

                ## else discard it
                else:
                    trait_dict[ID] = [ID] + ['']*n_traits

            ## case 3: discard s
            else:
                trait_dict[ID] = [ID] + ['']*n_traits

            ############################################################################
            event, values = window_progress_bar.read(timeout=10)
            if event == 'Cancel'  or event is None:
                print('Cancel')
                window_progress_bar.Close()
                raise RuntimeError
            # update bar with loop value +1 so that bar eventually reaches the maximum
            progress_update += progress_increase
            progress_bar.UpdateBar(progress_update)
            ############################################################################

        window_progress_bar.Close()

        metadata_df = pd.DataFrame(list(trait_dict.values()), columns=['ID'] + trait_names)
        new_df = add_metadata(TaXon_table_df, metadata_df)
        new_df.to_excel(TaXon_table_xlsx, index=False)

        ## print closing text
        sg.Popup("Traits were added to the TaXon table.", title="Finished", keep_on_top=True)

        ## write log
        from taxontabletools.create_log import ttt_log
        ttt_log("Added traits", "processing", TaXon_table_xlsx.name, TaXon_table_xlsx.name, "", path_to_outdirs)



#
