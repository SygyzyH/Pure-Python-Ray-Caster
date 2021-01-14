import main
import settings
import type_enumerator


def init():
    main.game_map = []
    file = open("maps/start.map", "r")
    for line in file:
        if line.find("d: ") == -1:
            main.game_map.append(line.replace("\n", "").split(" "))
        else:
            if line.find("portals") is not -1:
                load_data(line, "portal")
            elif line.find("sectors") is not -1:
                load_data(line, "sector")
            elif line.find("sprites") is not -1:
                load_data(line, "sprite")
            elif line.find("enemies") is not -1:
                pass
    return main.game_map


def load(filename: str):
    main.game_map = []
    file = open("maps/" + filename + ".map", "r")
    for line in file:
        if line.find("d: ") == -1:
            main.game_map.append(line.replace("\n", "").split(" "))
        else:
            if line.find("portals") is not -1:
                load_data(line, "portal")
            elif line.find("sectors") is not -1:
                load_data(line, "sector")
            elif line.find("sprites") is not -1:
                load_data(line, "sprite")
            elif line.find("enemies") is not -1:
                pass


def load_data(line, game_piece_type):
    if line.find(game_piece_type + "s") is not -1:
        setattr(settings, game_piece_type + "s", [])
        # remove unnecessary parts of string (\n, intro section)
        parsed_line = line[len("d: " + str(game_piece_type) + " - "):-2]
        parsed_line = parsed_line.split(";")
        for piece in parsed_line:
            piece = piece.split(": ")
            getattr(settings, game_piece_type + "s").append(type_enumerator.GamePiece(getattr(type_enumerator.PieceType, game_piece_type.upper()), eval(piece[0]), eval(piece[1])))
