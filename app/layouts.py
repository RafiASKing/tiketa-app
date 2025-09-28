"""Seat layout definitions for auditorium seating maps."""

from __future__ import annotations

# Seat map uses strings for seats (e.g., "A1") and None for aisles/walkways.
# Each inner list represents a row in the auditorium. Columns align across rows
# so CSS grid can render the layout faithfully.

SEAT_MAP: list[list[str | None]] = [
    # A
    ["A1","A2","A3","A4","A5","A6","A7","A8","A9",None,"A10","A11","A12","A13","A14","A15","A16","A17","B18"],
    # B
    ["B1","B2","B3","B4","B5","B6","B7","B8","B9",None,"B10","B11","B12","B13","B14","B15","B16","B17","B18"],
    # C
    ["C1","C2","C3","C4","C5","C6","C7","C8","C9",None,"C10","C11","C12","C13","C14","C15","C16","C17","C18"],
    # D
    ["D1","D2","D3","D4","D5","D6","D7","D8","D9",None,"D10","D11","D12","D13","D14","D15","D16","D17","D18"],
    # E
    ["E1","E2","E3","E4","E5","E6","E7","E8","E9",None,"E10","E11","E12","E13","E14","E15","E16","E17","E18"],
    # F
    ["F1","F2","F3","F4","F5","F6","F7","F8","F9",None,"F10","F11","F12","F13","F14","F15","F16","F17","F18"],
    # G
    ["G1","G2","G3","G4","G5","G6","G7","G8","G9",None,"G10","G11","G12","G13","G14","G15","G16","G17","G18"],
    # H
    ["H1","H2","H3","H4","H5","H6","H7","H8","H9",None,"H10","H11","H12","H13","H14","H15","H16","H17","H18"],
    # I
    ["I1","I2","I3","I4","I5","I6","I7","I8","I9",None,"I10","I11","I12","I13","I14","I15","I16","I17","I18"],
    # J
    ["J1","J2","J3","J4","J5","J6","J7","J8","J9",None,"J10","J11","J12","J13","J14","J15","J16","J17","J18"],
    # K (kosong lorong)
    [None]*19,
    # L (lebih sempit)
    ["L1","L2","L3","L4","L5","L6","L7","L8","L9",None,"L10","L11","L12","L13","L14","L15","L16","L17","L18"],
    # M (lebih sempit lagi)
    ["M1","M2","M3","M4","M5","M6","M7","M8","M9",None,"M10","M11","M12","M13","M14","M15","M16","M17","M18"]
]





