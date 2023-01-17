# Memetics' Random Loot Tables

Generates datapacks for (Java) Minecraft that randomize the loot tables, resulting in different (but consistent) random drops from objects, chests, entities, and gameplay elements such as fishing.  Chaotic fun!

<!--
/discord/:553903039082135555
/github/search/:user/:repo/:query
-->
<p align="center"> centered text 

[![Current Version](https://img.shields.io/badge/version-0.15.4.beta-blueviolet.svg)](https://github.com/MemeticsX/RLT) [![Searched count](https://img.shields.io/github/search/:MemeticsX/:RLT/:random-A8CC9D.svg)]() [![Total Downloads](https://img.shields.io/github/downloads/MemeticsX/RLT/total)](https://github.com/MemeticsX/RLT) [![GitHub Issues](https://img.shields.io/github/issues/MemeticsX/RLT.svg)](https://github.com/MemeticsX/RLT/issues) [![Discord](https://img.shields.io/discord/:553903039082135555)](https://discord.gg/guTcuM5V62)

...aaaaaand break!</p>
  
[![github release version](https://img.shields.io/github/v/release/nhn/tui.editor.svg?include_prereleases)](https://github.com/nhn/tui.editor/releases/latest) [![npm version](https://img.shields.io/npm/v/@toast-ui/editor.svg)](https://www.npmjs.com/package/@toast-ui/editor) [![license](https://img.shields.io/github/license/nhn/tui.editor.svg)](https://github.com/nhn/tui.editor/blob/master/LICENSE) [![PRs welcome](https://img.shields.io/badge/PRs-welcome-ff69b4.svg)](https://github.com/nhn/tui.editor/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) 

<p align="center">
  <a href="https://badge.fury.io/js/electron-markdownify">
    <img src="https://badge.fury.io/js/electron-markdownify.svg"
         alt="Gitter">
  </a>
  <a href="https://gitter.im/amitmerchant1990/electron-markdownify"><img src="https://badges.gitter.im/amitmerchant1990/electron-markdownify.svg"></a>
  <a href="https://saythanks.io/to/bullredeyes@gmail.com">
      <img src="https://img.shields.io/badge/SayThanks.io-%E2%98%BC-1EAEDB.svg">
  </a>
  <a href="https://www.paypal.me/AmitMerchant">
    <img src="https://img.shields.io/badge/$-donate-ff69b4.svg?maxAge=2592000&amp;style=flat">
  </a>
</p>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#download">Download</a> •
  <a href="#credits">Credits</a> •
  <a href="#related">Related</a> •
  <a href="#license">License</a>
</p>

*PLACEHOLDER: A nice animated image showing RLT in action.*


---

## Table of Contents 🚩

- [Features](#-features)
- [How It Works](#-how-it-works)
- [Getting Started](#-getting-started)
- [--Preparing the loot_tables folder](#preparing-the-loot_tables-folder)
- [--Creating and using RLT datapacks](#creating-and-using-rlt-datapacks)
- [Configuration](#-configuration)
- [--Config Files](#config-files)
- [--Recommended Configuration](#recommended-configuration)
- [Release History](#-release-history)
- [License](#-license)
- [Connect!](#-connect)
- [Support RLT](#-support-rlt)

---


## 📦🎨 Features

* [Viewer](https://github.com/nhn/tui.editor/tree/master/docs/en/viewer.md) : Supports a mode to display only markdown data without an editing area.
* [Internationalization (i18n)](https://github.com/nhn/tui.editor/tree/master/docs/en/i18n.md) : Supports English, Dutch, Korean, Japanese, Chinese, Spanish, German, Russian, French, Ukrainian, Turkish, Finnish, Czech, Arabic, Polish, Galician, Swedish, Italian, Norwegian, Croatian + language and you can extend.
* [Widget](https://github.com/nhn/tui.editor/tree/master/docs/en/widget.md) : This feature allows you to configure the rules that replaces the string matching to a specific `RegExp` with the widget node.
* [Custom Block](https://github.com/nhn/tui.editor/tree/master/docs/en/custom-block.md) : Nodes not supported by Markdown can be defined through custom block. You can display the node what you want through writing the parsing logic with custom block.

Some degree of customization through the table lists in the config files.  

The code here is provided as-is and is not actively supported, though the developer (Memetics / current Github username: viralmeme) intends to update the code from time to time. For discussion of the project, please visit the Mining after Dark Discord: see source code for link.


## How It Works 🔧

Memetics' Random Loot Tables (RLT) loads copies of the default (Java) Minecraft loot tables.  Based on a user-provided or system-determined random seed, it randomly redistributes the loot tables' contents.  The randomization is modified based on the RLT configuration settings, which allows it to avoid problematic drop assignments that would prevent game progression or make progression overly difficult and frustrating.  The resulting assignments are revised to correct issues such as now-impossible conditions checks like the "killed by player" condition applied to a non-entity.  Then the table set is written to a new datapack .zip file, which is ready to add to a new or existing Minecraft world.


## Getting Started ▶

### Prerequisites

Requirements for the software and other tools to build, test and push 
- [Example 1](https://www.example.com)
- [Example 2](https://www.example.com)


### Preparing the loot_tables folder

<details>

<summary>"Click to expand"</summary>

Memetics' Random Loot Tables (RLT) needs to have access to a copy of the Minecraft "loot_tables" folder, with all of its files and sub-folders and their files.  RLT will not run without the loot_tables folder being added to the RLT folder.

The loot_tables folder must be extracted from your current (Java) Minecraft game installation (or more specifically, from the version of the game corresponding with this version of RLT) and copied to the RLT application folder.  (For RLT 1.15.4 (beta), the RLT configuration (.config) files (2-block_objects.config, blockers.config, bottlenecks.config, and exclusions.config) also must be in the RLT folder.

_To extract the "loot_tables" folder from your Minecraft installation_:

1. In Windows File Explorer, navigate to the current Minecraft installation folder, which in Windows is normally found in %AppData%/.minecraft/versions/[version]/[version].jar/data/minecraft/loot_tables.  (For the current RLT build, the [version] folder is named "1.19.3".)

If you are unsure how to locate the loot_tables folder, start by pasting this into the location bar in the Windows File Explorer:

%AppData%/.minecraft/versions/

Then in the "versions" folder, open the folder named with the current Minecraft version: for instance, the folder named 1.19.3.  (The folder will not exist until you first launch that version of the game; so if the folder does not exist, open the Minecraft launcher and start that version of the game, so the Minecraft launcher will download all of the files necessary to run that version of the game.)

If you are unable to locate the Minecraft root installation folder, Minecraft may be installed in a different location on your system.  Wherever it is located, navigate to the root ".minecraft" folder where the game is installed, open the "versions" folder, and then locate the folder for the current version of the game.

2. In the [version] folder, open the compressed [version].jar file using a file compression utility such as 7Zip.  (For instance, in the folder 1.19.3, the file will be called 1.19.3.jar.)

3. In the compressed .jar file, open the "data" folder, and then open the "minecraft" folder.

4. In the "minecraft" folder, extract the "loot_tables" folder, copying it into the RLT folder.

5. Once the loot_tables folder and its contents have been extracted into the RLT folder, the RLT application should now be able to run.

</details>


### Creating and using RLT datapacks

<details>

<summary>"Expand / Contract"</summary>

When you run the RLT application, it will prompt you for a seed to use for randomizing the loot tables.  If you use the same seed and the same set of loot tables and config files, the application will generate the same (identical) datapack each time.  If you do not enter a seed, RLT will use a system-generated random seed.  Every time RLT is launched, the system-generated seed is generated at random, resulting in a different datapack each time.  (So if you want to produce the same datapack each time, manually enter the same seed each time.)

Once RLT generates a new datapack, it writes the datapack as a .zip file to the "RLT datapacks" folder in the RLT folder.  If you provided a seed, the file name will include the seed.

Copy the RLT datapack .zip file to the "datapacks" folder located in the savegame folder for a new or existing Minecraft world, and the loot drops will be randomized.


#### To add the RLT datapack to a new Minecraft world:

<details>
  
<summary>"Expand / Contract"</summary>
  
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

</details>


#### To add the RLT datapack to an existing Minecraft world:

<details>
<summary>"Expand / Contract"</summary>
  
- Exit the world (if it is currently open in Minecraft).
- In File Explorer, navigate to the savegame folder for the world.  (By default, this folder is located in %AppData%/.minecraft/saves/.  However, you can also open the world save folder from within Minecraft: Select the world on the Singleplayer menu, click Edit, and then click "Open World Folder.")
- In the world's savegame folder, open the datapacks folder.
- Copy the RLT datapack .zip file into the datapacks folder.
- Resume playing the world.  The loot drops should now be randomzied.

</details>

</details>


## Configuration 📊

### Config files

The lists in the configuration files are used primarily to prevent loot table assignments that block game progress, such as assigning blaze rods to drop from an End chest when blaze rods are needed to gain access to the End in the first place. The config lists also allow the exclusion of certain loot tables from random assignments, such as table assignments that would make the game too frustrating to play. For instance, if blaze rods only dropped from certain infested blocks, it might take a frustratingly long time of random digging before locating those blocks in the hope that blaze rods could be obtained from them.

**The [bottlenecks.config](bottlenecks.config) file** holds the list of loot tables for loot that is needed for progression.  By default, it contains blaze.json and enderman.json, since ender pearls and blaze powder are needed to help locate strongholds and activate the End portals to allow passage to the End.  Technically, ender pearls can also be found from Piglin bartering (as of Minecraft 1.16), so ender pearls could still be found even if Enderman drops are not available, but if both of those bottlenecks get assigned to drop from objects or entities exclusive to the End, progress will still be impossible.  (For a more cautious configuration, piglin_bartering.json could also be added to the bottlenecks.config list.)

**The [blockers.config](blockers.config) file** holds the list of loot tables that RLT will avoid assigning the drops from tables listed in bottlenecks.config.  This way, the important bottlenecks drops will not be overly difficult if not impossible to find.  Probably nobody wants to dig around all over the world at random to try to locate an infested diorite vein in the hope that maybe it will drop an ender pearl or two, and no one wants the starting bonus chest to be the only place where one can find a blaze rod.  We might still want those items' drops to be assigned elsewhere, but we don't want those to be the only droppers of important resources.  So the blockers tables are withheld from the assignment pool until the bottlenecks tables have been assigned to non-blockers from the general (non-blocker, non-excluded) unassigned tables list; then the blockers are added to the general assignment list for random assignment with the rest of the pool.

**The [exclusions.config](exclusions.config) file** holds the list of loot tables that will not be altered; the tables in this list will remain unrandomized.  This list contains:

- showstoppers: things that won't drop anything, potentially preventing important resources from dropping, since they're not implemented (in the case of certain entities like Giant and Zombie Horse as well as tables for future objects and entities that have not yet been implemented (and therefore are empty currently); and
- killjoys (a.k.a. frustrators): tables which, if included in the randomized loot (either as droppers or to have their loot dropped by something else), would make the game significantly less fun.  The items on this list are less problematic for game progression and are more a matter of taste.


### Recommended Configuration

To prevent assignments that block game progression, such as blaze rods being assigned to drop from chests or entities only found in the End, the default blockers and bottlenecks lists generally should be kept as they are, although piglin_bartering.json could be added to bottlenecks.config to help ensure the availability of ender pearls.

At the very least, keep blaze.json and _either_ enderman.json or piglin_bartering.json in the bottlenecks.config list, and keep very rare or hard-to-find droppers (such as spawn_bonus_chest.json and the infested blocks) in the blockers.config list.  

The default showstoppers and "not yet implemented" lists in exclusions.config should also be kept as-is.

However, the killjoys list (in exclusions.config) can be modified as desired.  Additional loot tables may be added to the killjoys list if you want to reduce the frustration of having to hunt for days on end to find certain hard-to-find loot drops, or if you have certain tables that you simply want to have retain their normal drops.

<ul>
Memetics finds it tedious to have 17 varieties of candle and another 17 varieties of candle cake dropping candles as part of the randomized loot set, taking up 34 of the drops, and having the unbreakable cakes assigned other items' loot tables (and thus being unable to produce those drops), so those 34 tables are included on the default killjoys list.  Memetics also (currently) likes to have shulker_box.json on the list and therefore unrandomized, so that at least one type of shulker box is available as a reusable shulker box for gameplay.  But YMMV.
</ul>

Feel free to experiment, though!  The config lists may be modified or even removed entirely, and RLT will still generate datapacks - and you still might get lucky with what items get dropped from where, but ultimately, you will have to be the judge of the results of such experiments.


## Release History 📅

RLT follows [semantic versioning](http://semver.org/). For the release history, see the version [tags in the RLT GitHub repository](https://github.com/MemeticsX/RLT/tags).


## License 📜

Distributed under the GNU GPL 3.0 license. See the [LICENSE](LICENSE) file for more information.


## Connect 🌏

Join the discussion of RLT on [the Mining after Dark Discord server](https://discord.gg/guTcuM5V62).  You can also report issues with installing or running Memetics' RLT on [the RLT GitHub repository](https://github.com/MemeticsX/RLT).


## Support RLT 🚀

If you like this project, please consider showing your support (thanks!):

(No Patreon yet or whatever; for now, just consider dropping by the Mining after Dark Discord to say thanks.  :-)

---


📦 I hope you enjoy using RLT and playing Minecraft with random loot tables!  :D
-Memetics
