import typing
from . import Items, ItemNames
from .MissionTables import campaign_mission_table, SC2Campaign, SC2Mission

"""
Item name groups, given to Archipelago and used in YAMLs and /received filtering.
For non-developers the following will be useful:
* Items with a bracket get groups named after the unbracketed part
  * eg. "Advanced Healing AI (Medivac)" is accessible as "Advanced Healing AI"
  * The exception to this are item names that would be ambiguous (eg. "Resource Efficiency")
* Item flaggroups get unique groups as well as combined groups for numbered flaggroups
  * eg. "Unit" contains all units, "Armory" contains "Armory 1" through "Armory 6"
  * The best place to look these up is at the bottom of Items.py
* Items that have a parent are grouped together
  * eg. "Zergling Items" contains all items that have "Zergling" as a parent
  * These groups do NOT contain the parent item
  * This currently does not include items with multiple potential parents, like some LotV unit upgrades
* All items are grouped by their race ("Terran", "Protoss", "Zerg", "Any")
* Hand-crafted item groups can be found at the bottom of this file
"""

item_name_groups: typing.Dict[str, typing.List[str]] = {}

# Groups for use in world logic
item_name_groups["Missions"] = ["Beat " + mission.mission_name for mission in SC2Mission]
item_name_groups["WoL Missions"] = ["Beat " + mission.mission_name for mission in campaign_mission_table[SC2Campaign.WOL]] + \
                                   ["Beat " + mission.mission_name for mission in campaign_mission_table[SC2Campaign.PROPHECY]]

# These item name groups should not show up in documentation
unlisted_item_name_groups = {
    "Missions", "WoL Missions"
}

# Some item names only differ in bracketed parts
# These items are ambiguous for short-hand name groups
bracketless_duplicates: typing.Set[str]
# This is a list of names in ItemNames with bracketed parts removed, for internal use
_shortened_names = [(name[:name.find(' (')] if '(' in name else name)
      for name in [ItemNames.__dict__[name] for name in ItemNames.__dir__() if not name.startswith('_')]]
# Remove the first instance of every short-name from the full item list
bracketless_duplicates = set(_shortened_names)
for name in bracketless_duplicates:
    _shortened_names.remove(name)
# The remaining short-names are the duplicates
bracketless_duplicates = set(_shortened_names)
del _shortened_names

# All items get sorted into their data type
for item, data in Items.get_full_item_list().items():
    # Items get assigned to their flaggroup's display type
    item_name_groups.setdefault(data.type.display_name, []).append(item)
    # Items with a bracket get a short-hand name group for ease of use in YAMLs
    if '(' in item:
        short_name = item[:item.find(' (')]
        # Ambiguous short-names are dropped
        if short_name not in bracketless_duplicates:
            item_name_groups[short_name] = [item]
            # Short-name groups are unlisted
            unlisted_item_name_groups.add(short_name)
    # Items with a parent get assigned to their parent's group
    if data.parent_item:
        # The parent groups need a special name, otherwise they are ambiguous with the parent
        parent_group = f"{data.parent_item} Items"
        item_name_groups.setdefault(parent_group, []).append(item)
        # Parent groups are unlisted
        unlisted_item_name_groups.add(parent_group)
    # All items get assigned to their race's group
    race_group = data.race.name.capitalize()
    item_name_groups.setdefault(race_group, []).append(item)


# Hand-made groups
class ItemGroupNames:
    TERRAN_UNITS = "Terran Units"
    ZERG_UNITS = "Zerg Units"
    PROTOSS_UNITS = "Protoss Units"

    BARRACKS_UNITS = "Barracks Units"
    FACTORY_UNITS = "Factory Units"
    STARPORT_UNITS = "Starport Units"
    NOVA_EQUIPMENT = "Nova Equipment"
    TERRAN_BUILDINGS = "Terran Buildings"
    TERRAN_MERCENARIES = "Terran Mercenaries"

    GATEWAY_UNITS = "Gateway Units"
    ROBO_UNITS = "Robo Units"
    STARGATE_UNITS = "Stargate Units"
    PROTOSS_BUILDINGS = "Protoss Buildings"
    AIUR = "Aiur"
    NERAZIM = "Nerazim"
    TAL_DARIM = "Tal'Darim"
    PURIFIER = "Purifier"


item_name_groups[ItemGroupNames.TERRAN_UNITS] = terran_units = [
    item_name for item_name, item_data in Items.item_table.items()
    if item_data.type in (Items.TerranItemType.Unit, Items.TerranItemType.Mercenary, Items.TerranItemType.Building)
]
item_name_groups[ItemGroupNames.ZERG_UNITS] = zerg_units = [
    item_name for item_name, item_data in Items.item_table.items()
    if item_data.type in (Items.ZergItemType.Unit, Items.ZergItemType.Mercenary, Items.ZergItemType.Morph)
]
item_name_groups[ItemGroupNames.PROTOSS_UNITS] = protoss_units = [
    item_name for item_name, item_data in Items.item_table.items()
    if item_data.type in (Items.ProtossItemType.Unit, Items.ProtossItemType.Unit_2, Items.ProtossItemType.Building)
]

# Terran
item_name_groups[ItemGroupNames.BARRACKS_UNITS] = barracks_units = [
    ItemNames.MARINE, ItemNames.MEDIC, ItemNames.FIREBAT, ItemNames.MARAUDER,
    ItemNames.REAPER, ItemNames.GHOST, ItemNames.SPECTRE, ItemNames.HERC,
]
item_name_groups[ItemGroupNames.FACTORY_UNITS] = factory_units = [
    ItemNames.HELLION, ItemNames.VULTURE, ItemNames.GOLIATH, ItemNames.DIAMONDBACK,
    ItemNames.SIEGE_TANK, ItemNames.THOR, ItemNames.PREDATOR, ItemNames.WIDOW_MINE,
    ItemNames.CYCLONE, ItemNames.WARHOUND,
]
item_name_groups[ItemGroupNames.STARPORT_UNITS] = starport_units = [
    ItemNames.MEDIVAC, ItemNames.WRAITH, ItemNames.VIKING, ItemNames.BANSHEE,
    ItemNames.BATTLECRUISER, ItemNames.HERCULES, ItemNames.SCIENCE_VESSEL, ItemNames.RAVEN,
    ItemNames.LIBERATOR, ItemNames.VALKYRIE,
]
item_name_groups[ItemGroupNames.TERRAN_BUILDINGS] = terran_buildings = [
    item_name for item_name, item_data in Items.item_table.items()
    if item_data.type == Items.TerranItemType.Building
]
item_name_groups[ItemGroupNames.TERRAN_MERCENARIES] = terran_mercenaries = [
    item_name for item_name, item_data in Items.item_table.items()
    if item_data.type == Items.TerranItemType.Mercenary
]
item_name_groups[ItemGroupNames.NOVA_EQUIPMENT] = nova_equipment = [
    *[item_name for item_name, item_data in Items.item_table.items()
        if item_data.type == Items.TerranItemType.Nova_Gear],
    ItemNames.NOVA_PROGRESSIVE_STEALTH_SUIT_MODULE,
]

# Protoss
item_name_groups[ItemGroupNames.GATEWAY_UNITS] = gateway_units = [
    ItemNames.ZEALOT, ItemNames.CENTURION, ItemNames.SENTINEL, ItemNames.SUPPLICANT,
    ItemNames.STALKER, ItemNames.INSTIGATOR, ItemNames.SLAYER,
    ItemNames.SENTRY, ItemNames.HAVOC, ItemNames.ENERGIZER,
    ItemNames.DRAGOON, ItemNames.ADEPT, ItemNames.DARK_ARCHON,
    ItemNames.HIGH_TEMPLAR, ItemNames.SIGNIFIER, ItemNames.ASCENDANT,
    ItemNames.DARK_TEMPLAR, ItemNames.AVENGER, ItemNames.BLOOD_HUNTER,
]
item_name_groups[ItemGroupNames.ROBO_UNITS] = robo_units = [
    ItemNames.WARP_PRISM, ItemNames.OBSERVER,
    ItemNames.IMMORTAL, ItemNames.ANNIHILATOR, ItemNames.VANGUARD,
    ItemNames.COLOSSUS, ItemNames.WRATHWALKER,
    ItemNames.REAVER, ItemNames.DISRUPTOR,
]
item_name_groups[ItemGroupNames.STARGATE_UNITS] = stargate_units = [
    ItemNames.PHOENIX, ItemNames.MIRAGE, ItemNames.CORSAIR,
    ItemNames.VOID_RAY, ItemNames.DESTROYER,
    ItemNames.SCOUT, ItemNames.TEMPEST,
    ItemNames.CARRIER, ItemNames.MOTHERSHIP,
    ItemNames.ARBITER, ItemNames.ORACLE,
]
item_name_groups[ItemGroupNames.PROTOSS_BUILDINGS] = protoss_buildings = [
    item_name for item_name, item_data in Items.item_table.items()
    if item_data.type == Items.ProtossItemType.Building
]
item_name_groups[ItemGroupNames.AIUR] = [
    ItemNames.ZEALOT, ItemNames.DRAGOON, ItemNames.SENTRY, ItemNames.AVENGER, ItemNames.HIGH_TEMPLAR,
    ItemNames.IMMORTAL, ItemNames.REAVER,
    ItemNames.PHOENIX, ItemNames.SCOUT, ItemNames.ARBITER, ItemNames.CARRIER,
]
item_name_groups[ItemGroupNames.NERAZIM] = [
    ItemNames.CENTURION, ItemNames.STALKER, ItemNames.DARK_TEMPLAR, ItemNames.SIGNIFIER, ItemNames.DARK_ARCHON,
    ItemNames.ANNIHILATOR,
    ItemNames.CORSAIR, ItemNames.ORACLE, ItemNames.VOID_RAY,
]
item_name_groups[ItemGroupNames.TAL_DARIM] = [
    ItemNames.SUPPLICANT, ItemNames.SLAYER, ItemNames.HAVOC, ItemNames.BLOOD_HUNTER, ItemNames.ASCENDANT,
    ItemNames.VANGUARD, ItemNames.WRATHWALKER,
    ItemNames.DESTROYER, ItemNames.MOTHERSHIP,
    ItemNames.WARP_PRISM_PHASE_BLASTER,
]
item_name_groups[ItemGroupNames.PURIFIER] = [
    ItemNames.SENTINEL, ItemNames.ADEPT, ItemNames.INSTIGATOR, ItemNames.ENERGIZER,
    ItemNames.COLOSSUS, ItemNames.DISRUPTOR,
    ItemNames.MIRAGE, ItemNames.TEMPEST,
]

# Sanity checks
assert len(terran_units) == len(barracks_units) + len(factory_units) + len(starport_units) + len(terran_buildings) + len(terran_mercenaries)
assert len(protoss_units) == len(gateway_units) + len(robo_units) + len(stargate_units) + len(protoss_buildings)
