# CG 2024.1 - Assignment 1
#
# D. H. Lelis - 12543822
# Samuel Figueiredo Veronez - 12542626


DEFAULT_MATERIAL = "default"


# Adapted from the files provided by the professor (Ricardo Marcondes Marcacini)
def load_obj(filepath: str, split_objects=False):
    vertices = []
    texture_coords = []
    normals = []
    models = []
    current_model = {
        "name": "_root",
        "vertices": [],
        "normals": [],
        "texture": [],
        "faces": [],
    }
    vertex_offset = 0
    texture_offset = 0
    normal_offset = 0
    material = "default"

    with open(filepath, "r") as file:
        for line in file:
            if line.startswith("#"):
                continue

            values = line.split()
            if not values:
                continue

            if split_objects and values[0] == "o":
                # When a new object is declared, save the current model and start a new one
                if (
                    current_model["vertices"]
                    or current_model["texture"]
                    or current_model["faces"]
                    or current_model["normals"]
                ):
                    models.append(current_model)

                new_name = values[1]
                current_model = {
                    "name": new_name,
                    "vertices": [],
                    "texture": [],
                    "faces": [],
                    "normals": [],
                }
                vertex_offset += len(vertices)
                texture_offset += len(texture_coords)
                normal_offset += len(normals)
                vertices = []
                texture_coords = []
                normals = []

            elif values[0] == "v":
                vertices.append(values[1:4])
                current_model["vertices"].append(values[1:4])

            elif values[0] == "vn":
                normals.append(values[1:4])
                current_model["normals"].append(values[1:4])

            elif values[0] == "vt":
                texture_coords.append(values[1:3])
                current_model["texture"].append(values[1:3])

            elif values[0] in ("usemtl", "usemat"):
                material = values[1]

            elif values[0] == "f":
                face = []
                face_texture = []
                face_normal = []
                for v in values[1:]:
                    w = v.split("/")
                    # Re-index vertex positions
                    if len(w) > 0 and w[0].isdigit():
                        face.append(int(w[0]) - vertex_offset)
                    # Re-index texture coordinates
                    if len(w) >= 2 and w[1].isdigit():
                        face_texture.append(int(w[1]) - texture_offset)
                    else:
                        face_texture.append(0)

                    # Re-index normals
                    if len(w) >= 3 and w[2].isdigit():
                        face_normal.append(int(w[2]) - normal_offset)

                current_model["faces"].append(
                    (face, face_texture, face_normal, material)
                )

    # Append the last model if it has any content
    if (
        current_model["vertices"]
        or current_model["texture"]
        or current_model["faces"]
        or current_model["normals"]
    ):
        models.append(current_model)

    return models


def load_mtllib(filepath: str):
    """Loads a Wavefront material library."""
    materials = {}
    material = None
    for line in open(filepath, "r"):
        if line.startswith("#"):
            continue
        values = line.split()
        if not values:
            continue
        if values[0] == "newmtl":
            material = {}
            materials[values[1]] = material
        if material is None:
            continue
        if values[0] == "Kd":
            material["Kd"] = list(map(float, values[1:]))
        if values[0] == "map_Kd":
            material["map_Kd"] = values[1]
        if values[0] == "d":
            material["d"] = float(values[1])

        if values[0] == "Ka":
            material["Ka"] = list(map(float, values[1:]))

        if values[0] == "Ks":
            material["Ks"] = list(map(float, values[1:]))

        if values[0] == "Ke":
            material["Ke"] = list(map(float, values[1:]))

        if values[0] == "Ni":
            material["Ni"] = float(values[1])

        if values[0] == "illum":
            material["illum"] = float(values[1])

    return materials


if __name__ == "__main__":
    model_file = input("Enter the name of the model file: ")
    model = load_obj(model_file)
    print("Model: ", model)
