################################################################################
##
##  Memetics' Random Loot Tables: A random loot table (RLT) datapack generator
##  for Minecraft.
##
##  Copyright (c) 2021-2023 by Memetics (Minecraft) / Memetics (Twitch) /
##      MemeticsX (GitHub)
##
##  Written in Python (most recently version 3.11.1) using IDLE.
##
##  For the latest source code and documentation, visit:
##  https://github.com/memeticsx/RLT
##
##  Join the RLT discussion in the Mining after Dark ("MaD") community on
##  Discord: https://discord.gg/guTcuM5V62
##
##
##  This file is part of Memetics' Random Loot Tables.
##
##  Memetics' Random Loot Tables is free software: you can redistribute it
##  and/or modify it under the terms of the GNU General Public License as
##  published by the Free Software Foundation, either version 3 of the License,
##  or (at your option) any later version.
##
##  Memetics' Random Loot Tables is distributed in the hope that it will be
##  useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
##  Public License for more details.
##
##  You should have received a copy of the GNU General Public License along
##  with this application.  If not, see https://www.gnu.org/licenses/ .
##
################################################################################


###----------------> WIDTH MEASUREMENT BAR (80 CHARACTERS) <-----------------###


import os
import io
import sys
import json
import random
import zipfile
from pathlib import Path


################################################################################
# Application version, supported (Java) Minecraft version, Minecraft datapack
# format version, and meta (pack.mcmeta) string

RLT_version = '0.15.4.beta'
Minecraft_version = '1.19.3'
datapack_format = 10

# Note: The value for datapack_format needs to be '10' for Minecraft 1.19.x.
# Must be a numeric value, not a string, or the string's surrounding quotes
# will end up in the datapack metadata and break it.

# --> Future plan: Make the Minecraft_version selectable, and modify
# datapack_format to follow the correct version.  If the user selects "future
# (post- {current Minecraft version}) version - experimental", add +1 to the
# current datapack_format value, or prompt them for the new datapack format
# number.  (?)


################################################################################
# Folder locations

    # For production, set this to the default Minecraft loot tables folder,
    # 'loot_tables'.  For testing, set to another (test) folder.
    #
    # --> Currently, the loot tables folder must be present in this Python
    # application's local folder / current directory for the application to
    # work.  NOTE: If using a test loot tables folder, such as LT_test, after
    # datapack generation you'll need to rename the folder to loot_tables in
    # the .zip file for the test datapack to work in-game.
    # --> For testing, possibly we could code the .zip file creation steps to
    # include updating the root folder name to loot_tables, regardless of what
    # the internal name is here.  (But maybe that's just too much of an edge
    # case to bother with; most users probably would never be working with
    # a different folder name there.)

        # --> To-Do: Research changing folder handling to load loot tables from another location.
        # --> Create an installer / installation package?
        # --> Add working folder / path-building

loot_tables_folder = 'loot_tables'

# Error check: Test whether the loot_tables_folder exists and
# is accessible; if not, report error and exit.

if os.path.isdir(loot_tables_folder) == False:
    print(f"The loot tables folder '{loot_tables_folder}' is not accessible or does not exist in the current folder.")
    print("The default loot tables folder and all of its contents (including sub-folders) must be extracted (copied)")
    print(f"from the Java Minecraft {Minecraft_version} game installation files and must be located in the current working folder")
    print("where this RLT application is running.\n")
    print()
    print(f"To extract the loot tables folder: in %AppData%, go to: \\.minecraft\\versions\\{Minecraft_version} and open {Minecraft_version}.jar")
    print("using 7zip or another file compression utility.  (This may require opening the .jar file from within the")
    print("unzip utility or renaming a copy of the .jar file to give it the .zip extension.)  Then in the .jar file,")
    print("navigate to the data/minecraft/loot_tables folder and extract the folder, copying it to the RLT working folder.")
    print("See the documentation for Memetics' RLT for more details.\n")
    print()
    print("Exiting...\n")
    os.system('pause')
    sys.exit()

# Set the RLT datapacks output folder as a subfolder of the current folder.

datapack_folder = os.path.join(os.getcwd(), 'RLT datapacks')


################################################################################
# (Config) File locations

exclusionsconfig = os.path.join(os.getcwd(), 'exclusions.config')
bottlenecksconfig = os.path.join(os.getcwd(), 'bottlenecks.config')
blockersconfig = os.path.join(os.getcwd(), 'blockers.config')
two_block_objectsconfig = os.path.join(os.getcwd(), '2-block_objects.config')


################################################################################
# Declare list & dictionary variables for handling loot tables file names
# and assignments

# Non-blocker loot tables file names (including relative paths).
table_names = []

# Non-bottleneck loot table file names (drops that have not yet been assigned).
unassigned = []

# Loot table names we don't want included in the datapack at all.
exclusions = []

# Loot table names we don't want assigned to drop any of the blockers tables.
# These are assigned before the main unasssigned set.
bottlenecks = []

# Loot table names we don't want assigned to drop from bottlenecks objects.
# Added to table_names only after bottlenecks are assigned.
    # --> Later, we may expand to enable selectable degrees of difficulty:
    #   multiple "frustrater" levels (selectable at runtime).
blockers = []

# These are assigned to random table_names before other assignments are made.
unassigned_bottlenecks = []

# These are added to table_names after the bottlenecks files have been assigned.
table_names_blockers = []

# Used to build the RLT datapack .zip file: A dictionary of randomized pairs
# of loot table file names with path.
assignments = {}

# The file name - table contents assignments with the loot tables cleaned up.
# This is the list used for data pack .zip file creation.  The code takes the
# file name listed in the key (the first loot table name) and assigns it the
# file contents from the file in the value (the second loot table name).
new_tables = {}

# Lists of table names in each sub-folder of the loot tables root folder.
# Doesn't (yet) include sub-sub-folders (villagers, sheep, etc.).
    # --> Instead of determining these from the folder tree, maybe we could
    #   read the "type" key's value from each file and use that info instead.
blocks_table_names = []
# chests_table_names = []   # Not implemented yet.
entity_table_names = []
# gameplay_table_names = [] # Not implemented yet.

# Doors, beds, and tall flowers.  Need this list to clean their loot tables of
# problematic conditions checks.
two_block_objects = []

    # --> Future plan: Convert config files into one JSON file with sections
    #   (nested lists), and write a separate tool or add code here to enable
    #   config content manipulation programmatically.  Could even error-check
    #   by checking the file name selections against the current loot tables
    #   set's file names.


################################################################################
# Functions - JSON file handling; loot table conditional altering; etc.

    # --> Future plan: Convert more of the main UI section into functions.

    # --> Implement another fuction, conditions_surgeon or something, that will
    #   search all "conditions" blocks for a specific sub-key or sub-value,
    #   killing the entire block when found.  For example,
    #   "minecraft:block_state_property."


def kill_keys(obj, key, subkey=None, subval=None):
    """Searches a JSON tree of nested list and dict elements for occurrences
    of empty list and dict elements and removes them.  Also removes dict keys
    that match key if the key's value is a list of dicts and if one of
    those dicts has a key matching subkey, a value matching subval, or both if
    both are passed to the function.  If subkey and subval are not provided,
    all matches of key are deleted.  Returns the modified obj.

    :param obj: A JSON tree object of nested iterables (dicts and/or lists).
    :param key: The key to search for and remove.
    :param subkey: (Optional) The sub-key to search for.
    :param subval: (Optional) The sub-value to search for.
    """

    def empty(x):
        return x is None or x == {} or x == [] or x == ''

    def search_branch(obj, key, subkey, subval):
        """Recursively search a complex JSON tree for empty list and dict
        entries and key (with required subkey and subval, if provided) and
        remove all instances found.
        """

        # If obj is not a list or dict (typically where we've hit a
        # leaf - no further nested levels of dict or list), return
        # the obj unchanged.

        if not isinstance(obj, (dict, list)):
            return obj

        # If obj is a list, prune each element, and return a pruned
        # list without the empty list elements.

        elif isinstance(obj, list):
            return [v for v in (search_branch(v, key, subkey, subval)
                                    for v in obj) if not empty(v)]

        # If this is reached, obj is a dict.  For each key in the dict,
        # if it matches key, and no subkey and subval were provided,
        # delete the key.  Or if the key's value is a list of dicts,
        # search for a match of subkey or subval (or subkey and subval
        # if both are provided), and if found, delete key.  Then return
        # a pruned dict of the key: (pruned) value pairs, including all
        # of the remaining ones except any empty ones.

        else:   # obj is a dict
            for k, v in list(obj.items()):

                # If no subkey & subval, delete key if found.

                if k == key:
                    if empty(subkey) and empty(subval):
                        obj.pop(k)

                    # Search for subkey and subval in the sub-dicts.
                    # If sub-dicts have subkey and subval (or one, if
                    # the other wasn't provided), delete key.
                    
                    else:
                        if isinstance(v, list):
                            for item in v:
                                if isinstance(item, dict):
                                    for sk, sv in list(item.items()):
                                        if ((sk == subkey and sv == subval) or (
                                                sk == subkey and empty(subval)) or (
                                                empty(subkey) and sv == subval)):
                                            obj.pop(k)

            # Whether or not we've killed any keys, next iterate through
            # any remaining keys, returning a dict of k: v pairs for all
            # of the (pruned) values in the dict, except leave out any
            # keys with empty values.

            return {k: v for k, v in ((k, search_branch(v, key, subkey, subval))
                                    for k, v in obj.items()) if not empty(v)}

    # The call that starts the recursion through the tree, ultimately
    # returning the fully pruned object (the result of the prune_branch
    # function call).

    return search_branch(obj, key, subkey, subval)


def prune_json_tree(obj, kill_key=None, kill_val=None):
    """Searches a JSON tree of nested list and dict elements for occurrences
    of empty list and dict elements and removes them.  Also removes dict keys
    that match key and val (if both are passed to the function), or key, or val.
    If neither key nor val are passed, function simply prunes all empty branches
    found in obj.  Returns the pruned obj.

    :param obj: A JSON tree object of nested iterables (dicts and/or lists).
    :param key: (Optional) The key to search for.
    :param val: (Optional) The value to search for.
    """

    def empty(x):
        return x is None or x == {} or x == [] or x == ''

    def prune_branch(obj, kill_key, kill_val):
        """Recursively search a complex JSON tree for empty list and dict
        entries (and key / val if given) and remove all instances found.
        """

        # If obj is not a list or dict (typically where we've hit a
        # leaf - no further nested levels of dict or list), return
        # the obj unchanged.

        if not isinstance(obj, (dict, list)):
            return obj

        # If obj is a list, prune each element, and return a pruned
        # list without the empty list elements.

        elif isinstance(obj, list):
            return [v for v in (prune_branch(v, kill_key, kill_val)
                                    for v in obj) if not empty(v)]

        # If this is reached, obj is a dict.  For each key and value
        # pair in the dict, delete the pair if it matches kill_key
        # or kill_val (or both, if both were given).  Then return a
        # pruned dict of the key: (pruned) value pairs, including
        # all of the remaining ones except any empty ones.

        else:   # obj is a dict
            for k, v in list(obj.items()):
                if ((k == kill_key and v == kill_val)
                        or (k == kill_key and empty(kill_val))
                        or (empty(kill_key) and v == kill_val)):
                    obj.pop(k)

            # Whether or not we've killed any keys, next iterate through
            # any remaining keys, returning a dict of k: v pairs for all
            # of the (pruned) values in the dict, except leave out any
            # keys with empty values.

            return {k: v for k, v in ((k, prune_branch(v, kill_key, kill_val))
                                    for k, v in obj.items()) if not empty(v)}

    # The call that starts the recursion through the tree, ultimately
    # returning the fully pruned object (the result of the prune_branch
    # function call).

    return prune_branch(obj, kill_key, kill_val)


def checkcollisions(a, b, aname, bname):
    """Test to see whether loot tables are included on more than one config
        list.  If so, reports the error, then exits.

    :param a: First list of loot tables to be compared
    :param b: Second list of loot tables to be compared
    :param aname: Name of first list of loot tables
    :param bname: Name of second list of loot tables
    """

    collisions = sorted(set(a).intersection(b))
    if len(collisions) > 0:
        print("\nThe datapack cannot be generated because of conflicting\n")
        print("entries in the config lists.  The following loot tables are\n")
        print(f"listed on both {aname} and {bname} lists:\n")

        # Using the "unpacking" operator (*) to unpack the list and then
        # changing the separator from space to newline:

        print(*collisions, sep="\n")
        print("\nEach loot table can be on only one list at most.  Please")
        print("update the config lists to remove duplicates and then run the")
        print("application again.\n")
        print("Exiting...\n")
        os.system('pause')
        sys.exit()


def revise_contents(dropperfilepath, lootfilepath, loottable):
    """Examines each entry in the assignments dict and returns each loot table
        with revisions to correct issues if certain conditions are met.

    :param dropperfilepath: The file name of the object doing the dropping
    :param key: The file name of the new loot table to be dropped
    :param value: The loot table (the file contents)
    """

    # For clarity and simplicity, extract the file names from the paths.

    dropperfile = os.path.basename(dropperfilepath)
    lootfile = os.path.basename(lootfilepath)

##    print(f"Examining lootfile: {lootfile}...\n") # <-- For testing only

    # If the dropper is the same as the loot to be dropped (i.e., it
    # was assigned to drop itself), keep the loot table as-is.

    if dropperfile == lootfile:
        return loottable

    # Because "minecraft:killed_by_player" is the only condition that can
    # cause an entity drop to fail: If an entity is assigned to drop another
    # entity's drops, no changes are made (the new entity can still be killed),
    # unless the dropper is the armor stand - a non-killable entity, in which
    # case the killed_by_player condition is removed.

    elif dropperfile in entity_table_names and lootfile in entity_table_names:
        if dropperfile == 'armor_stand.json':
            pruned = prune_json_tree(loottable, 'condition', 'minecraft:killed_by_player')
            pruned2 = prune_json_tree(pruned, 'condition' 'minecraft:match_tool')
            return pruned2
        else:
            return loottable

    # If the dropper is not an entity but the lootfile is, remove the
    # impossible-to-meet condition "killed_by_player".
    #
    # --> We may need to further test the condition(s) relating to non-entity
    # objects being assigned to drop entity tables.
    #
    # * Testing note: If prune_json_tree would return the killed key's value,
    # we could wrap the prune_json_tree call in a print statement for testing
    # and confirmation.

    elif dropperfile not in entity_table_names and lootfile in entity_table_names:
        return prune_json_tree(loottable, 'condition', 'minecraft:killed_by_player')

    # If the lootfile is one of the two-block objects, we remove the
    # self-check condition that prevents drops from any non-self object.
    # (This condition was preventing drops of beds, doors, and tall flowers.)
    # In future versions, we may make this more sophisticated: for example,
    # restoring the dropper file's conditions block so that a 2-block
    # object still drops only one copy of its random loot instead of two.
    #
    # --> Future plan: Test condition(s) relating to 2-block objects.  For
    # 2-block objects, restore the 2-block table names' own "entries" > 
    # "conditions" section (if this will not conflict with oddball drop tables'
    # conditions). Might need to add the condition to each section for each
    # item to drop.  May still require removing an existing condition or
    # conditions block, particularly if the lootfile is also a 2-block object.
    #
    # We could also apply this thinking to double slabs (re-enabling them
    # as the dropper to drop two items instead of one).  (But doesn't normal
    # Minecraft logic only drop one slab when a double is broken?)
    #
    # --> Also note: Since this is a known location in the JSON data, we're
    # pointing to its specific location here.  But for future-proofing, we
    # might need to change this to a recursive search instead: once finding
    # the correct conditions key/section, searching deeper to ensure that it
    # is indeed the correct one before completing the operation.

    elif lootfile in two_block_objects:
        return kill_keys(loottable, 'conditions', 'block')

    # If the lootfile is fishing.json (and it wasn't assigned to drop itself),
    # remove the impossible-to-meet condition of the object having a bobber and
    # being in open water (and thus allow treasure drops still).
    #
    # --> Future plan: Develop a deeper-recursion search function, one that
    # can locate the main key and then search deeper to locate a sub-key under
    # that key to confirm that the main "conditions" key needs to be removed,
    # or to delete only the (a) sub-key under it.  (See two-block objects note.)

    elif lootfile == 'fishing.json':
        return kill_keys(loottable, 'conditions', 'entity', 'this')

    # The glow lichen table checks self for each of its six orientations to
    # prevent double drops.  But like the two-block objects, this check will
    # prevent drops from other objects, so we remove the "functions" key
    # where all of these conditions are checked.
    #
    # --> When glow lichen is the dropper, as with two-block objects (beds,
    # doors, tall flowers), we might want in the future to restore the default
    # glow lichen functions to whatever table it is assigned.

    elif lootfile == 'glow_lichen.json':
        return kill_keys(loottable, 'functions')

    # If none of the other checks passed, it means that (hopefully) there are
    # no other conditions in which the drop will be broken or otherwise
    # problematic, so we return loottable as-is.

    else:
        return loottable


################################################################################
# Begin UI output


print(f"\nMemetics\' Random Loot Tables {RLT_version} for (Java) Minecraft {Minecraft_version}")
print("(should work with Minecraft 1.14 or later).")
print("Copyright (c) 2021-2023 Memetics (GNU General Public License version 3)")
print()
print("For the latest source code and documentation, visit https://github.com/MemeticsX/RLT .")
print("\n")
print("This application randomizes the default loot tables for Minecraft.  It generates a datapack that the user then")
print("places in a savegame\'s datapacks folder.  In Minecraft 1.17 and later, the datapacks folder can be accessed")
print("before world creation on the Create New World page using the Data Packs button.  The datapacks folder for an")
print("existing savegame can be found in the savegame\'s root folder, which can be opened from within Minecraft by")
print("clicking Singleplayer, then on the Select World page, selecting the savegame, clicking the Edit button, and then")
print("on the Edit World page clicking the Open World Folder button.")
print()
print("Before running this application, you must extract the loot tables from the current Minecraft version (the folder")
print("called 'loot_tables' and all of its sub-folders and files).  The loot_tables folder must be in the same folder as")
print("this application for the application to locate the loot tables and generate the data pack correctly.  In addition,")
print("the blockers.config, bottlenecks.config, and exclusions.config files must be in the current folder if customization")
print("is being used.\n\n")


# Prompt user for a PRNG seed

seed = input("Enter a seed (a number or text string). Leave blank for a system-generated random seed: ")
print()



# Set PRNG seed & datapack name based on user input.

if len(seed) > 0:
    print(f"Creating RLT datapack using the seed '{seed}'.")
    random.seed(seed)       # This seeds the PRNG with the input seed.
    datapack_name = 'RLT_{}'.format(seed)
    datapack_description = 'Memetics\' Random Loot Tables: seed = {}'.format(seed)
    datapack_filename = 'RLT (seed = ' + seed + ') for Minecraft ' + Minecraft_version + '.zip'
else:
    print("Creating RLT datapack using a random, system-generated seed (different for each run).\n")

    # The PRNG is already seeded with a system-determined random seed upon
    # import of the random module, so no need to call random.seed() here.
    # If in the future we allow multiple runs of system-determined
    # random seeds, though, we'll need to re-initialize with random.seed()
    # for each run.

    datapack_name = 'RLT_random_seed'
    datapack_description = 'Memetics\' Random Loot Tables: random seed'
    datapack_filename = 'RLT (random seed) for Minecraft ' + Minecraft_version + '.zip'

# If the data pack already exists, confirm over-writing it.

if os.path.isfile(os.path.join(datapack_folder, datapack_filename)):
    if len(seed) > 0:
        print(f"Warning: A datapack for seed '{seed}' already exists.")
        print("Making a new datapack with that seed will over-write the existing one.\n")
    else:
        print("Warning: A datapack for a system-generated random seed already exists.")
        print("Making a new random-seed datapack will over-write the existing one.\n")
    print("Do you wish to proceed?\n")
    choice = 'x'
    while choice[0].lower() != 'y':
        print("Enter 'Y' (yes) to generate a new datapack, over-writing the current datapack.")
        choice = input("Enter 'N' (no) to abort and exit the application: ")
        if choice[0].lower() == 'n':
            print("\nData pack generation canceled.  Exiting...")
            os.system('pause')
            sys.exit()
        if choice[0].lower() != 'y':
            print("\nPlease choose a valid option: (Y) to proceed or (N) to abort and exit.\n")

print("\nGenerating datapack.  This may take a moment, depending on the size of the loot table set...\n")


# Load exclusions list; remove blank lines and comment lines.

if os.path.isfile(exclusionsconfig):
    with open(exclusionsconfig, 'r') as exclusionsfile:
        print("Loading exclusions list")
        exclusions = exclusionsfile.read().split('\n')
        exclusions[:] = [x for x in exclusions if not (
                        x.lstrip() == '' or x.lstrip().startswith('#'))]
else:
    print(f"Warning: No exclusions list; '{exclusionsconfig}' file not found).")

# Load bottlenecks list; remove blank lines and comment lines.

if os.path.isfile(bottlenecksconfig):
    with open(bottlenecksconfig, 'r') as bottlenecksfile:
        print("Loading bottlenecks list")
        bottlenecks = bottlenecksfile.read().split('\n')
        bottlenecks[:] = [x for x in bottlenecks if not (
                        x.lstrip() == '' or x.lstrip().startswith('#'))]
else:
    print(f"Warning: No bottlenecks list; '{bottlenecksconfig}' file not found).")

# Load blockers list; remove blank lines and comment lines.

if os.path.isfile(blockersconfig):
    with open(blockersconfig, 'r') as blockersfile:
        print("Loading blockers list")
        blockers = blockersfile.read().split('\n')
        blockers[:] = [x for x in blockers if not (
                    x.lstrip() == '' or x.lstrip().startswith('#'))]
else:
    print(f"Warning: No blockers list; '{blockersconfig}' file not found).")

# Check for tables that appear on more than one config list.  (If there are
# duplicates, report them and then exit.)

checkcollisions(exclusions, bottlenecks, 'exclusions', 'bottlenecks')
checkcollisions(exclusions, blockers, 'exclusions', 'blockers')
checkcollisions(bottlenecks, blockers, 'bottlenecks', 'blockers')

# Load two-block objects list; remove blank lines and comment lines.

if os.path.isfile(two_block_objectsconfig):
    with open(two_block_objectsconfig, 'r') as two_block_objectsfile:
        print("Loading two-block objects list")
        two_block_objects = two_block_objectsfile.read().split('\n')
        two_block_objects[:] = [x for x in two_block_objects if not (
                            x.lstrip() == '' or x.lstrip().startswith('#'))]
else:
    print(f"Warning: '{two_block_objectsconfig}' file not found).")


###################################################################################
# Load loot tables file names from the loot_tables folder tree (including local
# relative paths), sorting them to table_names and table_names_blockers lists.

print(f"Scanning local {loot_tables_folder} folder tree for loot table files")

# Read the loot tables directory:
# First, add all of the blocks tables and entities tables to lists for use
# later when revising the tables (stripping out "killed by player" conditions,
# or etc.).  Next, build the preliminary sorted lists of loot tables.  Ignore
# file names that appear on the exclusions list, and then assign all remaining
# file names to the table_names lists (filtered by blockers) and also to the
# unassigned lists (filtered by bottlenecks).
    # Filtered file names get assigned to either the table_names_blockers list
    # or the unassigned_bottlenecks list.

# Load the file names and relative paths for each loot tables sub-folder
# into their respective lists.  (Only doing blocks & entities for now, so
# we know which tables are in those categories for the table revision /
# clean-up step.)  Skip the loot tables in the exclusions list.  (Report
# each skipped file to print output.)
#
# Add bottlenecks files to table_names (allow bottleneck names to have
# bottleneck drops), but instead of adding them to unassigned, put them in
# the special unassigned_bottlenecks list for priority assignment.
#
# Add blockers files to the unassigned list but not the main table_names
# list: keep them in the separate table_names_blockers list until the
# bottlenecks drops have been assigned.  Then later we'll return them to
# the main table_names list for assignment with the rest.
#
# Add all other (non-special) tables to both table_names and unassigned.

for dirpath, dirnames, filenames in os.walk(loot_tables_folder):
    for filename in filenames:
        if dirpath == os.path.join(loot_tables_folder, 'blocks'):
            blocks_table_names.append(filename)
        if dirpath == os.path.join(loot_tables_folder, 'entities'):
            entity_table_names.append(filename)
        if filename in exclusions:
            print(f"  Skipping excluded loot table: {filename}")
        elif filename in bottlenecks:
            table_names.append(os.path.join(dirpath, filename))
            unassigned_bottlenecks.append(os.path.join(dirpath, filename))
        elif filename in blockers:
            table_names_blockers.append(os.path.join(dirpath, filename))
            unassigned.append(os.path.join(dirpath, filename))
        else:
            table_names.append(os.path.join(dirpath, filename))
            unassigned.append(os.path.join(dirpath, filename))


###################################################################################
# Randomization procedures

# Assign the bottlenecks drops to random, non-blocker table_names:
# Go through the table_names list and give each a random drops assignment from
# the unassigned list.  Pick random loot table file name from table_names for
# each unassigned_bottlenecks drop, and assign them to the assignments
# dictionary as key(table_names): value(unassigned_bottlenecks).  Then delete
# the table_names entry for each: This way we don't later try to assign a
# different unassigned drop value to a previously assigned table_names key.

if len(unassigned_bottlenecks) > 0:
    print("Assigning bottleneck drops to random non-blocker tables")
    for drop in unassigned_bottlenecks:
        i = random.randint(0, len(table_names)-1)
        assignments[table_names[i]] = drop
        del table_names[i]

# Now that the bottlenecks have been taken care of, add table_names_blockers
# to the main table_names list.  Then all the remaining table_names names and
# unassigned drops will be ready for assignment.

if len(table_names_blockers) > 0:
    print("Moving blockers to main tables list")
    for blockername in table_names_blockers:
        table_names.append(blockername)

# About to complete remaining assignments: Report status (varying by whether
# or not there were bottlenecks assignments).

if len(assignments) > 0:
    print("Assigning random drops for remaining loot tables")
else:
    print("Assigning random drops for all loot tables")

# Make sure table_names and unassigned lists have same number of elements.
# (Note: We probably don't need this error check.)

if len(table_names) != len(unassigned):
    print("Error: table_names list and unassigned list contain different items or different numbers of elements.")
    os.system('pause')
    sys.exit()

# Complete all of the remaining table --> drop assignments: For each
# table_names name, assign a random unassigned drop (add as key:value
# to the assignments dictionary).

for name in table_names:
    i = random.randint(0, len(unassigned)-1)
    assignments[name] = unassigned[i]
    del unassigned[i]


################################################################################
# File contents prep

# Load the default loot tables (the actual JSON content of each table) from
# the default files.  Call the function 'revise_contents' to conditionally
# alter the loot tables, correcting problems such as removing checks for
# certain impossible drop conditions.

# For each key in the assignments dict, load the file contents as JSON,
# revise those contents as needed, and then convert back to JSON and store
# in new_tables dict (the newly revised version of the assignments dict).

print("Updating the tables to correct broken drop conditions")
for filename in assignments:
    try:
        with open(assignments[filename],'r') as file:
            new_tables[filename] = json.dumps(revise_contents(filename, assignments[filename], json.loads(file.read())), indent = 2)
    except Exception as ex:
        print(f"An error occurred with creating new_tables list: {ex}\n")
        print("Exiting...")
        os.system('pause')
        sys.exit()


################################################################################
# RLT post-game forensics info prep

# Create new dictionary of assignments by file names only (strip out the
# path elements) using a dictionary comprehension.  This will be used to
# create a text file with a listing of all assignments sorted by file name
# for game post-mortem analysis.

basename_assignments = {os.path.basename(key): os.path.basename(assignments[key]) for key in assignments}


################################################################################
# Build the datapack .zip file.


print("Building datapack zip file\n")

# Build the zip file contents.

# Assign zipdata as a file-like object which will be the container for the
# binary stream data that follows.  Then assign zf as a zipfile object,
# which will handle operations for writing zipfile contents to zipdata in
# memory prior to the file write operation.

zipdata = io.BytesIO()
with zipfile.ZipFile(zipdata, 'w', zipfile.ZIP_DEFLATED, False) as zf:

    # Write the loot tables assignments to two text files (sorted by loot
    # tables tree; sorted by table file name) for post-game analysis and
    # troubleshooting (add both to zf).

    # Create fc as a text stream to contain the following text (in the "with"
    # block), which is stored in a variable and then written to the text file.

    with io.StringIO() as fc:

        # Write this content at the start of fc (= top of the text file).

        fc.write(f"RLT datapack: {datapack_name}\n")
        fc.write(f"Datapack file name: {datapack_filename}\n\n")
        fc.write("Loot table assignments sorted by loot table tree path:\n\n")

        # For each dictionary entry in assignments, sorted by key (path +
        # filename), add each key (path + filename) and its value (filename
        # only) to fc. (The file=fc element makes it print to the file.)

        for key, value in sorted(assignments.items()): print(
                f"{key} --> {os.path.basename(value)}", file=fc)

        # Assign the value of fc to a variable, so we can write the file
        # from there.

        assignments_by_tree = fc.getvalue()

    # Write the text file into the .zip file.

    zf.writestr("RLT_info/Loot table assignments by tree.txt", assignments_by_tree)

    # Create fc as a text stream to contain the following text (in the "with"
    # block), which is stored in a variable and then written to the text file.

    with io.StringIO() as fc:

        # Write this content at the start of fc (= top of the text file).

        fc.write(f"RLT datapack: {datapack_name}\n")
        fc.write(f"Datapack file name: {datapack_filename}\n\n")
        fc.write("Loot table assignments by file:\n\n")

        # For each dictionary entry in basename_assignments, sorted by key
        # (filename): add each key (filename only) and its value (filename
        # only) to fc. (The file=fc element makes it print to the file.)

        for key, value in sorted(basename_assignments.items()): print(
                f"{key} --> {value}", file=fc)

        # Assign the value of fc to a variable, so we can write the file
        # from there.

        assignments_by_file = fc.getvalue()

    # Write the text file, adding it to the .zip file object.

    zf.writestr('RLT_info/Loot table assignments by file.txt', assignments_by_file)

    # For each "key" (loot table file name) in new_tables, add to the zip file
    # a file with that name but with the "value" loot table file's contents.

    for lootfile, contents in new_tables.items():
        zf.writestr(os.path.join('data/minecraft/', lootfile), contents)

    # Write the rest of the Minecraft-required datapack files.

    zf.writestr('pack.mcmeta', json.dumps({'pack':{'pack_format':datapack_format, 'description':datapack_description}}, indent=4))
    zf.writestr('data/minecraft/tags/functions/load.json', json.dumps({'values':['{}:reset'.format(datapack_name.lower())]}))
    zf.writestr('data/{}/functions/reset.mcfunction'.format(datapack_name.lower()), 'tellraw @a ["",{"text":"Memetics\' RLT: Random Loot Tables","color":"green"}]')

# Check the current folder for the RLT datapacks folder; if it does not
# exist, create it.

print(f"Writing datapack file to folder: {datapack_folder}\n")
try:
    if not os.path.isdir(datapack_folder):
        os.mkdir(datapack_folder)
except Exception as ex:
    print(f"An error occurred.  Error message: {ex}\n")
    print("Exiting...")
    os.system('pause')
    sys.exit()

# Now write the actual .zip file to the datapack folder using the zip file
# contents we just created in the zipdata file-like object.

try:
    with open(os.path.join(datapack_folder, datapack_filename), 'wb') as file:
        file.write(zipdata.getvalue())
except Exception as ex:
    print(f"An error occurred.  Error message: {ex}\n")
    print("Exiting...")
    os.system('pause')
    sys.exit()

# Report success, pause for keystroke, and then exit.

print(f"Datapack '{datapack_filename}' was created successfully.\n")

os.system('pause')
sys.exit()
