import pickle,math,sys,os,string,shutil
import numpy as np
import pandas as pd
from opentrons import protocol_api

path = os.getcwd()

metadata = {
    'protocolName': 'Single Volume Dispense Protocol',
    'author': 'Madison Wahlsten @madisonwahlsten',
    'description': '''This protocol is meant to mimick the Mantis Liquid Handler by distributing a set volume of liquid to wells of as many 384-well or 96-well plates as needed from a reservoir.
    To use, please generate experiment parameters using generateSingleDispenseList.py and reanalyzing this protocol through the Opentrons app.
    Volume Range: 1 - 300 uL
    Plate Types: Costar 96-well v-bottom, PlateOne 384-well conical bottom
    Number of Plates: 8''',
    'apiLevel': '2.13'
}


'''
--------------------------------------------------------------------------------------------------------------------
'''


def run(protocol):
    protocol.set_rail_lights(True)
    if not protocol.is_simulating():
        dispenseParameters = pickle.load(open('/data/user_storage/BenchItems.pkl', 'rb'))
    else:
        try:
            dispenseParameters = pickle.load(open('/data/user_storage/BenchItems.pkl', 'rb'))
        except FileNotFoundError:
            dispenseParameters = pickle.load(open('{}/BenchItems.pkl'.format(path), 'rb'))
    
    reservoirDeckSlot = dispenseParameters['reservoirDeckSlot']
    reservoirType = dispenseParameters['reservoirType']
    reservoirLocation = dispenseParameters['reservoirLocation']
    destinationPlates = dispenseParameters['destinationPlates']
    plateType = dispenseParameters['plateType']
    dispenseVolume = dispenseParameters['volume']

    bench_items = {reservoirDeckSlot:reservoirType}
    for i, destinationPlate in enumerate(destinationPlates):
        bench_items[destinationPlate] = plateType[i]

    tips_300 = protocol.load_labware('opentrons_96_tiprack_300ul', 10)
    tips_20 = protocol.load_labware('opentrons_96_tiprack_20ul', 11)
    
    left = protocol.load_instrument('p300_multi_gen2', 'left',  tip_racks=[tips_300])
    right = protocol.load_instrument('p20_multi_gen2', 'right',  tip_racks=[tips_20])
    if not protocol.is_simulating():
        tipLoc_300 = int(open('/data/user_storage/300uL_tipColumn.txt', 'r').read())
        tipLoc_20 = int(open('/data/user_storage/20uL_tipColumn.txt', 'r').read())
    else:
        tipLoc_300 = 1
        tipLoc_20 = 1
    plates, reservoirs = load_bench(protocol, bench_items)

    reservoir = reservoirs[reservoirDeckSlot][reservoirLocation]
    pipette_to_use = left if dispenseVolume >= 20 else right
    tips_to_use = tips_300 if pipette_to_use == left else tips_20
    tip_position = tipLoc_300 if tips_to_use == tips_300 else tipLoc_20
    try:
        pipette_to_use.pick_up_tip(tips_to_use['A'+str(tip_position)])
    except protocol_api.labware.OutOfTipsError:
        if pipette_to_use == left:
            val = '300uL'
        else:
            val = '20uL'
        protocol.set_rail_lights(False)
        protocol.pause("Replace the tips for {} pipette.".format(val))
        protocol.set_rail_lights(True)
        tip_position = 1
        pipette_to_use.pick_up_tip(tips_to_use['A'+str(tip_position)])
    if not protocol.is_simulating():
        tip_position += 1
        if tips_to_use == tips_300:
            open('/data/user_storage/300uL_tipColumn.txt', 'w').write(str(tip_position))
        else:
            open('/data/user_storage/20uL_tipColumn.txt', 'w').write(str(tip_position))
    for plate in plates.values():
        pipette_to_use.distribute(dispenseVolume, reservoir, plate.wells(), \
            new_tip='never',blow_out=True, blowout_location='source well')
    pipette_to_use.drop_tip()
    protocol.set_rail_lights(False)

def load_bench(protocol, bench_items):
    '''
    Returns 2 dicts for plates and reagent reservoirs loaded into the opentrons protocol (value) by deck position (key).
    '''
    plates = {}
    reservoirs = {}
    for deck_slot in bench_items.keys():
        deck_item = bench_items[deck_slot]
        if deck_item == '96-well':
            plates[deck_slot] = protocol.load_labware('costar_96_wellplate_320ul', deck_slot)
        elif deck_item == '384-well':
            plates[deck_slot] = protocol.load_labware('plateone_384_wellplate_140ul', deck_slot)
        elif deck_item == 'divided':
            reservoirs[deck_slot] = protocol.load_labware('nest_12_reservoir_15ml', deck_slot)
        elif deck_item == 'single':
            reservoirs[deck_slot] = protocol.load_labware('nest_1_reservoir_195ml', deck_slot)
    
    return plates, reservoirs
