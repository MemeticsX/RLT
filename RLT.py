##############################################################################################################################################################
##                                                                                                                                                          ##
##  Memetics' Random Loot Tables: A random loot table (RLT) datapack generator for Minecraft                                                                ##
##                                                                                                                                                          ##
##  Copyright (c) 2021-2022 Memetics (Minecraft and Twitch username) / viralmeme (Github username)                                                          ##
##                                                                                                                                                          ##
##  For the latest source code and documentation, visit htps://github.com/viralmeme/RLT                                                                     ##
##                                                                                                                                                          ##
##  Join the RLT discussion in the Mining after Dark ("MaD") community on Discord: https://discord.gg/CHdxWu26kS                                            ##
##                                                                                                                                                          ##
##                                                                                                                                                          ##
##  This file is part of Memetics' Random Loot Tables.                                                                                                      ##
##                                                                                                                                                          ##
##  Memetics' Random Loot Tables is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License               ##
##  as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.                                   ##
##                                                                                                                                                          ##
##  Memetics' Random Loot Tables is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty             ##
##  of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.                                            ##
##                                                                                                                                                          ##
##  You should have received a copy of the GNU General Public License along with Memetics' RLT.  If not, see https://www.gnu.org/licenses/ .                ##
##                                                                                                                                                          ##
##############################################################################################################################################################


import os
import io
import sys
import json
import random
import zipfile


# Application version, supported (Java) Minecraft version, and Minecraft datapack format version

RLT_version = '0.14'
Minecraft_version = '1.18.1'
Datapack_format = 8             # Must be a numeric value, not a string, or the string's surrounding quotes will end up in the datapack metadata and break it.


# Begin UI output

print('\nMemetics\' Random Loot Tables {} for (Java) Minecraft {} (works with Minecraft 1.14 or later).'.format(RLT_version, Minecraft_version))
print('Copyright (c) 2021-2022 Memetics (GNU General Public License version 3)\n\n')
print('This application randomizes the default loot tables for Minecraft.  It generates a datapack that the user then')
print('places in a savegame\'s datapacks folder.  In Minecraft 1.17 and later, the datapacks folder can be accessed')
print('before world creation on the Create New World page using the Data Packs button.  The datapacks folder for an')
print('existing savegame can be found in the savegame\'s root folder, which can be opened from within Minecraft by')
print('clicking Singleplayer, then on the Select World page, selecting the savegame, clicking the Edit button, and then')
print('on the Edit World page clicking the Open World Folder button.\n')
print('This application requires extracting the loot tables from the current Minecraft version (the folder called')
print('loot_tables and all of its sub-folders and files).  The loot_tables root folder must be in the same folder as this')
print('application for the application to locate the loot tables and generate the data pack correctly.  In addition, the')
print('blockers.config, bottlenecks.config, and showstoppers.config files must be in the current folder if customization')
print('is being used.  It is also recommended to remove the "killed by user" condition block from all of the entity loot')
print('tables to prevent the failure of entity drops when their tables are assigned to non-killable entities.  Similarly,')
print('the condition that checks the fishing bobber state should be removed from the fishing table to ensure that the')
print('fishing treasure sub-table can be called by the main fishing table.\n\n')


# Prompt user for a PRNG seed

seed = input('Enter a seed (a number or text string). Leave blank for a system-generated random seed: ')
print()

# Set PRNG seed & datapack name based on user input
    # Do we need error checking on seed length to prevent buffer overflow?

if len(seed) > 0:
    print('Creating RLT datapack using the seed "{}".\n'.format(seed))
    random.seed(seed)
    datapack_name = 'RLT_{}'.format(seed)
    datapack_description = 'Memetics\' Random Loot Tables: seed = {}'.format(seed)
else:
    print('Creating RLT datapack using a random, system-generated seed (different for each run).\n')
    datapack_name = 'RLT_random_seed'
    datapack_description = 'Memetics\' Random Loot Tables: random seed'

datapack_filename = datapack_name + '_for_Minecraft_' + Minecraft_version + '.zip'

print('This may take a moment, depending on the size of the loot table set...\n')

# Declare list & dictionary variables for handling loot tables file names and assignments

table_names = []            # All the non-blocker loot tables file names (including relative paths), as read from the file structure.
unassigned = []             # The non-bottleneck loot tables file names (drops that have not yet been assigned).
showstoppers = []           # Loads showstoppers.txt list of loot table names we don't want included in the datapack at all.  Removed from table_names permanently.
bottlenecks = []            # Loads bottlenecks.txt list of loot table file names we don't want assigned to blockers tables.  Priority-assigned before the main unasssigned list.
blockers = []               # Loads blockers.txt list of loot table names we don't want bottlenecks drops assigned to.  Added to table_names only after bottlenecks are assigned.
                                # --> Later, we may expand to enable selectable degrees of difficulty: multiple "frustrater" levels (selectable at runtime).
unassigned_bottlenecks = [] # List of bottlenecks files (local path + filename): These drops are assigned to random table_names before the rest of the assignments are made.
table_names_blockers = []   # List of blockers files (local path + filename): These are added to table_names after the bottlenecks files have been assigned.

assignments = {}            # Used to build the RLT datapack .zip file: A dictionary of randomized pairs of loot table file names with path.  The zip file creation code takes the 
                            # file name listed in the key (the first loot table name) and assigns it the file contents from the file listed in the value (the second loot table name).


# Load lists of bottlenecks, blockers, and showstoppers files.
    # --> Should add error checking here to handle missing or empty config files.

with open('showstoppers.config', 'r') as showstoppersfile:          # Load showstoppers list from file.  ( --> Add error checking!  Ignore empty lines.)
    print('Loading show-stoppers file list from config file')
    showstoppers = showstoppersfile.read().split('\n')              # Assign each line of the file to the show-stoppers list.

with open('bottlenecks.config', 'r') as bottlenecksfile:            # Load bottlenecks list from file.  ( --> Add error checking!  Ignore empty lines.)
    print('Loading bottlenecks file list from config file')
    bottlenecks = bottlenecksfile.read().split('\n')                # Assign each line of the file to the bottlenecks list.

with open('blockers.config', 'r') as blockersfile:                  # Load blockers list from file.  ( --> Add error checking!  Ignore empty lines.)
    print('Loading blockers file list from config file')
    blockers = blockersfile.read().split('\n')                      # Assign each line of the file to the blockers list.

# Load all of the loot_tables file names from the loot_tables folder tree (including local relative paths), sorting them to table_names and table_names_blockers lists.
    # Note: The files in the loot_tables tree should have been pre-culled and edited* (see RLT readme file).
        # --> *Future plan: Write a separate application to automatically remove the "killed by player" block from the .json files.
        # --> Would be nice if we could do that removal from within this application, and only for assignments where a non-mob loot table gets assigned a mob drop...).

###################################################################################
## NOTE!  Replace 'loot_tables' below with 'LT_test' or 'LT_test_7' for testing. ##    ( --> Research changing file/folder handling to load loot tables from a different folder location.)
###################################################################################    ( --> Create an installer / installation package?)

loot_tables_folder = 'loot_tables'  # For production, set this to the normal Minecraft loot tables folder, 'loot_tables'.  For testing, set this to 'LT_test' or 'LT_test_7'.
                                    # --> Currently, the loot tables folder must be present in this Python application's local folder / current directory for the application to work.
                                    # NOTE: If using a test loot tables folder, such as LT_test, after datapack generation you'll need to rename the folder to loot_tables
                                    # in the .zip file for the test datapack to work in-game.  At some point, the code should be updated to revise the root name to loot_tables.

# Test whether the loot_tables_folder exists and is accessible; if not, report error and exit.  Otherwise continue.

if os.path.isdir(loot_tables_folder) == False:
    print('The loot tables folder {} is not accessible or does not exist in the current folder.\n'.format(loot_tables_folder))
    os.system('pause')
    sys.exit()

print('Scanning local {} folder tree for loot table files'.format(loot_tables_folder))


# Read the loot tables directory: Ignore file names that appear on the showstoppers list, and then
# assign all remaining file names to the table_names lists (filtered by blockers) and also to the unassigned lists (filtered by bottlenecks).
    # Filtered file names get assigned to either the table_names_blockers list or the unassigned_bottlenecks list.
            # --> Do we need to add error-checking here to at least report if a file name in the blockers or bottlenecks list does not exist in the local loot tables set?

for dirpath, dirnames, filenames in os.walk(loot_tables_folder):
    for filename in filenames:
        if filename in showstoppers:                                        # Skip all loot tables that appear in the show-stoppers list.  (Report each skipped file to print output.)
            print('Skipping show-stopper {}'.format(filename))
        elif filename in bottlenecks:                                       # Add bottlenecks files to table_names (allow bottleneck names to have bottleneck drops), but instead of
            table_names.append(os.path.join(dirpath, filename))             # adding them to unassigned, put them in the special unassigned_bottlenecks list for priority assignment.
            unassigned_bottlenecks.append(os.path.join(dirpath, filename))
        elif filename in blockers:                                          # Add blockers files to the unassigned list but not the main table_names list: keep them in
            table_names_blockers.append(os.path.join(dirpath, filename))    # the separate table_names_blockers list until the bottlenecks drops have been assigned.
            unassigned.append(os.path.join(dirpath, filename))              # Then later we'll return them to the main table_names list for assignment with the rest.
        else:
            table_names.append(os.path.join(dirpath, filename))             # All other (non-special) tables get added to both table_names and unassigned.
            unassigned.append(os.path.join(dirpath, filename))

# Assign the bottlenecks drops to random, non-blocker table_names. 

if len(unassigned_bottlenecks) > 0:
    print('Assigning bottleneck drops to random non-blocker tables')
    for drop in unassigned_bottlenecks:             # Go through the table_names list and give each a random drops assignment from the unassigned list.  Pick random 
        i = random.randint(0, len(table_names)-1)   # loot table file name from table_names for each unassigned_bottlenecks drop, and assign them to the assignments 
        assignments[table_names[i]] = drop          # dictionary as key(table_names): value(unassigned_bottlenecks).  Then delete the table_names entry for each:
        del table_names[i]                          # This way we don't later try to assign a different unassigned drop value to a previously assigned table_names key.

# Now that the bottlenecks have been taken care of, add the table_names_blockers to the main table_names list.
    # Then all the remaining table_names names and unassigned drops will be ready for assignment.

if len(table_names_blockers) > 0:
    print('Moving blockers to main tables list')
    for blockername in table_names_blockers:
        table_names.append(blockername)

# About to complete remaining assignments: Report status (varying by whether or not there were bottlenecks assignments).

if len(assignments) > 0:
    print('Assigning random drops for remaining loot tables')
else:
    print('Assigning random drops for all loot tables')

# Error check: make sure table_names and unassigned lists have same number of elements.

if len(table_names) != len(unassigned):
    print('Error: table_names list and unassigned list contain different items or numbers of elements.')
    os.system('pause')
    sys.exit()

# Complete all of the remaining table --> drop assignments:
    # For each table_names name, assign a random unassigned drop (add as key:value to assignments dictionary).

for name in table_names:
    i = random.randint(0, len(unassigned)-1)
    assignments[name] = unassigned[i]
    del unassigned[i]

# Create new dictionary of assignments by file names only (strip out the path elements) using a dictionary comprehension.
    # This will be used to create a text file with a listing of all assignments sorted by file name for game post-mortem analysis.

basename_assignments = {os.path.basename(key): os.path.basename(assignments[key]) for key in assignments}

# Now build the datapack .zip file.
    # --> A progress bar would be nice.

print('Building datapack zip file\n')

# Build the zip file contents.

zipdata = io.BytesIO()                                                  # Assign zipdata as a file-like object which will be the container for the binary stream data that follows.
with zipfile.ZipFile(zipdata, 'w', zipfile.ZIP_DEFLATED, False) as zf:  # Assign zf as a zipfile object, which will handle operations for writing zipfile contents to zipdata in memory
                                                                            # prior to the file write operation.

# Write the loot tables assignments to two text files (sorted by loot tables tree; sorted by table file name) for post-game analysis and troubleshooting (add both to zf).

    with io.StringIO() as fc:       # Create fc as a text stream to contain the following text (in the "with" block), which will be stored in a variable and then written to the text file.
        fc.write('RLT datapack: {}.zip\nLoot table assignments sorted by loot table tree path:\n\n'.format(datapack_name))  # Write this content at the start of fc (for top of text file).
        for key, value in sorted(assignments.items()):                              # For each dictionary entry in assignments, sorted by key (path + filename),
            print('{0} --> {1}'.format(key, os.path.basename(value)), file = fc)    # add each key (path + filename) and its value (filename only) to fc (file = for the print statement).
        assignments_by_tree = fc.getvalue()                                         # Assign the buffer contents in fc to assignments_by_tree, so we can then write the file.
    zf.writestr('RLT_info/Loot table assignments by tree.txt', assignments_by_tree) # Write the text file into the .zip file.

    with io.StringIO() as fc:       # Create fc as a text stream to contain the following text (in the "with" block), which will be stored in a variable and then written to the text file.
        fc.write('RLT datapack: {}.zip\nLoot table assignments by file:\n\n'.format(datapack_name))     # Write this content at the start of fc (for top of text file).
        for key, value in sorted(basename_assignments.items()):                     # For each dictionary entry in basename_assignments, sorted by key (filename),
            print('{0} --> {1}'.format(key, value), file=fc)                        # add each key (filename only) and its value (filename only) to fc (file = for the print statement).
        assignments_by_file = fc.getvalue()                                         # Assign the value of fc to assignments_by_file, so we can then write the file.
    zf.writestr('RLT_info/Loot table assignments by file.txt', assignments_by_file) # Write the text file into the .zip file.

# For each "key" (loot table file name) in assignments, create a file with that name in the zip file but containing the "value" loot table file's contents.

    for lootfile in assignments:
        with open(assignments[lootfile]) as file:
            contents = file.read()
        zf.writestr(os.path.join('data/minecraft/', lootfile), contents)

# Write the rest of the Minecraft-required datapack files:

    zf.writestr('pack.mcmeta', json.dumps({'pack':{'pack_format':Datapack_format, 'description':datapack_description}}, indent=4))  # pack_format value = 7 for Minecraft 1.17
    zf.writestr('data/minecraft/tags/functions/load.json', json.dumps({'values':['{}:reset'.format(datapack_name)]}))               # and = 8 for Minecraft 1.18+.
    zf.writestr('data/{}/functions/reset.mcfunction'.format(datapack_name), 'tellraw @a ["",{"text":"Memetics\' RLT: Random Loot Tables","color":"green"}]')

# Check for existence of datapacks folder; if it does not exist, create it.

datapack_folder = os.path.join(os.getcwd(), 'RLT datapacks')            # Set the RLT datapacks output folder as a subfolder in the current folder.
print('Writing datapack file to folder: {}\n'.format(datapack_folder))

try:
    if not os.path.isdir(datapack_folder):                              # If the RLT datapacks output folder doesn't exist in the current folder, create it.
        os.mkdir(datapack_folder)
except Exception:
    print('Datapack folder could not be created or accessed.  Make sure you have write access permission for {}.'.format(datapack_folder))
    os.system('pause')
    sys.exit()

# Now write the actual .zip file to the datapack folder using the zip file contents we just created in the zipdata file-like object.

try:
    with open(os.path.join(datapack_folder, datapack_filename), 'wb') as file:
            file.write(zipdata.getvalue())
except Exception:
    print('Datapack file could not be created (.zip file write operation failed). Check to make sure you have access permissions to the folder.')
    os.system('pause')
    sys.exit()

# Report success, pause for keystroke, and then exit.

print('Datapack {} was created successfully.\n'.format(datapack_filename))

os.system('pause')
sys.exit()


### This project was inspired by the SethBling YouTube video that introduced the idea of basic loot table randomizing. ###
