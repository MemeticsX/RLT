Memetics' Random Loot Tables for Minecraft

================================
Preparing the loot_tables folder
================================

Memetics' Random Loot Tables (RLT) needs to have access to a copy of the Minecraft "loot_tables" folder, with all of its files and sub-folders and their files.  RLT will not run without the loot_tables folder being added to the RLT folder.

The loot_tables folder must be extracted from your current (Java) Minecraft game installation (or more specifically, from the version of the game corresponding with this version of RLT) and copied to the RLT application folder.  (For RLT 1.15.4 (beta), the RLT configuration (.config) files (2-block_objects.config, blockers.config, bottlenecks.config, and exclusions.config) also must be in the RLT folder.

To extract the "loot_tables" folder from your Minecraft installation:

1. In Windows File Explorer, navigate to the current Minecraft installation folder, which in Windows is normally found in %AppData%/.minecraft/versions/[version]/[version].jar/data/minecraft/loot_tables.  (For the current RLT build, the [version] folder is named "1.19.3".)

If you are unsure how to locate the loot_tables folder, start by pasting this into the location bar in the Windows File Explorer:

%AppData%/.minecraft/versions/

Then in the "versions" folder, open the folder named with the current Minecraft version: for instance, the folder named 1.19.3.  (The folder will not exist until you first launch that version of the game; so if the folder does not exist, open the Minecraft launcher and start that version of the game, so the Minecraft launcher will download all of the files necessary to run that version of the game.)

If you are unable to locate the Minecraft root installation folder, Minecraft may be installed in a different location on your system.  Wherever it is located, navigate to the root ".minecraft" folder where the game is installed, open the "versions" folder, and then locate the folder for the current version of the game.

2. In the [version] folder, open the compressed [version].jar file using a file compression utility such as 7Zip.  (For instance, in the folder 1.19.3, the file will be called 1.19.3.jar.)

3. In the compressed .jar file, open the "data" folder, and then open the "minecraft" folder.

4. In the "minecraft" folder, extract the "loot_tables" folder, copying it into the RLT folder.

5. Once the loot_tables folder and its contents have been extracted into the RLT folder, the RLT application should now be able to run.

Please visit our GitHub repository to report any problems you encounter with installing or running the RLT application: https://github.com/MemeticsX/RLT/discussions.


================================
Creating and using RLT datapacks
================================

When you run the RLT application, it will prompt you for a seed to use for randomizing the loot tables.  If you use the same seed and the same set of loot tables and config files, the application will generate the same (identical) datapack each time.  If you do not enter a seed, RLT will use a system-generated random seed.  Every time RLT is launched, the system-generated seed is generated at random, resulting in a different datapack each time.  (So if you want to produce the same datapack each time, manually enter the same seed each time.)

Once RLT generates a new datapack, it writes the datapack as a .zip file to the "RLT datapacks" folder in the RLT folder.  If you provided a seed, the file name will include the seed.

Copy the RLT datapack .zip file to the "datapacks" folder located in the savegame folder for a new or existing Minecraft world, and the loot drops will be randomized.


Adding the RLT datapack to a new Minecraft world:
------------------------------------------------

If you want to create a new world in which the loot tables start randomized (this works in Minecraft version 1.17 and later):

- On the Singleplayer* menu, click "Create New World."
- In the "Create New World" form, click "Data Packs."
- In the "Select Data Packs" form, click "Open Pack Folder."  The datapacks folder for the new world will open in a new File Explorer window.  (The files for the new world are located in a temporary folder until world creation is finalized.)
- Copy the newly generated RLT datapack from the "RLT datapacks" folder into the new world's "datapacks" folder.  (Once the file is added to the folder, the File Explorer window showing the new world's "datapacks" folder may be closed.)
- Switch back to Minecraft: The datapack should now appear in the "Available" list.
- Click the RLT datapack icon to move the datapack to the "Selected" list, and then click "Done."
- Update any other world creation settings as desired.
- Finally, click "Create New World" to finish world creation and launch your new RLT world!

* The process is simliar for Mulitplayer worlds.  However, if you are running the standalone Minecraft server, you may have to launch the server to let it create the new world for the first time (so that the world savegame folder and its "datapacks" folder will be created), stop the server, add the RLT datapack to the world's datapacks folder, and then restart the server.


To add the RLT datapack to an existing Minecraft world:
------------------------------------------------------

- Exit the world (if it is currently open in Minecraft).
- In File Explorer, navigate to the savegame folder for the world.  (By default, this folder is located in %AppData%/.minecraft/saves/.  However, you can also open the world save folder from within Minecraft: Select the world on the Singleplayer menu, click Edit, and then click "Open World Folder.")
- In the world's savegame folder, open the datapacks folder.
- Copy the RLT datapack .zip file into the datapacks folder.
- Resume playing the world.  The loot drops should now be randomzied.



I hope you enjoy using RLT and playing Minecraft with random loot tables!  :D
-Memetics
