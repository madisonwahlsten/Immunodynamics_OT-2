import numpy as np

metadata = {
    'protocolName': 'Block M',
    'author': 'Madison Wahlsten @madisonwahlsten',
    'description': 'Draw a picture of a University of Michigan "block M" logo',
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
    maize = reservoir['A3']
    blue = reservoir['A2']

    # Decode image to wells
    blue_wells = [well.top() for well in plate.wells(
        'A3', 'A4', 'A5', 'A6', 'A17', 'A18', 'A19', 'A20', 'B3', 'B7', 'B16', 'B20', 'C3', 'C8', 'C15', 'C20', 'D3', 'D4', 'D9', 'D14', 'D19', 'D20', 'E4', 'E10', 'E13', 'E19', 'F4', 'F7', 'F11', 'F12', 'F16', 'F19', 'G4', 'G7', 'G8', 'G15', 'G16', 'G19', 'H4', 'H7', 'H9', 'H14', 'H16', 'H19', 'I4', 'I7', 'I10', 'I13', 'I16', 'I19', 'J4', 'J7', 'J10', 'J13', 'J16', 'J19', 'K4', 'K7', 'K10', 'K11', 'K12', 'K13', 'K16', 'K19', 'L4', 'L7', 'L16', 'L19', 'M3', 'M4', 'M7', 'M15', 'M16', 'M19', 'M20', 'N3', 'N8', 'N15', 'N20', 'O3', 'O8', 'O15', 'O20', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P15', 'P16', 'P17', 'P18', 'P19', 'P20')]
    maize_wells = [well.top() for well in plate.wells(
        'B4', 'B5', 'B6', 'B17', 'B18', 'B19', 'C4', 'C5', 'C6', 'C7', 'C16', 'C17', 'C18', 'C19', 'D5', 'D6', 'D7', 'D8', 'D15', 'D16', 'D17', 'D18', 'E5', 'E6', 'E7', 'E8', 'E9', 'E14', 'E15', 'E16', 'E17', 'E18', 'F5', 'F6', 'F8', 'F9', 'F10', 'F13', 'F14', 'F15', 'F17', 'F18', 'G5', 'G6', 'G9', 'G10', 'G11', 'G12', 'G13', 'G14', 'G17', 'G18', 'H5', 'H6', 'H10', 'H11', 'H12', 'H13', 'H17', 'H18', 'I5', 'I6', 'I11', 'I12', 'I17', 'I18', 'J5', 'J6', 'J11', 'J12', 'J17', 'J18', 'K5', 'K6', 'K17', 'K18', 'L5', 'L6', 'L17', 'L18', 'M5', 'M6', 'M17', 'M18', 'N4', 'N5', 'N6', 'N7', 'N16', 'N17', 'N18', 'N19', 'O4', 'O5', 'O6', 'O7', 'O16', 'O17', 'O18', 'O19'
    )]

     # Distribute maize solution to wells
    p300.distribute(100, maize, maize_wells, disposal_vol=0, trash=False, blow_out=True, blowout_location='source well')
    # Distribute blue solution to wells
    p300.distribute(100, blue, blue_wells, disposal_vol=0, trash=False, blow_out=True, blowout_location='source well')
