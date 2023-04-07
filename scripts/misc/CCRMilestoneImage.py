import numpy as np
import string

metadata = {
    'protocolName': 'CCR Milestone Image',
    'author': 'Madison Wahlsten @madisonwahlsten',
    'description': 'Draw a picture of a dendritic cell and T cell',
    'apiLevel': '2.9'
}


def run(ctx):

    # Load Labware
    tiprack = ctx.load_labware('opentrons_96_tiprack_1000ul', 6)
    plate = ctx.load_labware('plateone_384_wellplate_140ul', 1)
    reservoir = ctx.load_labware('nest_12_reservoir_15ml', 2)

    # Load Pipette
    p300 = ctx.load_instrument('p1000_single_gen2', 'right',
                               tip_racks=[tiprack])

    # Solutions
    color1 = reservoir['A1'] # PURPLE
    color2 = reservoir['A2'] # DARK PURPLE
    color3 = reservoir['A3'] # GREEN
    color4 = reservoir['A4'] # DARK GREEN
    colors = [color1, color2, color3, color4]

    # Decode image to wells
    color1_wells = []
    color2_wells = []
    color3_wells = []
    color4_wells = []

    color_array = np.loadtxt('/data/user_storage/DC_map.csv', delimiter=',', dtype=str)
    print(color_array.shape)
    for i, row in enumerate(list(string.ascii_uppercase)[:16]):
        for j, col in enumerate(range(1,25)):
            if color_array[i, j] == 'P':
                color1_wells.append(row+str(col))
            elif color_array[i, j] == 'DP':
                color2_wells.append(row+str(col))
            elif color_array[i, j] == 'G':
                color3_wells.append(row+str(col))
            elif color_array[i, j] == 'DG':
                color4_wells.append(row+str(col))
    
    color1_wells = [plate.wells_by_name()[i].top() for i in color1_wells] # PURPLE
    color2_wells = [plate.wells_by_name()[i].top() for i in color2_wells] # DARK PURPLE
    color3_wells = [plate.wells_by_name()[i].top() for i in color3_wells] # GREEN
    color4_wells = [plate.wells_by_name()[i].top() for i in color4_wells] #DARK GREEN

    wells = [color1_wells, color2_wells, color3_wells, color4_wells]

    # Distribute solution to wells
    for i in range(4):
        p300.distribute(100, colors[i], wells[i], disposal_vol=0, trash=False, blow_out=True, blowout_location='source well')
